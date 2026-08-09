"""Utility Helpers, Document Rendering, and Compilation Tools.

Provides shared configuration dataclasses, markdown-to-HTML rendering engines,
MathJax and print stylesheet wrappers, and Google Chrome headless PDF compilers.
"""

from __future__ import annotations

import logging
import os
import re
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Final

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from markdown_it import MarkdownIt

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger: Final[logging.Logger] = logging.getLogger("Utils")


def build_chrome_command(
    html_path: str,
    pdf_path: str,
    virtual_time_budget_ms: int = 9000,
) -> list[str]:
    """Helper function to assemble the command-line argument list for Google Chrome.

    Args:
        html_path: Path to the source HTML file.
        pdf_path: Destination path for the generated PDF document.
        virtual_time_budget_ms: Allocated millisecond wait budget for JavaScript.

    Returns:
        list[str]: Command argument vector for subprocess invocation.
    """
    return [
        "google-chrome",
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        f"--virtual-time-budget={virtual_time_budget_ms}",
        f"--print-to-pdf={pdf_path}",
        html_path,
    ]


def wrap_svg_diagram(svg_code: str) -> str:
    """Helper function to wrap an SVG XML string in a responsive CSS container.

    Args:
        svg_code: Raw SVG XML text.

    Returns:
        str: Styled HTML div element enclosing the SVG.
    """
    return f'<div class="diagram-wrapper">{svg_code}</div>'


class DiagramProcessor:
    """Processes Markdown text to replace Mermaid code blocks with vector SVGs."""

    @staticmethod
    def replace_mermaid_with_placeholders(markdown_content: str) -> tuple[str, int]:
        """Scans Markdown for Mermaid blocks and substitutes sequential placeholders.

        Args:
            markdown_content: Raw Markdown source text.

        Returns:
            tuple[str, int]: Processed Markdown string and replaced blocks count.
        """
        mermaid_blocks: list[str] = re.findall(
            pattern=r"```mermaid\n(.*?)```",
            string=markdown_content,
            flags=re.DOTALL,
        )
        processed_md: str = markdown_content
        for idx, block in enumerate(mermaid_blocks):
            placeholder: str = f"<!--VECTOR_SVG_PLACEHOLDER_{idx}-->"
            target_str: str = f"```mermaid\n{block}```"
            processed_md = processed_md.replace(target_str, placeholder, 1)
        return processed_md, len(mermaid_blocks)

    @staticmethod
    def inject_vector_svgs(html_content: str, svg_list: Sequence[str]) -> str:
        """Injects crisp vector SVG elements in place of HTML comment placeholders.

        Args:
            html_content: Rendered HTML containing comment placeholders.
            svg_list: Ordered list of SVG XML strings.

        Returns:
            str: HTML content with embedded vector diagram wrappers.
        """
        result_html: str = html_content
        for idx, svg_code in enumerate(svg_list):
            placeholder: str = f"<!--VECTOR_SVG_PLACEHOLDER_{idx}-->"
            wrapper: str = wrap_svg_diagram(svg_code)
            result_html = result_html.replace(f"<p>{placeholder}</p>", wrapper)
            result_html = result_html.replace(placeholder, wrapper)
        return result_html


class MarkdownDocumentRenderer:
    """Renders processed Markdown into styled HTML with MathJax and print CSS."""

    def __init__(self, page_size: str = "A4") -> None:
        """Initializes the Markdown renderer.

        Args:
            page_size: Target page size standard for print styling.
        """
        self.page_size: str = page_size
        self._md_parser: MarkdownIt = MarkdownIt().enable("table")

    def render_body(self, markdown_text: str) -> str:
        """Converts Markdown text to raw HTML body elements.

        Args:
            markdown_text: Input Markdown text.

        Returns:
            str: HTML markup string.
        """
        return str(self._md_parser.render(markdown_text))

    def wrap_html_template(self, body_html: str, document_title: str) -> str:
        """Wraps HTML body inside a complete HTML5 document with CSS.

        Args:
            body_html: Inner HTML body content.
            document_title: Document header title tag.

        Returns:
            str: Full HTML5 document string.
        """
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{document_title}</title>
    <script id="MathJax-script" async
            src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
    </script>
    <script>
        MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
            }}
        }};
    </script>
    <style>
        @page {{
            size: {self.page_size};
            margin: 20mm 16mm 20mm 16mm;
        }}
        * {{
            box-sizing: border-box;
        }}
        body {{
            font-family: system-ui, -apple-system, BlinkMacSystemFont,
                         'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.65;
            color: #1e293b;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
            font-size: 11.5pt;
            letter-spacing: -0.01em;
        }}
        h1 {{
            color: #0f172a;
            font-size: 22pt;
            font-weight: 700;
            border-bottom: 2.5px solid #0284c7;
            padding-bottom: 8px;
            margin-top: 26pt;
            margin-bottom: 14pt;
            page-break-after: avoid;
            break-after: avoid;
        }}
        h2 {{
            color: #0284c7;
            font-size: 16pt;
            font-weight: 600;
            margin-top: 20pt;
            margin-bottom: 10pt;
            border-bottom: 1.5px solid #e2e8f0;
            padding-bottom: 5px;
            page-break-after: avoid;
            break-after: avoid;
        }}
        h3 {{
            color: #1e293b;
            font-size: 13.5pt;
            font-weight: 600;
            margin-top: 16pt;
            margin-bottom: 8pt;
            page-break-after: avoid;
            break-after: avoid;
        }}
        h4 {{
            color: #334155;
            font-size: 12pt;
            font-weight: 600;
            margin-top: 12pt;
            margin-bottom: 6pt;
            page-break-after: avoid;
            break-after: avoid;
        }}
        p {{
            margin-top: 0;
            margin-bottom: 10pt;
            text-align: justify;
        }}
        table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 16pt 0;
            font-size: 10pt;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #cbd5e1;
            box-shadow: 0 2px 5px rgba(0,0,0,0.04);
            page-break-inside: auto;
            break-inside: auto;
        }}
        tr {{
            page-break-inside: avoid;
            break-inside: avoid;
        }}
        th, td {{
            padding: 9px 12px;
            text-align: left;
            vertical-align: top;
            border-bottom: 1px solid #e2e8f0;
            border-right: 1px solid #e2e8f0;
        }}
        th:last-child, td:last-child {{
            border-right: none;
        }}
        tr:last-child td {{
            border-bottom: none;
        }}
        th {{
            background: linear-gradient(135deg, #0284c7, #0369a1);
            color: #ffffff;
            font-weight: 600;
            font-size: 10.5pt;
        }}
        tr:nth-child(even) {{
            background-color: #f8fafc;
        }}
        blockquote {{
            border-left: 4.5px solid #0284c7;
            background-color: #f0f9ff;
            margin: 12pt 0;
            padding: 10pt 16pt;
            color: #0369a1;
            border-radius: 0 8px 8px 0;
            font-size: 11pt;
            font-style: italic;
        }}
        .diagram-wrapper {{
            text-align: center;
            margin: 22pt 0;
            padding: 16pt;
            background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
            border: 1.5px solid #cbd5e1;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            page-break-inside: avoid;
            break-inside: avoid;
        }}
        .diagram-wrapper svg {{
            display: block;
            margin: 0 auto;
            max-width: 100%;
            height: auto;
        }}
        code {{
            background-color: #f1f5f9;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 9.5pt;
            color: #0284c7;
            font-weight: 600;
        }}
        hr {{
            border: 0;
            height: 1.5px;
            background: #cbd5e1;
            margin: 18pt 0;
        }}
        ul, ol {{
            margin-top: 0;
            margin-bottom: 10pt;
            padding-left: 24px;
        }}
        li {{
            margin-bottom: 4pt;
        }}
    </style>
</head>
<body>
    {body_html}
</body>
</html>
"""


class HeadlessPDFCompiler:
    """Compiles HTML documents to print-ready PDFs using Headless Google Chrome."""

    @staticmethod
    def compile_pdf(
        html_path: str, pdf_path: str, virtual_time_budget_ms: int = 9000
    ) -> bool:
        """Executes Google Chrome headless to print HTML to high-resolution PDF.

        Args:
            html_path: Path to the input HTML file.
            pdf_path: Path where the output PDF will be generated.
            virtual_time_budget_ms: Wait time for JavaScript (MathJax) rendering.

        Returns:
            bool: True if PDF generation succeeded, False otherwise.
        """
        cmd: list[str] = build_chrome_command(
            html_path=html_path,
            pdf_path=pdf_path,
            virtual_time_budget_ms=virtual_time_budget_ms,
        )

        base_pdf_name: str = os.path.basename(pdf_path)
        logger.info(
            f"Executing Google Chrome headless PDF export for {base_pdf_name}..."
        )
        try:
            result: subprocess.CompletedProcess[str] = subprocess.run(
                args=cmd,
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
            if result.returncode == 0 and os.path.exists(pdf_path):
                size_kb: float = os.path.getsize(pdf_path) / 1024.0
                logger.info(
                    f"✓ PDF Generated successfully: {pdf_path} ({size_kb:.1f} KB)"
                )
                return True
            else:
                logger.error(
                    f"Chrome PDF failed (code {result.returncode}): {result.stderr}"
                )
                return False
        except Exception as err:
            logger.error(f"Exception during Chrome PDF compilation: {err}")
            return False
