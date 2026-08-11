# 🏗️ Academic RAG Synthesis Engine: End-to-End System Architecture

**Author**: Arabindaksha Mishra (`mishraarabinda02@gmail.com`)  
**Scope**: Complete Technical Description of Repository Architecture, Components, and Data Flow  

---

## 1. What Exactly Did We Build?

We built a modular, production-grade **Academic Multi-Modal RAG Platform & Parameterized Sizing Engine** designed to synthesize technically grounded software engineering assignment specifications and publication-grade deliverables.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    END-TO-END PIPELINE ARCHITECTURAL STACK                                  │
├─────────────────────────┬──────────────────────────┬──────────────────────────┬─────────────────────────────┤
│ 1. Multi-Modal Parsing  │ 2. Dual Vector Index     │ 3. Hybrid RRF Retrieval  │ 4. Deterministic Sizing     │
│ • PDFExtractor (pypdf)  │ • Dense: ChromaDB        │ • LangChain Ensemble     │ • IFPUG Function Points     │
│ • PPTXExtractor (pptx)  │ • Sparse: BM25 Lexical   │ • 60% Dense + 40% Sparse │ • Basic COCOMO Equations    │
├─────────────────────────┼──────────────────────────┼──────────────────────────┼─────────────────────────────┤
│ 5. Live File Watcher    │ 6. Vector SVG Graphics   │ 7. Headless Publishing   │ 8. Interactive Interfaces   │
│ • OS inotify (watchdog) │ • Scalable UML 2.5 SVGs  │ • Chrome Headless PDF    │ • FastAPI REST API (:8000)  │
│ • Incremental Indexing  │ • Zero JS layout crash   │ • MathJax 3 LaTeX Engine │ • Responsive SPA Dashboard  │
└─────────────────────────┴──────────────────────────┴──────────────────────────┴─────────────────────────────┘
```

---

## 2. Core Modules & Component Breakdown

```text
src/
├── __init__.py          # Unified package root with sorted exports
├── data_modal.py        # 📦 Immutable domain dataclasses (DocumentChunk, ProjectParameters, BuildResult)
├── data_parser.py       # 📄 Multi-modal extraction strategies (PDFExtractor, PPTXExtractor, Registry)
├── rag_pipeline.py      # 🔍 Dense vector database (ChromaDB + all-MiniLM-L6-v2)
├── langchain_pipeline.py# 🔀 Hybrid Ensemble Retriever (Dense Chroma + Sparse BM25 via RRF)
├── synthesis_engine.py  # ⚙️ Deterministic mathematical calculator (Function Points & COCOMO)
├── watcher.py           # 👁️ Live directory watcher for automatic incremental indexing (watchdog)
├── vector_svgs.py       # 🎨 High-resolution UML 2.5 vector SVG diagram library
├── utils.py             # 🛠️ Markdown renderer, MathJax templating & Headless Chrome compiler
├── api_server.py        # 🚀 FastAPI REST server with asynchronous endpoints
└── dashboard_html.py    # 💻 Single-page application (SPA) web interface template
```

---

## 3. Detailed Data Flow Step-by-Step

### Step 1: Multi-Modal Ingestion & Strategy Pattern ([src/data_parser.py](file:///usr/local/google/home/arabindaksha/academic-rag-synthesis-engine/src/data_parser.py))
* **Strategy Interface (`BaseDocumentExtractor`)**: Defines `can_handle(file_path)` and `extract_chunks(...)`.
* **PDF Engine (`PDFExtractor`)**: Slices PDFs page-by-page using `pypdf`.
* **PPTX Engine (`PPTXExtractor`)**: Traverses XML shape trees, extracting text runs from shapes, tables, and notes using `python-pptx`.
* **Registry (`DocumentExtractorRegistry`)**: Dispatches files to the appropriate extractor with automatic format fallback.
* **Output**: **551 atomically complete knowledge chunks** carrying rich metadata tuples (`source`, `slide_or_page`, `doc_type`).

---

### Step 2: Dual-Engine Vector Indexing & Hybrid Search ([src/langchain_pipeline.py](file:///usr/local/google/home/arabindaksha/academic-rag-synthesis-engine/src/langchain_pipeline.py))
* **Dense Embedding**: `sentence-transformers/all-MiniLM-L6-v2` embeds all chunks into a 384-dimensional continuous latent space in **ChromaDB**.
* **Sparse Lexical Index**: `BM25Retriever` indexes exact keywords for precise acronym and code lookups (`"FR-01"`, `"NFR-02"`, `"COCOMO"`).
* **Hybrid Fusion**: LangChain's `EnsembleRetriever` merges both search results using **Reciprocal Rank Fusion (RRF)**:
  $$\text{RRF}(d) = \frac{0.6}{60 + r_{\text{Dense}}(d)} + \frac{0.4}{60 + r_{\text{BM25}}(d)}$$

---

### Step 3: Parameterized Sizing & Formula Sizing ([src/synthesis_engine.py](file:///usr/local/google/home/arabindaksha/academic-rag-synthesis-engine/src/synthesis_engine.py))
Instead of leaving math to an LLM, pure Python functions calculate software metrics deterministically:
* **Function Point Analysis (IFPUG)**:
  $$\text{UFP} = (EI \times 4) + (EO \times 5) + (EQ \times 4) + (ILF \times 10) + (EIF \times 7)$$
  $$\text{VAF} = 0.65 + (0.01 \times \sum TDI)$$
  $$\text{AFP} = \text{UFP} \times \text{VAF}, \quad \text{Derived KLOC} = \frac{\text{AFP} \times \text{LOC/FP}}{1000}$$
* **Basic COCOMO Estimation**:
  $$\text{Effort (PM)} = a \times (\text{KLOC})^b, \quad T_{dev} = c \times (\text{Effort})^d, \quad \text{Staff} = \frac{\text{Effort}}{T_{dev}}$$

---

### Step 4: High-Resolution Vector SVG Graphics ([src/vector_svgs.py](file:///usr/local/google/home/arabindaksha/academic-rag-synthesis-engine/src/vector_svgs.py))
* Replaces fragile client-side JavaScript diagramming (Mermaid) with **deterministic inline Vector SVGs**.
* Generates 5 crisp, scalable diagrams:
  1. System Context Diagram
  2. UML 2.5 Use Case Diagram (`«include»`, `«extend»`)
  3. Dynamic Load Balancing Activity Diagram
  4. Logical View Domain Class Model
  5. 4+1 Microservices & Kafka Component Architecture

---

### Step 5: Headless Google Chrome PDF Compilation ([src/utils.py](file:///usr/local/google/home/arabindaksha/academic-rag-synthesis-engine/src/utils.py))
* Injects MathJax 3 for mathematical equation rendering.
* Applies CSS `@page { size: A4; margin: 20mm 16mm; }` paged media rules.
* Invokes `google-chrome --headless=new --virtual-time-budget=9000` to ensure complete MathJax LaTeX rendering prior to print snapshotting.

---

### Step 6: Real-Time File Watcher Daemon ([src/watcher.py](file:///usr/local/google/home/arabindaksha/academic-rag-synthesis-engine/src/watcher.py))
* Uses `watchdog` to monitor `knowledge_base/` for newly dropped or updated lecture decks.
* Incrementally extracts and embeds new chunks in $< 300\text{ ms}$ without restarting the system.

---

### Step 7: FastAPI REST API & Single-Page Dashboard ([src/api_server.py](file:///usr/local/google/home/arabindaksha/academic-rag-synthesis-engine/src/api_server.py))
* Serves a responsive web interface at `http://localhost:8000/`.
* Exposes REST endpoints for live hybrid querying (`/api/query`), document upload (`/api/upload`), dynamic report generation (`/api/generate-report`), and artifact download (`/api/download/{filename}`).

---

## 4. Execution & Quickstart

```bash
# 1. Start Interactive Web Dashboard & REST API
python3 src/api_server.py

# 2. Run Standalone LangChain Hybrid Retrieval (CLI)
python3 src/langchain_pipeline.py

# 3. Compile Master Solution Deliverables (CLI)
python3 src/build_solution.py
```

---
*System Architecture Specification — Academic RAG Synthesis Engine.*
