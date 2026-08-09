#!/usr/bin/env python3
"""
Multi-Modal Academic RAG Pipeline (Production Engine)
BITS Pilani WILP - Software Engineering Coursework Engine
Parses PDFs, presentation slides (PPTX), and curriculum modules into ChromaDB with semantic retrieval.
"""

import os
import glob
from typing import List, Dict
from pypdf import PdfReader
from pptx import Presentation
import chromadb
from chromadb.utils import embedding_functions

class AcademicRAGPipeline:
    def __init__(self, workspace_path: str):
        self.workspace_path = workspace_path
        self.client = chromadb.Client()
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.collection = self.client.create_collection(
            name="se_academic_knowledge_base",
            embedding_function=self.embedding_fn
        )
        self.indexed_chunks = 0

    def _extract_from_pptx(self, file_path: str, filename: str, start_id: int) -> int:
        """Extracts text slide-by-slide from presentation files."""
        prs = Presentation(file_path)
        doc_id = start_id
        for slide_idx, slide in enumerate(prs.slides):
            text_runs = []
            for shape in slide.shapes:
                if shape.has_text_frame:
                    for paragraph in shape.text_frame.paragraphs:
                        text_runs.append(paragraph.text)
            full_text = "\n".join([t.strip() for t in text_runs if t.strip()])
            if len(full_text) > 20:
                self.collection.add(
                    documents=[full_text],
                    metadatas=[{
                        "source": filename,
                        "slide_or_page": slide_idx + 1,
                        "doc_type": "presentation_slide"
                    }],
                    ids=[f"chunk_{doc_id}"]
                )
                doc_id += 1
        return doc_id

    def _extract_from_pdf(self, file_path: str, filename: str, start_id: int) -> int:
        """Extracts text page-by-page from PDF documents."""
        reader = PdfReader(file_path)
        doc_id = start_id
        for page_idx, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and len(text.strip()) > 30:
                self.collection.add(
                    documents=[text.strip()],
                    metadatas=[{
                        "source": filename,
                        "slide_or_page": page_idx + 1,
                        "doc_type": "pdf_document"
                    }],
                    ids=[f"chunk_{doc_id}"]
                )
                doc_id += 1
        return doc_id

    def ingest_all(self):
        """Scans knowledge_base/ directory (course slides and rubrics) for multi-format knowledge ingestion."""
        search_patterns = [
            os.path.join(self.workspace_path, "knowledge_base", "**", "*.*"),
            os.path.join(self.workspace_path, "**", "*.*") if not os.path.exists(os.path.join(self.workspace_path, "knowledge_base")) else os.path.join(self.workspace_path, "knowledge_base", "*.*")
        ]
        
        all_files = []
        for pat in search_patterns:
            all_files.extend(glob.glob(pat, recursive=True))

        supported_exts = [".pdf", ".pptx", ".ppt"]
        target_files = [f for f in sorted(list(set(all_files))) if any(f.endswith(ext) for ext in supported_exts)]
        
        doc_id = 0
        for file_path in target_files:
            filename = os.path.basename(file_path)
            # Try PPTX first (supports PPTX files saved as .pdf/.ppt)
            try:
                doc_id = self._extract_from_pptx(file_path, filename, doc_id)
                continue
            except Exception:
                pass
            
            # Try PDF extraction
            try:
                doc_id = self._extract_from_pdf(file_path, filename, doc_id)
                continue
            except Exception:
                pass

        self.indexed_chunks = doc_id
        print(f"✓ Successfully indexed {self.indexed_chunks} knowledge chunks across {len(target_files)} source files!")

    def retrieve_context(self, query: str, top_k: int = 4) -> str:
        """Retrieves top-k relevant knowledge chunks for grounding."""
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        context_blocks = []
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            context_blocks.append(
                f"### [Source: {meta['source']} | Page/Slide: {meta['slide_or_page']}]\n{doc}"
            )
        return "\n\n".join(context_blocks)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Resolve repository root
    repo_root = os.path.abspath(os.path.join(current_dir, "..")) if os.path.basename(current_dir) == "src" else current_dir
    rag = AcademicRAGPipeline(repo_root)
    rag.ingest_all()

    tasks = {
        "Task 1: IEEE 830 Requirements Grounding": "IEEE 830 standard requirements specification functional requirements non-functional metrics",
        "Task 2: Behavioral & Activity Modeling": "Use case diagram actors relationships activity diagram dynamic load balancing 85% threshold",
        "Task 3: 4+1 View & Microservices Architecture": "4+1 architectural view model logical view class diagram microservices event-driven kafka",
        "Task 4: Function Points & COCOMO Sizing": "Function point calculation formula UFP VAF complexity multipliers basic COCOMO effort person-months"
    }

    print("\n" + "="*80)
    print("RAG DEMONSTRATION: RETRIEVING GROUNDED KNOWLEDGE CHUNKS")
    print("="*80)

    for task_name, query in tasks.items():
        print(f"\n==================== {task_name} ====================")
        retrieved = rag.retrieve_context(query, top_k=2)
        print(retrieved[:500] + "\n...\n")
