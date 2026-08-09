"""Multi-Modal Academic RAG Pipeline.

BITS Pilani WILP - Software Engineering Coursework Grounding Engine.
Coordinates document ingestion from the knowledge base, dense vector embeddings,
and semantic context retrieval using ChromaDB.
"""

from __future__ import annotations

import glob
import logging
import os
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any, Final

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import chromadb
from chromadb.api.models.Collection import Collection
from chromadb.utils import embedding_functions

from src.data_modal import DocumentChunk, RAGConfig
from src.data_parser import (
    DocumentExtractorRegistry,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger: Final[logging.Logger] = logging.getLogger("AcademicRAGPipeline")


def format_citation_block(
    source_file: str,
    page_or_slide: int,
    content: str,
) -> str:
    """Helper function to format a grounded Markdown context citation block.

    Args:
        source_file: Name of the originating document.
        page_or_slide: Page or slide number.
        content: Text content of the chunk.

    Returns:
        str: Formatted Markdown heading and citation block.
    """
    return f"### [Source: {source_file} | Page/Slide: {page_or_slide}]\n{content}"


def get_default_course_tasks() -> dict[str, str]:
    """Helper function returning standard curriculum evaluation benchmark queries.

    Returns:
        dict[str, str]: Task titles mapped to natural language search queries.
    """
    return {
        "Task 1: IEEE 830 Requirements Grounding": (
            "IEEE 830 standard requirements specification functional "
            "requirements non-functional metrics"
        ),
        "Task 2: Behavioral & Activity Modeling": (
            "Use case diagram actors relationships activity diagram "
            "dynamic load balancing 85% threshold"
        ),
        "Task 3: 4+1 View & Microservices Architecture": (
            "4+1 architectural view model logical view class diagram "
            "microservices event-driven kafka"
        ),
        "Task 4: Function Points & COCOMO Sizing": (
            "Function point calculation formula UFP VAF complexity "
            "multipliers basic COCOMO effort person-months"
        ),
    }


def scan_directory_for_extensions(
    base_dir: str,
    supported_extensions: tuple[str, ...],
) -> list[str]:
    """Helper function to recursively search for files with target extensions.

    Args:
        base_dir: Root directory to scan.
        supported_extensions: Tuple of lower-case file extensions.

    Returns:
        list[str]: Sorted list of matching file paths.
    """
    search_paths: list[str] = [
        os.path.join(base_dir, "**", "*.*"),
        os.path.join(base_dir, "*.*"),
    ]
    discovered: list[str] = []
    for pattern in search_paths:
        discovered.extend(glob.glob(pattern, recursive=True))

    return sorted({f for f in discovered if f.lower().endswith(supported_extensions)})


def unpack_query_results(
    raw_results: dict[str, Any],
) -> list[dict[str, str | int]]:
    """Helper function to extract and normalize matches from ChromaDB query output.

    Args:
        raw_results: Raw dictionary returned by collection.query().

    Returns:
        list[dict[str, Union[str, int]]]: Structured matches list.
    """
    matches: list[dict[str, str | int]] = []
    if raw_results and raw_results.get("documents") and raw_results.get("metadatas"):
        docs: list[str] = raw_results["documents"][0]
        metas: list[dict[str, Any]] = raw_results["metadatas"][0]
        for doc, meta in zip(docs, metas):
            matches.append(
                {
                    "content": str(doc),
                    "source": str(meta.get("source", "unknown")),
                    "page_or_slide": int(meta.get("slide_or_page", 1)),
                    "doc_type": str(meta.get("doc_type", "document")),
                }
            )
    return matches


class AcademicRAGPipeline:
    """End-to-End Multi-Modal Academic RAG Pipeline.

    Provides modular, loosely coupled document indexing, vector embedding,
    and cosine-similarity semantic retrieval grounded in academic course materials.
    """

    def __init__(
        self,
        workspace_path: str,
        config: RAGConfig | None = None,
        extractor_registry: DocumentExtractorRegistry | None = None,
    ) -> None:
        """Initializes the RAG Pipeline and in-memory ChromaDB vector store.

        Args:
            workspace_path: Root directory path of the project.
            config: Optional RAG configuration parameters.
            extractor_registry: Optional document extractor registry strategy.
        """
        self.workspace_path: str = os.path.abspath(workspace_path)
        self.config: RAGConfig = config or RAGConfig()
        self.registry: DocumentExtractorRegistry = (
            extractor_registry or DocumentExtractorRegistry()
        )

        self.client: chromadb.ClientAPI = chromadb.Client()
        self.embedding_fn: embedding_functions.SentenceTransformerEmbeddingFunction = (
            embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=self.config.embedding_model_name
            )
        )
        self.collection: Collection = self.client.create_collection(
            name=self.config.collection_name,
            embedding_function=self.embedding_fn,
        )
        self.indexed_chunks_count: int = 0

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

    def add_chunks_to_index(self, chunks: Sequence[DocumentChunk]) -> int:
        """Batches and inserts document chunks into the ChromaDB collection.

        Args:
            chunks: Sequence of DocumentChunk instances to persist.

        Returns:
            int: Total number of chunks successfully added.
        """
        if not chunks:
            return 0

        documents_list: list[str] = [chunk.content for chunk in chunks]
        metadatas_list: list[dict[str, str | int]] = [
            chunk.to_metadata() for chunk in chunks
        ]
        ids_list: list[str] = [chunk.chunk_id for chunk in chunks]

        self.collection.add(
            documents=documents_list,
            metadatas=metadatas_list,
            ids=ids_list,
        )
        self.indexed_chunks_count += len(chunks)
        return len(chunks)

    def ingest_knowledge_base(self) -> int:
        """Executes full automated ingestion across all discovered course documents.

        Returns:
            int: Total number of chunks indexed into ChromaDB.
        """
        target_files: list[str] = self.discover_knowledge_files()
        logger.info(
            f"Discovered {len(target_files)} knowledge base files in "
            f"{self.config.knowledge_base_dir}"
        )

        total_chunks: int = 0
        for file_path in target_files:
            chunks: list[DocumentChunk] = self.registry.extract_from_file(
                file_path=file_path,
                start_chunk_id=total_chunks,
                min_length=self.config.min_chunk_length,
            )
            if chunks:
                self.add_chunks_to_index(chunks)
                total_chunks += len(chunks)

        logger.info(
            f"✓ Indexed {self.indexed_chunks_count} knowledge chunks into ChromaDB."
        )
        return self.indexed_chunks_count

    def ingest_all(self) -> int:
        """Backward-compatible wrapper for ingest_knowledge_base().

        Returns:
            int: Total count of indexed chunks.
        """
        return self.ingest_knowledge_base()

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
    ) -> list[dict[str, str | int]]:
        """Queries ChromaDB for the top-k semantically nearest knowledge chunks.

        Args:
            query: Natural language query string.
            top_k: Optional count of top results (defaults to config.default_top_k).

        Returns:
            list[dict[str, Union[str, int]]]: Structured list of matches.
        """
        k: int = top_k or self.config.default_top_k
        raw_results: dict[str, Any] = self.collection.query(
            query_texts=[query],
            n_results=k,
        )
        return unpack_query_results(raw_results=raw_results)

    def retrieve_context(
        self,
        query: str,
        top_k: int | None = None,
    ) -> str:
        """Retrieves formatted Markdown context blocks for prompt augmentation.

        Args:
            query: Natural language search query.
            top_k: Number of chunks to retrieve.

        Returns:
            str: Formatted Markdown string with source citations.
        """
        matches: list[dict[str, str | int]] = self.retrieve(
            query=query,
            top_k=top_k,
        )
        context_blocks: list[str] = [
            format_citation_block(
                source_file=str(match["source"]),
                page_or_slide=int(match["page_or_slide"]),
                content=str(match["content"]),
            )
            for match in matches
        ]
        return "\n\n".join(context_blocks)


def run_pipeline_demo() -> None:
    """Executes a diagnostic demonstration of the Academic RAG Pipeline."""
    current_dir: str = os.path.dirname(os.path.abspath(__file__))
    repo_root: str = (
        os.path.abspath(os.path.join(current_dir, ".."))
        if os.path.basename(current_dir) == "src"
        else current_dir
    )

    rag: AcademicRAGPipeline = AcademicRAGPipeline(workspace_path=repo_root)
    rag.ingest_knowledge_base()

    tasks: dict[str, str] = get_default_course_tasks()

    print("\n" + "=" * 80)
    print("RAG DEMONSTRATION: RETRIEVING GROUNDED KNOWLEDGE CHUNKS")
    print("=" * 80)

    for task_name, query_text in tasks.items():
        print(f"\n==================== {task_name} ====================")
        retrieved_context: str = rag.retrieve_context(query_text, top_k=2)
        print(retrieved_context[:500] + "\n...\n")


if __name__ == "__main__":
    run_pipeline_demo()
