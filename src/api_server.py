"""Dynamic FastAPI REST API & Interactive Web Dashboard.

Provides interactive REST endpoints for semantic RAG queries, real-time
document uploads with automatic vector indexing, live parameterized sizing
computations, and dynamic PDF/HTML deliverable compilation.
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import Any, Final

import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.dashboard_html import get_dashboard_html
from src.data_modal import (
    COCOMOModel,
    COCOMOResult,
    FPSizingResult,
    ProjectParameters,
    QueryMatch,
    QueryResponse,
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
from src.vector_svgs import get_all_diagrams
from src.watcher import DynamicKnowledgeWatcher

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger: Final[logging.Logger] = logging.getLogger("APIServer")

repo_root: str = str(Path(__file__).resolve().parent.parent)
rag_engine: AcademicRAGPipeline = AcademicRAGPipeline(workspace_path=repo_root)
rag_engine.ingest_knowledge_base()

watcher: DynamicKnowledgeWatcher = DynamicKnowledgeWatcher(rag_pipeline=rag_engine)
watcher.start(non_blocking=True)

app: FastAPI = FastAPI(
    title="Academic RAG Synthesis Engine API",
    description="Dynamic Grounding, Retrieval, and Report Generation Engine",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    """Payload schema for semantic query search."""

    query: str = Field(..., example="IEEE 830 functional requirements and NFR metrics")
    top_k: int = Field(default=4, ge=1, le=20)


class ParameterizedReportRequest(BaseModel):
    """Payload schema for dynamic report synthesis."""

    system_name: str = Field(default="AeroGrid")
    domain: str = Field(default="Autonomous Drone Fleet Traffic Management")
    nfr_latency_p99_ms: int = Field(default=150)
    nfr_availability_pct: float = Field(default=99.999)
    nfr_telemetry_hz: int = Field(default=100)
    ufp_inputs: int = Field(default=6)
    ufp_outputs: int = Field(default=5)
    ufp_inquiries: int = Field(default=4)
    ufp_internal_files: int = Field(default=4)
    ufp_external_interfaces: int = Field(default=3)
    complexity_adjustment_factors_sum: int = Field(default=42)
    cocomo_category: str = Field(default="semidetached")
    loc_per_function_point: int = Field(default=53)
    labor_cost_per_person_month_usd: float = Field(default=8500.0)


@app.get("/", response_class=HTMLResponse)
def get_dashboard() -> HTMLResponse:
    """Serves the dynamic single-page dashboard."""
    return HTMLResponse(content=get_dashboard_html())


@app.get("/health")
def get_health() -> dict[str, Any]:
    """Returns the live status of the RAG vector index and watcher daemon."""
    return {
        "status": "online",
        "total_indexed_chunks": rag_engine.indexed_chunks_count,
        "embedding_model": rag_engine.config.embedding_model_name,
        "collection": rag_engine.config.collection_name,
    }


@app.post("/api/query", response_model=QueryResponse)
def query_rag(request: QueryRequest) -> QueryResponse:
    """Executes semantic cosine-similarity retrieval against ChromaDB."""
    matches_raw = rag_engine.retrieve(query=request.query, top_k=request.top_k)
    matches_list: list[QueryMatch] = [
        QueryMatch(
            content=str(m["content"]),
            source=str(m["source"]),
            page_or_slide=int(m["page_or_slide"]),
            doc_type=str(m["doc_type"]),
        )
        for m in matches_raw
    ]
    formatted_context: str = rag_engine.retrieve_context(
        query=request.query,
        top_k=request.top_k,
    )
    return QueryResponse(
        query=request.query,
        matches=matches_list,
        formatted_context=formatted_context,
        total_indexed_chunks=rag_engine.indexed_chunks_count,
    )


@app.post("/api/upload")
def upload_document(file: UploadFile) -> dict[str, Any]:
    """Uploads a new course PDF/PPTX and incrementally indexes it into ChromaDB."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename missing")

    dest_dir: str = os.path.join(rag_engine.workspace_path, "knowledge_base", "uploads")
    os.makedirs(dest_dir, exist_ok=True)
    dest_path: str = os.path.join(dest_dir, file.filename)

    content: bytes = file.file.read()
    with open(dest_path, "wb") as f:
        f.write(content)

    chunks = rag_engine.registry.extract_from_file(
        file_path=dest_path,
        start_chunk_id=rag_engine.indexed_chunks_count,
        min_length=rag_engine.config.min_chunk_length,
    )
    indexed_now = rag_engine.add_chunks_to_index(chunks) if chunks else 0

    return {
        "filename": file.filename,
        "file_size_bytes": len(content),
        "chunks_indexed": indexed_now,
        "total_active_chunks": rag_engine.indexed_chunks_count,
    }


@app.post("/api/generate-report")
def generate_custom_report(request: ParameterizedReportRequest) -> dict[str, Any]:
    """Dynamically computes FP/COCOMO metrics, synthesizes markdown,
    and compiles PDF deliverables.
    """
    try:
        cocomo_enum = COCOMOModel(request.cocomo_category.lower())
    except ValueError:
        cocomo_enum = COCOMOModel.SEMIDETACHED

    params = ProjectParameters(
        system_name=request.system_name,
        domain=request.domain,
        nfr_latency_p99_ms=request.nfr_latency_p99_ms,
        nfr_availability_pct=request.nfr_availability_pct,
        nfr_telemetry_hz=request.nfr_telemetry_hz,
        ufp_inputs=request.ufp_inputs,
        ufp_outputs=request.ufp_outputs,
        ufp_inquiries=request.ufp_inquiries,
        ufp_internal_files=request.ufp_internal_files,
        ufp_external_interfaces=request.ufp_external_interfaces,
        complexity_adjustment_factors_sum=request.complexity_adjustment_factors_sum,
        cocomo_category=cocomo_enum,
        loc_per_function_point=request.loc_per_function_point,
        labor_cost_per_person_month_usd=request.labor_cost_per_person_month_usd,
    )

    fp_res: FPSizingResult = compute_function_points(params)
    cocomo_res: COCOMOResult = compute_cocomo_metrics(
        kloc=fp_res.derived_kloc,
        mode=params.cocomo_category,
        labor_rate_usd=params.labor_cost_per_person_month_usd,
    )

    citations: dict[str, str] = {
        "task1": str(
            rag_engine.retrieve(
                "IEEE 830 requirements functional non-functional", top_k=1
            )[0]["source"]
        ),
        "task2": str(
            rag_engine.retrieve("use case activity diagram modeling", top_k=1)[0][
                "source"
            ]
        ),
        "task3": str(
            rag_engine.retrieve("4+1 architectural view microservices", top_k=1)[0][
                "source"
            ]
        ),
        "task4": str(
            rag_engine.retrieve("function points cocomo estimation", top_k=1)[0][
                "source"
            ]
        ),
    }

    dynamic_md = synthesize_dynamic_report_markdown(
        params=params,
        fp_result=fp_res,
        cocomo_result=cocomo_res,
        rag_citations=citations,
    )

    out_dir = os.path.join(repo_root, "output")
    os.makedirs(out_dir, exist_ok=True)
    clean_name = params.system_name.replace(" ", "_")
    html_out = os.path.join(out_dir, f"{clean_name}_Dynamic.html")
    pdf_out = os.path.join(out_dir, f"{clean_name}_Dynamic.pdf")

    processed_md, _ = DiagramProcessor.replace_mermaid_with_placeholders(dynamic_md)
    renderer = MarkdownDocumentRenderer(page_size="A4")
    body_html = renderer.render_body(processed_md)
    body_with_svgs = DiagramProcessor.inject_vector_svgs(body_html, get_all_diagrams())
    full_html = renderer.wrap_html_template(
        body_with_svgs, f"{params.system_name} - Dynamic Solution"
    )

    with open(html_out, "w", encoding="utf-8") as f:
        f.write(full_html)

    compiler = HeadlessPDFCompiler()
    pdf_success = compiler.compile_pdf(
        html_path=html_out, pdf_path=pdf_out, virtual_time_budget_ms=9000
    )
    pdf_size_kb = (
        round(os.path.getsize(pdf_out) / 1024.0, 1)
        if pdf_success and os.path.exists(pdf_out)
        else 0.0
    )

    return {
        "success": pdf_success,
        "system_name": params.system_name,
        "fp_sizing": {
            "unadjusted_function_points": fp_res.unadjusted_function_points,
            "value_adjustment_factor": fp_res.value_adjustment_factor,
            "adjusted_function_points": fp_res.adjusted_function_points,
            "derived_kloc": fp_res.derived_kloc,
        },
        "cocomo_estimation": {
            "effort_person_months": cocomo_res.effort_person_months,
            "development_time_months": cocomo_res.development_time_months,
            "average_staff_size": cocomo_res.average_staff_size,
            "estimated_total_cost_usd": cocomo_res.estimated_total_cost_usd,
            "productivity_loc_per_pm": cocomo_res.productivity_loc_per_pm,
        },
        "pdf_download_url": f"/api/download/{os.path.basename(pdf_out)}",
        "html_download_url": f"/api/download/{os.path.basename(html_out)}",
        "pdf_size_kb": pdf_size_kb,
    }


@app.get("/api/download/{filename}")
def download_artifact(filename: str) -> FileResponse:
    """Downloads a compiled PDF or HTML deliverable artifact."""
    file_path = os.path.join(repo_root, "output", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File artifact not found")
    return FileResponse(file_path, filename=filename)


def run_api_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    """Launches the Uvicorn ASGI server."""
    logger.info(f"🚀 Starting Academic RAG Server on http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_api_server()
