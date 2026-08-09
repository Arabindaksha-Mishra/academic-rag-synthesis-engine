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


@unique
class COCOMOModel(Enum):
    """Enumeration of standard Basic COCOMO software project categories."""

    ORGANIC = "organic"
    SEMIDETACHED = "semidetached"
    EMBEDDED = "embedded"


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
            dict[str, str | int]: Dictionary storing source metadata.
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
class ProjectParameters:
    """Dynamic project specification and mathematical parameter configuration.

    Attributes:
        system_name: Name of the target software system.
        domain: Industry vertical (e.g., 'Autonomous Drone Fleet Traffic Management').
        nfr_latency_p99_ms: P99 latency requirement threshold in milliseconds.
        nfr_availability_pct: High-availability SLA target percentage.
        nfr_telemetry_hz: Telemetry ingestion throughput frequency in Hz.
        ufp_inputs: External Inputs count.
        ufp_outputs: External Outputs count.
        ufp_inquiries: External Inquiries count.
        ufp_internal_files: Internal Logical Files count.
        ufp_external_interfaces: External Interface Files count.
        complexity_adjustment_factors_sum: Sum of 14 GSC degrees of influence.
        cocomo_category: Organic, Semidetached, or Embedded project model.
        loc_per_function_point: Lines of code multiplier per function point.
        labor_cost_per_person_month_usd: Blended engineering labor rate in USD.
    """

    system_name: str = "AeroGrid"
    domain: str = "Autonomous Drone Fleet Traffic Management"
    nfr_latency_p99_ms: int = 150
    nfr_availability_pct: float = 99.999
    nfr_telemetry_hz: int = 100
    ufp_inputs: int = 6
    ufp_outputs: int = 5
    ufp_inquiries: int = 4
    ufp_internal_files: int = 4
    ufp_external_interfaces: int = 3
    complexity_adjustment_factors_sum: int = 42
    cocomo_category: COCOMOModel = COCOMOModel.SEMIDETACHED
    loc_per_function_point: int = 53
    labor_cost_per_person_month_usd: float = 8500.0


@dataclass(frozen=True)
class FPSizingResult:
    """Results of dynamic Function Point analysis and code size derivation.

    Attributes:
        unadjusted_function_points: Computed raw UFP value.
        value_adjustment_factor: Computed VAF based on degrees of influence.
        adjusted_function_points: Final AFP value.
        derived_kloc: Derived thousands of source lines of code.
    """

    unadjusted_function_points: int
    value_adjustment_factor: float
    adjusted_function_points: float
    derived_kloc: float


@dataclass(frozen=True)
class COCOMOResult:
    """Results of dynamic Basic COCOMO effort and duration estimation.

    Attributes:
        effort_person_months: Total required development effort in Person-Months.
        development_time_months: Nominal project duration in calendar months.
        average_staff_size: Recommended full-time engineering team headcount.
        estimated_total_cost_usd: Total estimated engineering labor cost.
        productivity_loc_per_pm: Computed productivity in LOC per Person-Month.
    """

    effort_person_months: float
    development_time_months: float
    average_staff_size: float
    estimated_total_cost_usd: float
    productivity_loc_per_pm: float


@dataclass(frozen=True)
class QueryMatch:
    """Represents an individual semantically retrieved document match.

    Attributes:
        content: Extracted textual chunk body.
        source: Originating document filename.
        page_or_slide: Page or slide number.
        doc_type: Document classification tag.
        relevance_score: Optional similarity or distance metric score.
    """

    content: str
    source: str
    page_or_slide: int
    doc_type: str
    relevance_score: float | None = None


@dataclass(frozen=True)
class QueryResponse:
    """Structured response container for semantic search queries.

    Attributes:
        query: Original natural language search query.
        matches: List of retrieved QueryMatch objects.
        formatted_context: Formatted Markdown context blocks with citations.
        total_indexed_chunks: Total chunks active in vector index.
    """

    query: str
    matches: list[QueryMatch]
    formatted_context: str
    total_indexed_chunks: int


@dataclass(frozen=True)
class RAGConfig:
    """Configuration settings for embedding models and vector collections.

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
