"""Data Models, Schemas, and Immutable Value Objects.

Defines all core domain entities, configuration schemas, results,
and data transfer models utilized across the Academic RAG engine.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from enum import Enum, unique


def get_default_repo_root() -> str:
    """Helper function computing the absolute path of the repository root.

    Returns:
        str: Absolute path to the repository directory.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


@unique
class DiagramType(Enum):
    """Enumeration of available architectural and UML diagrams."""

    CONTEXT = "context"
    USE_CASE = "use_case"
    ACTIVITY = "activity"
    CLASS_DIAGRAM = "class_diagram"
    MICROSERVICES = "microservices"


@dataclass(frozen=True)
class DocumentChunk:
    """Represents a discrete semantic knowledge chunk extracted from a document.

    Attributes:
        content: Cleaned textual body of the chunk.
        source_file: Basename of the originating source document.
        page_or_slide: 1-indexed page or slide number where chunk originates.
        doc_type: Semantic classification tag (e.g., 'pdf_document').
        chunk_id: Unique string identifier for ChromaDB vector indexing.
    """

    content: str
    source_file: str
    page_or_slide: int
    doc_type: str
    chunk_id: str

    def to_metadata(self) -> dict[str, str | int]:
        """Serializes chunk metadata for vector database storage.

        Returns:
            dict[str, Union[str, int]]: Dictionary storing source metadata.
        """
        return {
            "source": self.source_file,
            "slide_or_page": self.page_or_slide,
            "doc_type": self.doc_type,
        }


def build_chunk(
    content: str,
    source_file: str,
    page_or_slide: int,
    doc_type: str,
    chunk_index: int,
) -> DocumentChunk:
    """Helper factory function to construct a typed DocumentChunk instance.

    Args:
        content: Extracted textual content.
        source_file: Source document filename.
        page_or_slide: Page or slide 1-indexed number.
        doc_type: Semantic classification label.
        chunk_index: Unique integer index for chunk ID generation.

    Returns:
        DocumentChunk: Initialized immutable chunk instance.
    """
    return DocumentChunk(
        content=content,
        source_file=source_file,
        page_or_slide=page_or_slide,
        doc_type=doc_type,
        chunk_id=f"chunk_{chunk_index}",
    )


@dataclass(frozen=True)
class RAGConfig:
    """Configuration settings for embedding models and vector database collections.

    Attributes:
        embedding_model_name: HuggingFace sentence-transformer model tag.
        collection_name: Target ChromaDB collection name.
        min_chunk_length: Minimum character length required to index a chunk.
        default_top_k: Default number of relevant chunks to retrieve per query.
        knowledge_base_dir: Name of the source directory containing courseware.
    """

    embedding_model_name: str = "all-MiniLM-L6-v2"
    collection_name: str = "se_academic_knowledge_base"
    min_chunk_length: int = 25
    default_top_k: int = 4
    knowledge_base_dir: str = "knowledge_base"


@dataclass(frozen=True)
class BuilderConfig:
    """Configuration settings for document building and PDF generation.

    Attributes:
        repo_root: Root directory of the repository.
        output_dir: Target output directory for generated deliverables.
        md_filename: Name of the master source markdown file.
        html_filename: Name of the compiled HTML output file.
        pdf_filename: Name of the final PDF deliverable.
        docx_filename: Name of the editable Word document.
        page_size: Print page format (default: 'A4').
        virtual_time_budget_ms: Budget allocated for MathJax rendering in Chrome.
    """

    repo_root: str = field(default_factory=get_default_repo_root)
    output_dir: str = "output"
    md_filename: str = "AeroGrid_Assignment_Solution.md"
    html_filename: str = "AeroGrid_Assignment_Solution.html"
    pdf_filename: str = "AeroGrid_Assignment_Solution.pdf"
    docx_filename: str = "AeroGrid_Assignment_Solution.docx"
    page_size: str = "A4"
    virtual_time_budget_ms: int = 9000

    @property
    def full_output_dir(self) -> str:
        """Returns absolute path to the output directory."""
        return os.path.join(self.repo_root, self.output_dir)

    @property
    def md_path(self) -> str:
        """Returns absolute path to the master markdown file."""
        return os.path.join(self.full_output_dir, self.md_filename)

    @property
    def html_path(self) -> str:
        """Returns absolute path to the compiled HTML file."""
        return os.path.join(self.full_output_dir, self.html_filename)

    @property
    def pdf_path(self) -> str:
        """Returns absolute path to the output PDF file."""
        return os.path.join(self.full_output_dir, self.pdf_filename)

    @property
    def docx_path(self) -> str:
        """Returns absolute path to the output DOCX file."""
        return os.path.join(self.full_output_dir, self.docx_filename)


@dataclass(frozen=True)
class BuildResult:
    """Encapsulates the status and output artifact paths of a build run.

    Attributes:
        success: True if all target documents were created successfully.
        html_path: Absolute path to the generated HTML file.
        pdf_path: Absolute path to the generated PDF file (if successful).
        pdf_size_kb: File size of the generated PDF in kilobytes.
        errors: List of error messages encountered during build execution.
    """

    success: bool
    html_path: str
    pdf_path: str | None = None
    pdf_size_kb: float = 0.0
    errors: list[str] = field(default_factory=list)
