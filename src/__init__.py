"""Academic RAG Synthesis Engine Core Package.

Provides high-performance multi-modal document extraction, ChromaDB
vector indexing, semantic grounding, vector SVG rendering, and
publication-grade PDF deliverable compilation.
"""

from src.data_modal import (
    BuilderConfig,
    BuildResult,
    DiagramType,
    DocumentChunk,
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

__all__ = [
    "DIAGRAM_REGISTRY",
    "AcademicRAGPipeline",
    "BaseDocumentExtractor",
    "BuildResult",
    "BuilderConfig",
    "DiagramProcessor",
    "DiagramType",
    "DocumentChunk",
    "DocumentExtractorRegistry",
    "HeadlessPDFCompiler",
    "MarkdownDocumentRenderer",
    "PDFExtractor",
    "PPTXExtractor",
    "RAGConfig",
    "build_chunk",
    "get_activity_svg",
    "get_all_diagrams",
    "get_class_diagram_svg",
    "get_context_svg",
    "get_default_repo_root",
    "get_diagram_by_type",
    "get_microservices_svg",
    "get_use_case_svg",
]
