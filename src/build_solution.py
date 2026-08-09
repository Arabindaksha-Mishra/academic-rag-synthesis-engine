"""Solution Deliverable & Report Builder Engine.

Coordinates Markdown rendering, SVG diagram injection, and publication-grade
A4 PDF generation via headless Google Chrome.
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import Final

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data_modal import BuilderConfig, BuildResult
from src.utils import (
    DiagramProcessor,
    HeadlessPDFCompiler,
    MarkdownDocumentRenderer,
)
from src.vector_svgs import (
    get_all_diagrams,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger: Final[logging.Logger] = logging.getLogger("SolutionBuilder")


def read_text_file(file_path: str) -> str:
    """Reads UTF-8 text content from a file path.

    Args:
        file_path: Target file path.

    Returns:
        str: Decoded file content.
    """
    with open(file_path, "r", encoding="utf-8") as file_handle:
        return file_handle.read()


def write_text_file(file_path: str, content: str) -> None:
    """Writes a text string to a target destination file path.

    Args:
        file_path: Destination file path.
        content: UTF-8 text string to write.
    """
    with open(file_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(content)


def compute_file_size_kb(file_path: str) -> float:
    """Computes file size in kilobytes.

    Args:
        file_path: Target file path.

    Returns:
        float: File size in KB, or 0.0 if file is missing.
    """
    if os.path.exists(file_path):
        return os.path.getsize(file_path) / 1024.0
    return 0.0


def render_markdown_with_svgs(
    raw_markdown: str,
    renderer: MarkdownDocumentRenderer,
    svg_diagrams: list[str],
) -> str:
    """Processes Markdown text, substitutes diagrams, and renders HTML body.

    Args:
        raw_markdown: Input Markdown source text.
        renderer: Initialized MarkdownDocumentRenderer instance.
        svg_diagrams: Ordered list of SVG diagram XML strings.

    Returns:
        str: HTML body markup with injected vector diagrams.
    """
    processed_md, count = DiagramProcessor.replace_mermaid_with_placeholders(
        markdown_content=raw_markdown
    )
    logger.info(f"Replaced {count} Mermaid blocks with vector SVG placeholders.")

    body_html: str = renderer.render_body(processed_md)
    return DiagramProcessor.inject_vector_svgs(
        html_content=body_html,
        svg_list=svg_diagrams,
    )


def generate_html_document(
    md_path: str,
    html_path: str,
    renderer: MarkdownDocumentRenderer,
    document_title: str,
) -> bool:
    """Compiles a Markdown file into a formatted HTML document artifact.

    Args:
        md_path: Path to the input Markdown source file.
        html_path: Destination path for the output HTML file.
        renderer: Document renderer instance.
        document_title: HTML title tag string.

    Returns:
        bool: True if HTML generation succeeded, False otherwise.
    """
    if not os.path.exists(md_path):
        logger.error(f"Source Markdown file not found at: {md_path}")
        return False

    raw_markdown: str = read_text_file(md_path)
    svg_diagrams: list[str] = get_all_diagrams()
    body_with_svgs: str = render_markdown_with_svgs(
        raw_markdown=raw_markdown,
        renderer=renderer,
        svg_diagrams=svg_diagrams,
    )

    full_html: str = renderer.wrap_html_template(
        body_html=body_with_svgs,
        document_title=document_title,
    )
    write_text_file(html_path, full_html)
    logger.info(f"✓ Formatted HTML compiled at: {html_path}")
    return True


def export_pdf_document(
    compiler: HeadlessPDFCompiler,
    html_path: str,
    pdf_path: str,
    virtual_time_budget_ms: int,
) -> tuple[bool, float]:
    """Compiles an HTML file into a high-resolution PDF document.

    Args:
        compiler: HeadlessPDFCompiler instance.
        html_path: Source HTML file path.
        pdf_path: Destination PDF file path.
        virtual_time_budget_ms: JavaScript wait budget in milliseconds.

    Returns:
        tuple[bool, float]: Success flag and generated file size in KB.
    """
    success: bool = compiler.compile_pdf(
        html_path=html_path,
        pdf_path=pdf_path,
        virtual_time_budget_ms=virtual_time_budget_ms,
    )
    size_kb: float = compute_file_size_kb(pdf_path) if success else 0.0
    return success, size_kb


class SolutionBuilder:
    """Coordinates document rendering, diagram injection, and compilation."""

    def __init__(self, config: BuilderConfig | None = None) -> None:
        """Initializes the solution builder with configuration parameters.

        Args:
            config: Optional BuilderConfig instance.
        """
        self.config: BuilderConfig = config or BuilderConfig()
        self.renderer: MarkdownDocumentRenderer = MarkdownDocumentRenderer(
            page_size=self.config.page_size
        )
        self.pdf_compiler: HeadlessPDFCompiler = HeadlessPDFCompiler()

    def build(self) -> BuildResult:
        """Executes the complete deliverable build pipeline.

        Returns:
            BuildResult: Detailed results and generated artifact paths.
        """
        os.makedirs(self.config.full_output_dir, exist_ok=True)

        doc_title: str = (
            "AeroGrid - Software Engineering Assignment Report - Arabindaksha Mishra"
        )

        html_created: bool = generate_html_document(
            md_path=self.config.md_path,
            html_path=self.config.html_path,
            renderer=self.renderer,
            document_title=doc_title,
        )
        if not html_created:
            return BuildResult(
                success=False,
                html_path="",
                errors=[f"Markdown file missing: {self.config.md_path}"],
            )

        pdf_success, pdf_size_kb = export_pdf_document(
            compiler=self.pdf_compiler,
            html_path=self.config.html_path,
            pdf_path=self.config.pdf_path,
            virtual_time_budget_ms=self.config.virtual_time_budget_ms,
        )

        return BuildResult(
            success=pdf_success,
            html_path=self.config.html_path,
            pdf_path=self.config.pdf_path if pdf_success else None,
            pdf_size_kb=pdf_size_kb,
        )


def build_perfect_solution() -> None:
    """Top-level execution entry point for compiling deliverables."""
    builder: SolutionBuilder = SolutionBuilder()
    result: BuildResult = builder.build()
    if result.success:
        print(
            f"\n✨ Build Successful! PDF deliverable generated at: "
            f"{result.pdf_path} ({result.pdf_size_kb:.1f} KB)"
        )
    else:
        print(f"\n❌ Build Failed: {result.errors}")


if __name__ == "__main__":
    build_perfect_solution()
