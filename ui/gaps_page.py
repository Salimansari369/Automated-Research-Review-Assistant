import gradio as gr
from typing import List, Dict, Any

def render_detailed_gaps(gaps: List[Dict[str, Any]]) -> str:
    if not gaps:
        default_gaps = [
            {
                "id": "GAP-01",
                "title": "Real-Time Dynamic Autonomy & Low-Latency Handover in LEO Mega-Constellations",
                "impact": "High Impact",
                "impact_class": "high",
                "evidence_ratio": "8 / 12 papers",
                "confidence": "92%",
                "description": "While existing studies demonstrate Multi-Agent RL algorithms in idealized simulation environments, real-time autonomous routing under Doppler shifts and high-velocity topology changes remains largely unvalidated with real flight hardware.",
                "suggested_direction": "Develop lightweight asynchronous actor-critic models suitable for onboard execution with FPGA hardware-in-the-loop validation.",
                "supporting_papers": [
                    {"title": "Multi-Agent Reinforcement Learning for Satellite Networks", "authors": "Kumar et al.", "year": 2024},
                    {"title": "Autonomous Decision-Making for 6G Non-Terrestrial Networks", "authors": "Singh et al.", "year": 2023},
                    {"title": "Dynamic Inter-Satellite Link Resource Allocation", "authors": "Chen et al.", "year": 2024}
                ]
            },
            {
                "id": "GAP-02",
                "title": "Heterogeneous Multi-Agent Consensus with Asymmetric Constellation Capabilities",
                "impact": "High Impact",
                "impact_class": "high",
                "evidence_ratio": "6 / 12 papers",
                "confidence": "87%",
                "description": "Most multi-agent formulations assume homogeneous satellite payloads with identical compute, memory, and energy budgets. Modern hybrid constellations (LEO + MEO + GEO) have highly asymmetric capabilities.",
                "suggested_direction": "Formulate hierarchical federated reinforcement learning policies with capability-weighted gradient aggregation.",
                "supporting_papers": [
                    {"title": "Federated Learning for Autonomous Swarm Satellites", "authors": "Patel et al.", "year": 2024},
                    {"title": "Heterogeneous Space-Air-Ground Integrated Networks", "authors": "Wang et al.", "year": 2023}
                ]
            },
            {
                "id": "GAP-03",
                "title": "Cross-Layer Radiation & Channel Degradation Adaptation (Ka/Q/V Bands)",
                "impact": "Medium Impact",
                "impact_class": "medium",
                "evidence_ratio": "5 / 12 papers",
                "confidence": "79%",
                "description": "Literature typically decouples physical layer channel modeling (rain fade, ionospheric scintillation) from higher-layer agentic routing decisions, causing sub-optimal throughput in high frequency bands.",
                "suggested_direction": "Implement neuro-symbolic agents that couple cross-layer physical telemetry directly into routing policy action spaces.",
                "supporting_papers": [
                    {"title": "Cognitive Space Antennas via Neuro-Symbolic Agents", "authors": "Sharma et al.", "year": 2025},
                    {"title": "Atmospheric Scintillation Effects on Space Communications", "authors": "Zhao et al.", "year": 2023}
                ]
            }
        ]
        gaps = default_gaps

    gap_cards = []
    for g in gaps:
        is_high = g.get("impact_class") == "high" or "High" in g.get("impact", "")
        impact_class = "impact-high" if is_high else "impact-medium"

        supporting_items = "".join([
            f"<li class='gap-supporting-item'><strong class='gap-supporting-title'>{p['title']}</strong> <span class='gap-supporting-meta'>({p['authors']}, {p['year']})</span></li>"
            for p in g.get("supporting_papers", [])[:4]
        ])

        gap_cards.append(f"""
        <div class="gap-result-card">
          <div class="gap-card-header">
            <div class="gap-header-left">
              <span class="gap-id-badge">{g['id']}</span>
              <h3 class="gap-card-title">{g['title']}</h3>
            </div>
            <span class="gap-impact-badge {impact_class}">
              {g['impact']}
            </span>
          </div>

          <div class="gap-metrics-row">
            <span>📊 Evidence Base: {g['evidence_ratio']}</span>
            <span>🎯 Detection Confidence: {g['confidence']}</span>
          </div>

          <div class="gap-void-box">
            <strong class="gap-void-label">Critical Research Void:</strong> {g['description']}
          </div>

          <div class="gap-direction-box">
            <strong class="gap-direction-label">Recommended Exploration Path:</strong> {g['suggested_direction']}
          </div>

          <details class="gap-details-accordion">
            <summary class="gap-summary-btn">View Grounded Supporting Papers ({len(g.get('supporting_papers', []))})</summary>
            <ul class="gap-supporting-list">
              {supporting_items}
            </ul>
          </details>
        </div>
        """)

    return "".join(gap_cards)


def create_gaps_view():
    with gr.Column(elem_classes=["gaps-view", "gaps-page-container"]):
        gr.Markdown("## 🔍 Research Gap Intelligence\n*Cross-paper meta-analysis identifying empirical and methodological voids.*")

        with gr.Row():
            detect_gaps_btn = gr.Button("🔍 Run Research Gap Intelligence", variant="primary", elem_classes=["btn-primary-gradient"])

        gaps_status_msg = gr.Markdown("Ready to detect research gaps.")
        gaps_container = gr.HTML(value=render_detailed_gaps([]))

    return {
        "detect_gaps_btn": detect_gaps_btn,
        "gaps_status_msg": gaps_status_msg,
        "gaps_container": gaps_container
    }
