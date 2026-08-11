"""Robust Hybrid RAG Pipeline Implemented with LangChain and LCEL.

Combines dense vector semantic search (ChromaDB + all-MiniLM-L6-v2) with
sparse lexical keyword search (BM25) using LangChain's EnsembleRetriever
and Reciprocal Rank Fusion (RRF) for ultra-robust document grounding.
"""

from __future__ import annotations

import logging
import os
import sys
import warnings
from collections.abc import Sequence
from pathlib import Path
from typing import Final

from langchain_chroma import Chroma
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.retrievers.bm25 import BM25Retriever
from langchain_core.documents import Document

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data_modal import DocumentChunk, RAGConfig
from src.data_parser import DocumentExtractorRegistry
from src.rag_pipeline import scan_directory_for_extensions

warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger: Final[logging.Logger] = logging.getLogger("LangChainHybridRAG")


def convert_chunk_to_langchain_document(chunk: DocumentChunk) -> Document:
    """Converts a repository DocumentChunk into a LangChain Document value object.

    Args:
        chunk: Source DocumentChunk instance.

    Returns:
        Document: LangChain Document representation with preserved metadata.
    """
    return Document(
        page_content=chunk.content,
        metadata={
            "source": chunk.source_file,
            "slide_or_page": chunk.page_or_slide,
            "doc_type": chunk.doc_type,
            "chunk_id": chunk.chunk_id,
        },
    )


def format_langchain_documents(docs: Sequence[Document]) -> str:
    """Formats a list of LangChain documents into clean grounded Markdown blocks.

    Args:
        docs: Retrieved LangChain Document objects.

    Returns:
        str: Formatted Markdown text block containing citations and bodies.
    """
    formatted_chunks: list[str] = []
    for doc in docs:
        source_name: str = os.path.basename(str(doc.metadata.get("source", "Unknown")))
        page_num: int = int(doc.metadata.get("slide_or_page", 1))
        doc_type: str = str(doc.metadata.get("doc_type", "document"))
        formatted_chunks.append(
            f"### [Source: {source_name} | Page/Slide: {page_num} ({doc_type})]\n"
            f"{doc.page_content.strip()}"
        )
    return "\n\n".join(formatted_chunks)


def create_hybrid_ensemble_retriever(
    documents: Sequence[Document],
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    collection_name: str = "academic_langchain_ensemble",
    dense_weight: float = 0.6,
    bm25_weight: float = 0.4,
    top_k: int = 4,
) -> EnsembleRetriever:
    """Constructs a hybrid EnsembleRetriever blending Dense Vector and Sparse BM25.

    Args:
        documents: List of chunked LangChain Document objects.
        embedding_model_name: HuggingFace sentence-transformers model tag.
        collection_name: Target ChromaDB collection name.
        dense_weight: Weight allocated to dense semantic vector scores in RRF.
        bm25_weight: Weight allocated to sparse BM25 lexical scores in RRF.
        top_k: Number of combined candidate documents to retrieve.

    Returns:
        EnsembleRetriever: Configured hybrid ensemble retriever.
    """
    embeddings: HuggingFaceEmbeddings = HuggingFaceEmbeddings(
        model_name=embedding_model_name
    )

    vector_store: Chroma = Chroma.from_documents(
        documents=list(documents),
        embedding=embeddings,
        collection_name=collection_name,
    )
    dense_retriever = vector_store.as_retriever(search_kwargs={"k": top_k})

    bm25_retriever: BM25Retriever = BM25Retriever.from_documents(
        documents=list(documents)
    )
    bm25_retriever.k = top_k

    ensemble: EnsembleRetriever = EnsembleRetriever(
        retrievers=[dense_retriever, bm25_retriever],
        weights=[dense_weight, bm25_weight],
    )
    logger.info(
        f"✓ Initialized Hybrid EnsembleRetriever (Dense={dense_weight}, "
        f"BM25={bm25_weight}, Top-K={top_k})"
    )
    return ensemble


class LangChainAcademicRAGPipeline:
    """Production-grade Hybrid RAG Pipeline orchestrated with LangChain and LCEL."""

    def __init__(
        self,
        workspace_path: str,
        config: RAGConfig | None = None,
        dense_weight: float = 0.6,
        bm25_weight: float = 0.4,
    ) -> None:
        """Initializes the LangChain hybrid pipeline.

        Args:
            workspace_path: Absolute root path of the project repository.
            config: Optional RAG configuration dataclass.
            dense_weight: Reciprocal Rank Fusion weight for dense vector search.
            bm25_weight: Reciprocal Rank Fusion weight for sparse BM25 search.
        """
        self.workspace_path: str = workspace_path
        self.config: RAGConfig = config or RAGConfig()
        self.dense_weight: float = dense_weight
        self.bm25_weight: float = bm25_weight
        self.registry: DocumentExtractorRegistry = DocumentExtractorRegistry()
        self.documents: list[Document] = []
        self.ensemble_retriever: EnsembleRetriever | None = None

    def discover_knowledge_files(self) -> list[str]:
        """Discovers all supported courseware files in the knowledge base directory.

        Returns:
            list[str]: Sorted list of absolute file paths matching extensions.
        """
        kb_path: str = os.path.join(
            self.workspace_path,
            self.config.knowledge_base_dir,
        )
        return scan_directory_for_extensions(
            base_dir=kb_path,
            supported_extensions=(".pdf", ".pptx", ".ppt"),
        )

    def load_from_chunks(self, chunks: Sequence[DocumentChunk]) -> int:
        """Builds the hybrid ensemble index directly from pre-extracted chunks.

        Args:
            chunks: Sequence of extracted DocumentChunk value objects.

        Returns:
            int: Number of documents loaded into the hybrid index.
        """
        self.documents = [
            convert_chunk_to_langchain_document(chunk) for chunk in chunks
        ]

        if not self.documents:
            logger.warning("No valid chunks provided for LangChain indexing.")
            return 0

        self.ensemble_retriever = create_hybrid_ensemble_retriever(
            documents=self.documents,
            embedding_model_name=self.config.embedding_model_name,
            collection_name=self.config.collection_name + "_langchain",
            dense_weight=self.dense_weight,
            bm25_weight=self.bm25_weight,
            top_k=self.config.default_top_k,
        )
        return len(self.documents)

    def ingest_and_build(self) -> int:
        """Ingests courseware documents and builds the hybrid EnsembleRetriever.

        Returns:
            int: Total number of documents indexed across dense and sparse stores.
        """
        files: list[str] = self.discover_knowledge_files()
        all_chunks: list[DocumentChunk] = []
        current_chunk_idx: int = 0

        for file_path in files:
            chunks = self.registry.extract_from_file(
                file_path=file_path,
                start_chunk_id=current_chunk_idx,
                min_length=self.config.min_chunk_length,
            )
            all_chunks.extend(chunks)
            current_chunk_idx += len(chunks)

        return self.load_from_chunks(all_chunks)

    def retrieve_hybrid(
        self,
        query: str,
        top_k: int = 4,
    ) -> list[Document]:
        """Executes Reciprocal Rank Fusion hybrid retrieval (Dense + BM25).

        Args:
            query: Natural language query string.
            top_k: Number of top documents to return.

        Returns:
            list[Document]: Rank-fused list of LangChain Document objects.
        """
        if self.ensemble_retriever is None:
            self.ingest_and_build()

        if self.ensemble_retriever is None:
            return []

        return self.ensemble_retriever.invoke(query)[:top_k]

    def retrieve_formatted_context(
        self,
        query: str,
        top_k: int = 4,
    ) -> str:
        """Retrieves and formats hybrid grounded context blocks.

        Args:
            query: Natural language query string.
            top_k: Number of top documents to return.

        Returns:
            str: Formatted Markdown context with citations.
        """
        matched_docs = self.retrieve_hybrid(query=query, top_k=top_k)
        return format_langchain_documents(matched_docs)


def run_standalone_langchain_demo() -> None:
    """CLI entry point demonstrating LangChain hybrid RAG retrieval."""
    repo_root: str = str(Path(__file__).resolve().parent.parent)
    pipeline: LangChainAcademicRAGPipeline = LangChainAcademicRAGPipeline(
        workspace_path=repo_root
    )
    pipeline.ingest_and_build()

    sample_queries: list[str] = [
        "IEEE 830 functional requirements and NFR metrics",
        "UML Use Case include extend dynamic load balancing",
        "Function point calculation formula UFP VAF COCOMO",
    ]

    for query in sample_queries:
        print(f"\n{'=' * 75}\n🔍 HYBRID QUERY (Dense + BM25): {query}\n{'=' * 75}")
        context = pipeline.retrieve_formatted_context(query=query, top_k=2)
        print(context)


if __name__ == "__main__":
    run_standalone_langchain_demo()
