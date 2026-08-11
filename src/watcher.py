"""Dynamic Knowledge Base File Watcher & Incremental Ingestion Daemon.

Monitors the courseware directory for newly added or modified slide decks and
rubric PDFs, immediately extracting and incrementally indexing them into the
live ChromaDB vector database in real time.
"""

from __future__ import annotations

import logging
import os
import sys
import time
from pathlib import Path
from typing import Final

from pypdf.errors import PyPdfError
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.rag_pipeline import AcademicRAGPipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger: Final[logging.Logger] = logging.getLogger("KnowledgeWatcher")


class KnowledgeBaseChangeHandler(FileSystemEventHandler):
    """Event handler for monitoring courseware file creation and modifications."""

    def __init__(self, rag_pipeline: AcademicRAGPipeline) -> None:
        """Initializes the change handler with an active RAG pipeline instance.

        Args:
            rag_pipeline: Target AcademicRAGPipeline instance for incremental indexing.
        """
        super().__init__()
        self.pipeline: AcademicRAGPipeline = rag_pipeline
        self._supported_exts: tuple[str, ...] = (".pdf", ".pptx", ".ppt")

    def _is_supported_file(self, path: str) -> bool:
        """Checks if the file extension is supported for ingestion.

        Args:
            path: Target file path.

        Returns:
            bool: True if supported format, False otherwise.
        """
        return path.lower().endswith(self._supported_exts)

    def on_created(self, event: FileSystemEvent) -> None:
        """Triggered when a new document is added to the watched knowledge base.

        Args:
            event: File system event descriptor.
        """
        if event.is_directory or not self._is_supported_file(event.src_path):
            return

        logger.info(f"✨ New document detected: {os.path.basename(event.src_path)}")
        self._ingest_file(event.src_path)

    def on_modified(self, event: FileSystemEvent) -> None:
        """Triggered when an existing document is updated.

        Args:
            event: File system event descriptor.
        """
        if event.is_directory or not self._is_supported_file(event.src_path):
            return

        logger.info(f"🔄 Document modified: {os.path.basename(event.src_path)}")
        self._ingest_file(event.src_path)

    def _ingest_file(self, file_path: str) -> None:
        """Extracts and adds chunks from a single document into the active vector index.

        Args:
            file_path: Absolute path to the changed file.
        """
        try:
            chunks = self.pipeline.registry.extract_from_file(
                file_path=file_path,
                start_chunk_id=self.pipeline.indexed_chunks_count,
                min_length=self.pipeline.config.min_chunk_length,
            )
            if chunks:
                added = self.pipeline.add_chunks_to_index(chunks)
                logger.info(
                    f"✓ Incrementally indexed {added} chunks from "
                    f"{os.path.basename(file_path)}. Total: "
                    f"{self.pipeline.indexed_chunks_count}"
                )
        except (PyPdfError, KeyError, ValueError, OSError) as err:
            logger.error(f"Failed to incrementally index {file_path}: {err}")


class DynamicKnowledgeWatcher:
    """Manages background directory monitoring and thread lifecycle."""

    def __init__(
        self,
        rag_pipeline: AcademicRAGPipeline,
        watch_directory: str | None = None,
    ) -> None:
        """Initializes the watcher service.

        Args:
            rag_pipeline: Active RAG pipeline.
            watch_directory: Target path to monitor (defaults to knowledge_base).
        """
        self.pipeline: AcademicRAGPipeline = rag_pipeline
        self.watch_dir: str = watch_directory or os.path.join(
            self.pipeline.workspace_path,
            self.pipeline.config.knowledge_base_dir,
        )
        self.observer: Observer = Observer()
        self.handler: KnowledgeBaseChangeHandler = KnowledgeBaseChangeHandler(
            rag_pipeline=self.pipeline
        )

    def start(self, non_blocking: bool = False) -> None:
        """Starts monitoring the knowledge base directory.

        Args:
            rag_pipeline: Boolean flag. If False, enters continuous sleep loop.
        """
        os.makedirs(self.watch_dir, exist_ok=True)
        self.observer.schedule(self.handler, path=self.watch_dir, recursive=True)
        self.observer.start()
        logger.info(f"👀 Live Document Watcher active on: {self.watch_dir}")

        if not non_blocking:
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.stop()

    def stop(self) -> None:
        """Stops the file system observer and joins the background thread."""
        logger.info("Stopping Knowledge Base Watcher...")
        self.observer.stop()
        self.observer.join()


def run_standalone_watcher() -> None:
    """CLI entry point for running the file watcher service."""
    repo_root: str = str(Path(__file__).resolve().parent.parent)
    pipeline: AcademicRAGPipeline = AcademicRAGPipeline(workspace_path=repo_root)
    pipeline.ingest_knowledge_base()

    watcher: DynamicKnowledgeWatcher = DynamicKnowledgeWatcher(rag_pipeline=pipeline)
    watcher.start(non_blocking=False)


if __name__ == "__main__":
    run_standalone_watcher()
