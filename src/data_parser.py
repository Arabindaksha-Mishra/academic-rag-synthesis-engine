"""Document Parsing and Extraction Engine.

Provides extensible, multi-modal document extraction strategies for parsing
heterogeneous academic materials (PDF lecture notes, presentation slide decks,
and curriculum rubric specifications) into discrete, typed semantic chunks.
"""

from __future__ import annotations

import logging
import os
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Final

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pptx import Presentation
from pypdf import PdfReader

from src.data_modal import DocumentChunk, build_chunk

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger: Final[logging.Logger] = logging.getLogger("DataParser")


def extract_paragraph_texts(shape: Any) -> list[str]:
    """Helper function to extract non-empty text strings from a shape frame.

    Args:
        shape: PPTX slide shape object.

    Returns:
        list[str]: Cleaned paragraph strings.
    """
    if not hasattr(shape, "has_text_frame") or not shape.has_text_frame:
        return []
    lines: list[str] = []
    for paragraph in shape.text_frame.paragraphs:
        cleaned: str = paragraph.text.strip()
        if cleaned:
            lines.append(cleaned)
    return lines


def extract_slide_text(slide: Any) -> str:
    """Helper function to aggregate all text content across shapes in a slide.

    Args:
        slide: PPTX slide object.

    Returns:
        str: Cleaned newline-separated slide text.
    """
    text_runs: list[str] = []
    for shape in slide.shapes:
        text_runs.extend(extract_paragraph_texts(shape))
    return "\n".join(text_runs).strip()


def extract_page_text(page: Any) -> str | None:
    """Helper function to extract and strip text from a PDF page object.

    Args:
        page: PyPDF page object.

    Returns:
        Optional[str]: Cleaned string if text is present, None otherwise.
    """
    raw_text: str | None = page.extract_text()
    if raw_text:
        cleaned: str = raw_text.strip()
        return cleaned if cleaned else None
    return None


class BaseDocumentExtractor(ABC):
    """Abstract Base Class defining document extraction strategy interface."""

    @abstractmethod
    def can_handle(self, file_path: str) -> bool:
        """Determines if the extractor supports the given file format.

        Args:
            file_path: Absolute or relative path to the candidate file.

        Returns:
            bool: True if supported, False otherwise.
        """

    @abstractmethod
    def extract_chunks(
        self, file_path: str, start_chunk_id: int, min_length: int = 25
    ) -> list[DocumentChunk]:
        """Extracts discrete semantic chunks from the source document.

        Args:
            file_path: Path to the target document.
            start_chunk_id: Starting integer sequence for unique chunk IDs.
            min_length: Minimum character threshold for valid content.

        Returns:
            list[DocumentChunk]: Extracted and validated document chunks.
        """


class PPTXExtractor(BaseDocumentExtractor):
    """Extractor strategy for PowerPoint slide presentations (.pptx, .ppt)."""

    def can_handle(self, file_path: str) -> bool:
        """Checks if the file extension corresponds to a presentation.

        Args:
            file_path: Path to the target file.

        Returns:
            bool: True if presentation format, False otherwise.
        """
        ext: str = os.path.splitext(file_path)[1].lower()
        return ext in (".pptx", ".ppt")

    def extract_chunks(
        self, file_path: str, start_chunk_id: int, min_length: int = 25
    ) -> list[DocumentChunk]:
        """Extracts text slide-by-slide from presentation shape text frames.

        Args:
            file_path: Path to the presentation file.
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
        except Exception as err:
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
        self, file_path: str, start_chunk_id: int, min_length: int = 25
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
        except Exception as err:
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
        self, file_path: str, start_chunk_id: int, min_length: int = 25
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
                except Exception:
                    pass

        return []
