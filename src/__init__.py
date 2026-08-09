"""Academic RAG Synthesis Engine Core Package.

Provides high-performance multi-modal document extraction, ChromaDB
vector indexing, semantic grounding, dynamic parameterized report synthesis,
directory file watcher hot-reloading, and FastAPI REST endpoints.
"""

from src.api_server import app, run_api_server
from src.data_modal import (
    BuilderConfig,
    BuildResult,
    COCOMOModel,
    COCOMOResult,
    DiagramType,
    DocumentChunk,
    FPSizingResult,
    ProjectParameters,
    QueryMatch,
    QueryResponse,
    RAGConfig,
    build_chunk,
    get_default_repo_root,
)
from src.data_parser import (
    BaseDocumentExtractor,
    DocumentExtractorRegistry,
    PDFExtractor,
    PPTXExtractor,
)
from src.rag_pipeline import AcademicRAGPipeline
from src.synthesis_engine import (
    compute_cocomo_metrics,
    compute_function_points,
    synthesize_dynamic_report_markdown,
)
from src.utils import (
    DiagramProcessor,
    HeadlessPDFCompiler,
    MarkdownDocumentRenderer,
)
from src.vector_svgs import (
    DIAGRAM_REGISTRY,
    get_activity_svg,
    get_all_diagrams,
    get_class_diagram_svg,
    get_context_svg,
    get_diagram_by_type,
    get_microservices_svg,
    get_use_case_svg,
)
from src.watcher import DynamicKnowledgeWatcher, KnowledgeBaseChangeHandler

__all__ = [
    "DIAGRAM_REGISTRY",
    "AcademicRAGPipeline",
    "BaseDocumentExtractor",
    "BuildResult",
    "BuilderConfig",
    "COCOMOModel",
    "COCOMOResult",
    "DiagramProcessor",
    "DiagramType",
    "DocumentChunk",
    "DocumentExtractorRegistry",
    "DynamicKnowledgeWatcher",
    "FPSizingResult",
    "HeadlessPDFCompiler",
    "KnowledgeBaseChangeHandler",
    "MarkdownDocumentRenderer",
    "PDFExtractor",
    "PPTXExtractor",
    "ProjectParameters",
    "QueryMatch",
    "QueryResponse",
    "RAGConfig",
    "app",
    "build_chunk",
    "compute_cocomo_metrics",
    "compute_function_points",
    "get_activity_svg",
    "get_all_diagrams",
    "get_class_diagram_svg",
    "get_context_svg",
    "get_default_repo_root",
    "get_diagram_by_type",
    "get_microservices_svg",
    "get_use_case_svg",
    "run_api_server",
    "synthesize_dynamic_report_markdown",
]
