"""Single Page Dashboard Web Interface HTML Template.

Provides the responsive client-side UI for real-time RAG queries,
parameterized sizing calculations, and dynamic report downloads.
"""

from __future__ import annotations


def get_dashboard_html() -> str:
    """Returns the interactive HTML5/CSS3 Single Page Dashboard."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Academic RAG Synthesis Engine - Live Dashboard</title>
    <style>
        :root {
            --bg-primary: #090d16;
            --bg-secondary: #0f172a;
            --bg-card: rgba(30, 41, 59, 0.7);
            --border-color: rgba(148, 163, 184, 0.15);
            --accent-cyan: #38bdf8;
            --accent-blue: #0284c7;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --success: #10b981;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: radial-gradient(circle at top, #0f172a 0%, #090d16 100%);
            color: var(--text-main);
            min-height: 100vh;
            padding: 2rem 1.5rem;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 2rem;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 2.5rem;
        }
        .logo {
            font-size: 1.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .badge {
            background: rgba(56, 189, 248, 0.15);
            border: 1px solid var(--accent-cyan);
            color: var(--accent-cyan);
            padding: 0.35rem 0.85rem;
            border-radius: 999px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .grid-layout {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
        }
        @media (max-width: 900px) {
            .grid-layout { grid-template-columns: 1fr; }
        }
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.75rem;
            backdrop-filter: blur(12px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        .card-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--accent-cyan);
            margin-bottom: 1.25rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .input-group { margin-bottom: 1.2rem; }
        label {
            display: block;
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 0.4rem;
        }
        input, select, textarea {
            width: 100%;
            padding: 0.75rem 1rem;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-main);
            font-family: inherit;
            font-size: 0.95rem;
            transition: border-color 0.2s;
        }
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: var(--accent-cyan);
        }
        .btn {
            background: linear-gradient(135deg, #0284c7, #0369a1);
            color: white;
            padding: 0.85rem 1.5rem;
            border: none;
            border-radius: 8px;
            font-weight: 700;
            cursor: pointer;
            width: 100%;
            transition: transform 0.15s, box-shadow 0.15s;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(2, 132, 199, 0.4);
        }
        .output-box {
            background: #060911;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            max-height: 280px;
            overflow-y: auto;
            white-space: pre-wrap;
            margin-top: 1rem;
            color: #cbd5e1;
        }
        .citation-item {
            background: rgba(15, 23, 42, 0.6);
            border-left: 3px solid var(--accent-cyan);
            padding: 0.85rem;
            border-radius: 0 8px 8px 0;
            margin-bottom: 0.75rem;
            font-size: 0.85rem;
        }
        .citation-source {
            color: var(--accent-cyan);
            font-weight: 600;
            margin-bottom: 0.3rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">⚡ Academic RAG Synthesis Engine</div>
            <div class="badge" id="chunkCounter">● Live Vector DB Active</div>
        </header>

        <div class="grid-layout">
            <div class="card">
                <div class="card-title">🔍 Dynamic Semantic Grounding</div>
                <div class="input-group">
                    <label for="searchQuery">Natural Language Query</label>
                    <textarea id="searchQuery" rows="3">IEEE 830 functional requirements
                        and performance metrics</textarea>
                </div>
                <div class="input-group">
                    <label for="topK">Top Chunks (k)</label>
                    <input type="number" id="topK" min="1" max="10" value="3">
                </div>
                <button class="btn" onclick="executeSearch()">Retrieve Grounded
                    Context</button>
                <div class="output-box" id="queryResults">Semantic matches will appear
                    here...</div>
            </div>

            <div class="card">
                <div class="card-title">📊 Parameterized Report Generator</div>
                <div class="input-group">
                    <label for="sysName">System Name</label>
                    <input type="text" id="sysName" value="AeroGrid Dynamic Edition">
                </div>
                <div class="input-group">
                    <label for="domainName">Industry Domain</label>
                    <input type="text" id="domainName" value="Autonomous Drone
                        Logistics">
                </div>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:1rem;">
                    <div class="input-group">
                        <label for="latencyNFR">P99 Latency (ms)</label>
                        <input type="number" id="latencyNFR" value="120">
                    </div>
                    <div class="input-group">
                        <label for="gscSum">14 GSCs Sum (TDI)</label>
                        <input type="number" id="gscSum" value="45">
                    </div>
                </div>
                <div class="input-group">
                    <label for="cocomoMode">COCOMO Project Category</label>
                    <select id="cocomoMode">
                        <option value="semidetached" selected>Semidetached (Medium
                            Complexity)</option>
                        <option value="organic">Organic (Straightforward)</option>
                        <option value="embedded">Embedded (Tight Constraints)</option>
                    </select>
                </div>
                <button class="btn" onclick="generateDynamicDeliverable()">Generate
                    Dynamic PDF Deliverable</button>
                <div class="output-box" id="buildStatus">Ready to synthesize custom
                    solution deliverable...</div>
            </div>
        </div>
    </div>

    <script>
        async function executeSearch() {
            const query = document.getElementById('searchQuery').value;
            const top_k = parseInt(document.getElementById('topK').value);
            const output = document.getElementById('queryResults');
            output.innerHTML = 'Retrieving nearest dense vectors from ChromaDB...';

            try {
                const response = await fetch('/api/query', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query, top_k })
                });
                const data = await response.json();
                
                let html = '';
                data.matches.forEach((m, idx) => {
                    html += `<div class="citation-item">
                        <div class="citation-source">[${idx + 1}] ${m.source} | Slide
                            ${m.page_or_slide}</div>
                        <div>${m.content}</div>
                    </div>`;
                });
                output.innerHTML = html || 'No matching chunks found.';
            } catch (err) {
                output.innerText = 'Error querying RAG engine: ' + err;
            }
        }

        async function generateDynamicDeliverable() {
            const status = document.getElementById('buildStatus');
            status.innerText = 'Synthesizing dynamic formulas and compiling PDF...';

            const payload = {
                system_name: document.getElementById('sysName').value,
                domain: document.getElementById('domainName').value,
                nfr_latency_p99_ms:
                    parseInt(document.getElementById('latencyNFR').value),
                complexity_adjustment_factors_sum:
                    parseInt(document.getElementById('gscSum').value),
                cocomo_category: document.getElementById('cocomoMode').value
            };

            try {
                const response = await fetch('/api/generate-report', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await response.json();
                status.innerHTML = `✨ Deliverable Built Successfully!\n\n` +
                    `• UFP: ${data.fp_sizing.unadjusted_function_points} | VAF:
                        ${data.fp_sizing.value_adjustment_factor} | KLOC:
                        ${data.fp_sizing.derived_kloc}\n` +
                    `• Effort: ${data.cocomo_estimation.effort_person_months} PM |
                        Staff: ${data.cocomo_estimation.average_staff_size} Eng\n\n` +
                    `📥 <a href="${data.pdf_download_url}" target="_blank"
                        style="color:#38bdf8; font-weight:bold;">Download PDF
                        (${data.pdf_size_kb} KB)</a> | ` +
                    `<a href="${data.html_download_url}" target="_blank"
                        style="color:#818cf8; font-weight:bold;">Open HTML</a>`;
            } catch (err) {
                status.innerText = 'Error compiling deliverable: ' + err;
            }
        }
    </script>
</body>
</html>
"""
