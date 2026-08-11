"""Multi-Modal Document Extractors, Parsers, and Chunking Registry.

Implements the Strategy Pattern for extracting structured semantic chunks
from Adobe PDF documents and Microsoft PowerPoint presentations with automatic
format fallback handling and metadata preservation.
"""

from __future__ import annotations

import logging
import os
import sys
from abc import ABC, abstractmethod
from collections.abc import Sequence
from pathlib import Path
from typing import Any, Final

from pptx import Presentation
from pptx.slide import Slide
from pypdf import PdfReader
from pypdf.errors import PyPdfError

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data_modal import DocumentChunk, build_chunk

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger: Final[logging.Logger] = logging.getLogger("DataParser")


def extract_paragraph_texts(paragraphs: Sequence[Any]) -> list[str]:
    """Helper function to extract non-empty cleaned strings from text paragraphs.

    Args:
        paragraphs: Collection of paragraph objects containing raw text.

    Returns:
        list[str]: Cleaned, non-empty text strings.
    """
    results: list[str] = []
    for p in paragraphs:
        text_content: str = p.text.strip()
        if text_content:
            results.append(text_content)
    return results


def extract_slide_text(slide: Slide) -> str:
    """Helper function extracting all text runs from shapes within a PowerPoint slide.

    Args:
        slide: Target PowerPoint slide instance.

    Returns:
        str: Consolidated newline-delimited slide text.
    """
    text_runs: list[str] = []
    for shape in slide.shapes:
        if shape.has_text_frame:
            extracted: list[str] = extract_paragraph_texts(shape.text_frame.paragraphs)
            text_runs.extend(extracted)
    return "\n".join(text_runs)


def extract_page_text(page: Any) -> str | None:
    """Helper function safely extracting text content from a PyPDF page.

    Args:
        page: PyPDF page object.

    Returns:
        str | None: Cleaned text string if extraction succeeds, None otherwise.
    """
    try:
        raw_text: str | None = page.extract_text()
        return raw_text.strip() if raw_text else None
    except (PyPdfError, KeyError, ValueError, OSError):
        return None


class BaseDocumentExtractor(ABC):
    """Abstract Base Class establishing the strategy interface for file extraction."""

    @abstractmethod
    def can_handle(self, file_path: str) -> bool:
        """Determines if the extractor strategy supports the given file format.

        Args:
            file_path: Path to the target document.

        Returns:
            bool: True if supported, False otherwise.
        """

    @abstractmethod
    def extract_chunks(
        self,
        file_path: str,
        start_chunk_id: int,
        min_length: int = 25,
    ) -> list[DocumentChunk]:
        """Extracts structured document chunks with attached metadata.

        Args:
            file_path: Path to the source file.
            start_chunk_id: Current chunk ID integer counter.
            min_length: Minimum character count required to keep a chunk.

        Returns:
            list[DocumentChunk]: List of extracted DocumentChunk objects.
        """


class PPTXExtractor(BaseDocumentExtractor):
    """Extractor strategy for Microsoft PowerPoint slide presentations (.pptx, .ppt)."""

    def can_handle(self, file_path: str) -> bool:
        """Checks if the file extension corresponds to a presentation format.

        Args:
            file_path: Path to the target file.

        Returns:
            bool: True if PPT/PPTX format, False otherwise.
        """
        lowered: str = file_path.lower()
        return lowered.endswith((".pptx", ".ppt"))

    def extract_chunks(
        self,
        file_path: str,
        start_chunk_id: int,
        min_length: int = 25,
    ) -> list[DocumentChunk]:
        """Extracts text frame content slide-by-slide from presentations.

        Args:
            file_path: Path to the PowerPoint file.
            start_chunk_id: Current chunk ID counter.
            min_length: Minimum text length filter.

        Returns:
            list[DocumentChunk]: Extracted slide chunks.
        """
        chunks: list[DocumentChunk] = []
        filename: str = os.path.basename(file_path)
        try:
            prs: Presentation = Presentation(file_path)
            for slide_idx, slide in enumerate(prs.slides, start=1):
                full_text: str = extract_slide_text(slide)
                if len(full_text) >= min_length:
                    current_id: int = start_chunk_id + len(chunks)
                    chunk_obj: DocumentChunk = build_chunk(
                        content=full_text,
                        source_file=filename,
                        page_or_slide=slide_idx,
                        doc_type="presentation_slide",
                        chunk_index=current_id,
                    )
                    chunks.append(chunk_obj)
        except (KeyError, ValueError, OSError, AttributeError, TypeError) as err:
            logger.warning(f"PPTX extraction bypassed for {filename}: {err}")
        return chunks


class PDFExtractor(BaseDocumentExtractor):
    """Extractor strategy for Adobe Portable Document Format files (.pdf)."""

    def can_handle(self, file_path: str) -> bool:
        """Checks if the file extension corresponds to a PDF document.

        Args:
            file_path: Path to the target file.

        Returns:
            bool: True if PDF format, False otherwise.
        """
        return file_path.lower().endswith(".pdf")

    def extract_chunks(
        self,
        file_path: str,
        start_chunk_id: int,
        min_length: int = 25,
    ) -> list[DocumentChunk]:
        """Extracts text page-by-page from PDF documents using PyPDF.

        Args:
            file_path: Path to the PDF file.
            start_chunk_id: Current chunk ID counter.
            min_length: Minimum text length filter.

        Returns:
            list[DocumentChunk]: Extracted page chunks.
        """
        chunks: list[DocumentChunk] = []
        filename: str = os.path.basename(file_path)
        try:
            reader: PdfReader = PdfReader(file_path)
            for page_idx, page in enumerate(reader.pages, start=1):
                page_text: str | None = extract_page_text(page)
                if page_text and len(page_text) >= min_length:
                    current_id: int = start_chunk_id + len(chunks)
                    chunk_obj: DocumentChunk = build_chunk(
                        content=page_text,
                        source_file=filename,
                        page_or_slide=page_idx,
                        doc_type="pdf_document",
                        chunk_index=current_id,
                    )
                    chunks.append(chunk_obj)
        except (PyPdfError, KeyError, ValueError, OSError) as err:
            logger.warning(f"PDF extraction bypassed for {filename}: {err}")
        return chunks


class DocumentExtractorRegistry:
    """Registry maintaining extraction strategies with multi-format fallback."""

    def __init__(self) -> None:
        """Initializes the registry with standard multi-modal extractors."""
        self._extractors: list[BaseDocumentExtractor] = [
            PPTXExtractor(),
            PDFExtractor(),
        ]

    def register_extractor(self, extractor: BaseDocumentExtractor) -> None:
        """Registers a new document extraction strategy.

        Args:
            extractor: Instance of a BaseDocumentExtractor subclass.
        """
        self._extractors.insert(0, extractor)

    def extract_from_file(
        self,
        file_path: str,
        start_chunk_id: int,
        min_length: int = 25,
    ) -> list[DocumentChunk]:
        """Attempts extraction across strategies with fallback handling.

        Args:
            file_path: Path to target file.
            start_chunk_id: Starting integer ID sequence.
            min_length: Minimum character length.

        Returns:
            list[DocumentChunk]: Extracted chunks if successful.
        """
        for extractor in self._extractors:
            if extractor.can_handle(file_path):
                chunks: list[DocumentChunk] = extractor.extract_chunks(
                    file_path=file_path,
                    start_chunk_id=start_chunk_id,
                    min_length=min_length,
                )
                if chunks:
                    return chunks

        for extractor in self._extractors:
            if not extractor.can_handle(file_path):
                try:
                    fallback_chunks: list[DocumentChunk] = extractor.extract_chunks(
                        file_path=file_path,
                        start_chunk_id=start_chunk_id,
                        min_length=min_length,
                    )
                    if fallback_chunks:
                        return fallback_chunks
                except (PyPdfError, KeyError, ValueError, OSError):
                    continue

        return []
