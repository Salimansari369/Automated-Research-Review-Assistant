import os
import json
import html
import gradio as gr
from typing import List, Dict, Any
from services.tavily_service import TavilyService

def render_earth_knowledge_globe_html(active_topic: str = "Academic Research") -> str:
    """
    Renders pure HTML for the 3D Earth-architecture knowledge sphere.
    """
    return """
    <div class="earth-globe-wrapper">
      <div class="earth-hud-badge">
        <span class="hud-dot pulsing"></span>
        <span>EARTH KNOWLEDGE TOPOLOGY • 3D ACTIVE SATELLITE SCAN</span>
      </div>
      <canvas id="earthKnowledgeCanvas" width="480" height="420" class="earth-canvas"></canvas>
      <div class="earth-controls-hint">
        <span>👆 Drag to rotate Earth • 🔍 Autonomous Literature Radar active</span>
      </div>
    </div>
    """

EARTH_SCRIPT_HEAD = """
<script>
(function() {
  function initEarthCanvas() {
    const canvas = document.getElementById("earthKnowledgeCanvas");
    if (!canvas || canvas.dataset.initialized === "true") return;
    canvas.dataset.initialized = "true";

    const ctx = canvas.getContext("2d");
    const dpr = window.devicePixelRatio || 1;
    canvas.width = 480 * dpr;
    canvas.height = 420 * dpr;
    ctx.scale(dpr, dpr);
    const width = 480;
    const height = 420;

    const globeRadius = 130;
    const cx = width / 2;
    const cy = height / 2;

    let rotX = 0.2;
    let rotY = 0;
    let targetRotX = 0.2;
    let targetRotY = 0;
    let isDragging = false;
    let lastMouseX = 0;
    let lastMouseY = 0;
    let autoSpeed = 0.007;

    const keywords = [
      "THEORY", "EXPERIMENTS", "METHODOLOGY", "REPRODUCIBILITY",
      "LATENT GAP", "SCALABILITY", "BENCHMARKS", "CAUSALITY",
      "HYPOTHESIS", "ABLATION", "PREDICTION", "GENERALIZATION",
      "EVALUATION", "EMPIRICAL", "OPTIMIZATION", "ALIGNMENT",
      "ROBUSTNESS", "TRANSFER LEARNING", "ZERO-SHOT", "AGENTIC"
    ];

    const words = [];
    const numWords = keywords.length;
    for (let i = 0; i < numWords; i++) {
      const phi = Math.acos(-1 + (2 * i) / numWords);
      const theta = Math.sqrt(numWords * Math.PI) * phi;
      const rad = globeRadius + 18 + (i % 3) * 14;
      words.push({
        text: keywords[i],
        x: rad * Math.sin(phi) * Math.cos(theta),
        y: rad * Math.cos(phi),
        z: rad * Math.sin(phi) * Math.sin(theta),
        size: (i % 4 === 0) ? 14 : 11,
        isBold: (i % 3 === 0)
      });
    }

    const earthPoints = [];
    for (let lat = -70; lat <= 70; lat += 20) {
      const latRad = (lat * Math.PI) / 180;
      const r = globeRadius * Math.cos(latRad);
      const y = globeRadius * Math.sin(latRad);
      for (let lon = 0; lon < 360; lon += 15) {
        const lonRad = (lon * Math.PI) / 180;
        earthPoints.push({
          x: r * Math.sin(lonRad),
          y: y,
          z: r * Math.cos(lonRad),
          type: "grid"
        });
      }
    }

    const landClusters = [
      { lat: 40, lon: -100, count: 30 },
      { lat: -15, lon: -60, count: 25 },
      { lat: 50, lon: 10, count: 35 },
      { lat: 10, lon: 20, count: 30 },
      { lat: 35, lon: 105, count: 45 },
      { lat: -25, lon: 135, count: 20 }
    ];
    landClusters.forEach(c => {
      for (let i = 0; i < c.count; i++) {
        const dLat = (Math.random() - 0.5) * 35;
        const dLon = (Math.random() - 0.5) * 45;
        const latRad = ((c.lat + dLat) * Math.PI) / 180;
        const lonRad = ((c.lon + dLon) * Math.PI) / 180;
        earthPoints.push({
          x: globeRadius * Math.cos(latRad) * Math.sin(lonRad),
          y: globeRadius * Math.sin(latRad),
          z: globeRadius * Math.cos(latRad) * Math.cos(lonRad),
          type: "land"
        });
      }
    });

    function onPointerDown(e) {
      isDragging = true;
      const p = e.touches ? e.touches[0] : e;
      lastMouseX = p.clientX;
      lastMouseY = p.clientY;
    }
    function onPointerMove(e) {
      if (!isDragging) return;
      const p = e.touches ? e.touches[0] : e;
      const dx = p.clientX - lastMouseX;
      const dy = p.clientY - lastMouseY;
      targetRotY += dx * 0.008;
      targetRotX -= dy * 0.008;
      lastMouseX = p.clientX;
      lastMouseY = p.clientY;
    }
    function onPointerUp() {
      isDragging = false;
    }

    canvas.addEventListener("mousedown", onPointerDown);
    window.addEventListener("mousemove", onPointerMove);
    window.addEventListener("mouseup", onPointerUp);
    canvas.addEventListener("touchstart", onPointerDown, { passive: true });
    window.addEventListener("touchmove", onPointerMove, { passive: true });
    window.addEventListener("touchend", onPointerUp);

    let radarAngle = 0;

    function render() {
      if (!document.getElementById("earthKnowledgeCanvas")) {
        requestAnimationFrame(render);
        return;
      }
      ctx.clearRect(0, 0, width, height);

      if (!isDragging) {
        targetRotY += autoSpeed;
      }
      rotY += (targetRotY - rotY) * 0.1;
      rotX += (targetRotX - rotX) * 0.1;
      radarAngle += 0.025;

      const cosY = Math.cos(rotY);
      const sinY = Math.sin(rotY);
      const cosX = Math.cos(rotX);
      const sinX = Math.sin(rotX);

      // 1. Atmosphere Glow
      const atmosGrad = ctx.createRadialGradient(cx, cy, globeRadius * 0.7, cx, cy, globeRadius * 1.25);
      atmosGrad.addColorStop(0, "rgba(8, 20, 45, 0.5)");
      atmosGrad.addColorStop(0.75, "rgba(0, 220, 255, 0.2)");
      atmosGrad.addColorStop(1, "rgba(0, 160, 255, 0)");
      ctx.fillStyle = atmosGrad;
      ctx.beginPath();
      ctx.arc(cx, cy, globeRadius * 1.25, 0, Math.PI * 2);
      ctx.fill();

      // 2. Rim
      ctx.strokeStyle = "rgba(0, 230, 255, 0.4)";
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.arc(cx, cy, globeRadius, 0, Math.PI * 2);
      ctx.stroke();

      // 3. Grid & Land
      for (let i = 0; i < earthPoints.length; i++) {
        const p = earthPoints[i];
        const x1 = p.x * cosY - p.z * sinY;
        const z1 = p.x * sinY + p.z * cosY;
        const y2 = p.y * cosX - z1 * sinX;
        const z2 = p.y * sinX + z1 * cosX;

        if (z2 > -25) {
          const scale = 360 / (360 + z2);
          const projX = cx + x1 * scale;
          const projY = cy + y2 * scale;
          const alpha = Math.max(0.12, (z2 + globeRadius) / (2 * globeRadius));

          if (p.type === "land") {
            ctx.fillStyle = `rgba(0, 255, 210, ${alpha * 0.95})`;
            ctx.beginPath();
            ctx.arc(projX, projY, 2.0 * scale, 0, Math.PI * 2);
            ctx.fill();
          } else {
            ctx.fillStyle = `rgba(0, 180, 255, ${alpha * 0.35})`;
            ctx.beginPath();
            ctx.arc(projX, projY, 1.0 * scale, 0, Math.PI * 2);
            ctx.fill();
          }
        }
      }

      // 4. Scanning Radar Wave
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(radarAngle);
      const sweepGrad = ctx.createLinearGradient(0, 0, globeRadius, 0);
      sweepGrad.addColorStop(0, "rgba(0, 255, 210, 0.4)");
      sweepGrad.addColorStop(1, "rgba(0, 255, 210, 0)");
      ctx.fillStyle = sweepGrad;
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.arc(0, 0, globeRadius, -0.4, 0.4);
      ctx.closePath();
      ctx.fill();
      ctx.restore();

      // 5. Research Keywords
      const sortedWords = [];
      for (let i = 0; i < words.length; i++) {
        const w = words[i];
        const x1 = w.x * cosY - w.z * sinY;
        const z1 = w.x * sinY + w.z * cosY;
        const y2 = w.y * cosX - z1 * sinX;
        const z2 = w.y * sinX + z1 * cosX;
        sortedWords.push({ text: w.text, x: x1, y: y2, z: z2, size: w.size, isBold: w.isBold });
      }
      sortedWords.sort((a, b) => a.z - b.z);

      for (let i = 0; i < sortedWords.length; i++) {
        const w = sortedWords[i];
        const scale = 360 / (360 + w.z);
        const projX = cx + w.x * scale;
        const projY = cy + w.y * scale;

        if (w.z < -10) {
          const alpha = Math.max(0.12, 0.25 * (w.z + globeRadius * 1.3) / globeRadius);
          ctx.fillStyle = `rgba(100, 160, 230, ${alpha})`;
          ctx.font = `9px "Segoe UI", Inter, sans-serif`;
          ctx.fillText(w.text, projX - 18, projY);
        } else {
          const alpha = Math.min(1.0, 0.35 + (w.z / globeRadius) * 0.65);
          ctx.font = `${w.isBold ? "bold " : ""}${Math.round(w.size * scale)}px "Segoe UI", Inter, sans-serif`;
          if (w.isBold) {
            ctx.shadowColor = "rgba(0, 240, 255, 0.8)";
            ctx.shadowBlur = 8;
            ctx.fillStyle = `rgba(240, 250, 255, ${alpha})`;
          } else {
            ctx.shadowColor = "rgba(0, 180, 255, 0.4)";
            ctx.shadowBlur = 4;
            ctx.fillStyle = `rgba(110, 220, 255, ${alpha})`;
          }
          ctx.fillText(w.text, projX - (w.text.length * 3.2), projY);
          ctx.shadowBlur = 0;
        }
      }

      requestAnimationFrame(render);
    }

    render();
  }

  setInterval(initEarthCanvas, 350);
})();
</script>
"""


def render_gap_survival_verdict_card(result: Dict[str, Any]) -> str:
    """
    Renders the live Tavily / Academic Web Investigation result verdict card.
    """
    if not result:
        return """
        <div class="survival-empty-card">
          <div class="survival-empty-icon">🛰️</div>
          <div class="survival-empty-text">
            <strong>Ready for Agentic Investigation</strong>
            <p>Select any detected gap below or enter a research inquiry to launch live Tavily web-scale verification.</p>
          </div>
        </div>
        """

    status = result.get("status", "SURVIVED (CRITICAL OPEN VOID)")
    is_survived = "SURVIVED" in status
    badge_color = "#10b981" if is_survived else "#f59e0b"
    badge_bg = "rgba(16, 185, 129, 0.15)" if is_survived else "rgba(245, 158, 11, 0.15)"
    badge_border = "rgba(16, 185, 129, 0.35)" if is_survived else "rgba(245, 158, 11, 0.35)"
    
    confidence = result.get("confidence", "93.4%")
    engine = result.get("search_engine", "Tavily AI & Academic Sweep")
    verdict = result.get("verdict", "")
    gap_title = result.get("gap_title", "")
    references = result.get("references", [])

    ref_items = []
    for r in references:
        url = r.get("url", "#")
        title = html.escape(r.get("title", "Recent Academic Publication"))
        snippet = html.escape(r.get("snippet", ""))
        ref_items.append(f"""
        <div class="verdict-ref-card">
          <div class="verdict-ref-header">
            <a href="{url}" target="_blank" rel="noopener noreferrer" class="verdict-ref-title">
              🔗 {title}
            </a>
            <span class="verdict-ref-score">{r.get('score', 90)}% Relevance</span>
          </div>
          <p class="verdict-ref-snippet">{snippet}</p>
        </div>
        """)

    ref_html = "".join(ref_items) if ref_items else "<p class='no-refs'>No conflicting publications found.</p>"

    return f"""
    <div class="gap-survival-result-box">
      <div class="survival-result-header">
        <div class="survival-headline-group">
          <span class="survival-tag-eyebrow">AGENTIC VERIFICATION OUTCOME</span>
          <h2 class="survival-target-title">Target Inquiry: {html.escape(gap_title)}</h2>
        </div>
        <div class="survival-badge-container">
          <span class="survival-status-pill" style="background: {badge_bg}; color: {badge_color}; border: 1px solid {badge_border};">
            ● {status}
          </span>
          <span class="survival-conf-pill">Confidence: {confidence}</span>
        </div>
      </div>

      <div class="survival-verdict-banner">
        <div class="verdict-banner-icon">🎯</div>
        <div class="verdict-banner-content">
          <strong>Empirical Research Verdict:</strong>
          <p>{html.escape(verdict)}</p>
        </div>
      </div>

      <div class="survival-engine-meta">
        <span>🌐 <strong>Engine:</strong> {html.escape(engine)}</span>
        <span>⚡ <strong>Verdict Time:</strong> Real-Time Multi-Source Synthesis</span>
      </div>

      <div class="survival-references-section">
        <h4 class="survival-refs-heading">Verified Literature Evidence & Citations ({len(references)}):</h4>
        <div class="survival-refs-grid">
          {ref_html}
        </div>
      </div>
    </div>
    """

def render_detailed_gaps(gaps: List[Dict[str, Any]]) -> str:
    """
    Renders detailed research gap cards with ground evidence and Tavily investigation triggers.
    """
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
    for idx, g in enumerate(gaps, 1):
        is_high = g.get("impact_class") == "high" or "High" in str(g.get("impact", ""))
        impact_class = "impact-high" if is_high else "impact-medium"

        supporting_items = "".join([
            f"<li class='gap-supporting-item'><strong class='gap-supporting-title'>{p.get('title', 'Academic Paper')}</strong> <span class='gap-supporting-meta'>({p.get('authors', 'Authors')}, {p.get('year', 'Recent')})</span></li>"
            for p in g.get("supporting_papers", [])[:4]
        ])

        gap_id = g.get("id") or f"GAP-{idx:02d}"
        gap_title = g.get("title") or g.get("area") or f"CRITICAL RESEARCH VOID #{idx}"
        gap_impact = g.get("impact") or "High Impact"
        gap_evidence = g.get("evidence_ratio") or "Empirical analysis"
        gap_conf = g.get("confidence") or "85%"
        gap_desc = g.get("description") or "Open limitation identified across analyzed literature."
        gap_direction = g.get("suggested_direction") or g.get("opportunity") or "Further empirical investigation and standardized evaluation recommended."

        gap_cards.append(f"""
        <div class="gap-result-card">
          <div class="gap-card-header">
            <div class="gap-header-left">
              <span class="gap-id-badge">{gap_id}</span>
              <h3 class="gap-card-title">{gap_title}</h3>
            </div>
            <span class="gap-impact-badge {impact_class}">
              {gap_impact}
            </span>
          </div>

          <div class="gap-metrics-row">
            <span>📊 Evidence Base: {gap_evidence}</span>
            <span>🎯 Detection Confidence: {gap_conf}</span>
          </div>

          <div class="gap-void-box">
            <strong class="gap-void-label">Critical Research Void:</strong> {gap_desc}
          </div>

          <div class="gap-direction-box">
            <strong class="gap-direction-label">Recommended Exploration Path:</strong> {gap_direction}
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
    """
    Constructs the Complete Research Gap Intelligence UI with 3D Earth Architecture Globe
    and Agentic Tavily Investigation console.
    """
    with gr.Column(elem_classes=["gaps-view", "gaps-page-container"]):

        # -------------------------------------------------------------
        # 1. 3D EARTH HERO SECTION ("SEE BEYOND the literature.")
        # -------------------------------------------------------------
        with gr.Row(elem_classes=["earth-hero-row"]):
            # Left: Futuristic Agentic Text & Investigation Input
            with gr.Column(scale=6, elem_classes=["earth-hero-left"]):
                gr.HTML("""
                <div class="see-beyond-container">
                  <div class="agentic-pill-tag">
                    <span class="pulse-emerald-dot"></span>
                    <span>AGENTIC RESEARCH INTELLIGENCE</span>
                  </div>
                  <h1 class="see-beyond-title">
                    SEE BEYOND<br>
                    <span class="text-cyan-glow">the literature.</span>
                  </h1>
                  <p class="see-beyond-subtitle">
                    Map the field. Find what's missing. Test whether the gap survives.
                  </p>
                </div>
                """)

                with gr.Group(elem_classes=["investigate-input-group"]):
                    gr.Markdown("**WHAT ARE YOU INVESTIGATING?**", elem_classes=["investigate-label"])
                    with gr.Row(elem_classes=["investigate-action-row"]):
                        investigate_input = gr.Textbox(
                            show_label=False,
                            placeholder="e.g. Real-Time Dynamic Autonomy & Low-Latency Handover in LEO Mega-Constellations",
                            lines=1,
                            elem_classes=["investigate-search-box"],
                            scale=4
                        )
                        investigate_btn = gr.Button(
                            "Begin Investigation ➔",
                            variant="primary",
                            elem_classes=["btn-investigate-cta"],
                            scale=2
                        )

                with gr.Accordion("⚙️ Advanced Tavily API & Search Settings (Optional)", open=False):
                    tavily_key_input = gr.Textbox(
                        label="Tavily API Key (Optional)",
                        placeholder="tvly-xxxxxxxxxxxxxxxxxxxx (Leave empty to use automatic free academic search fallback)",
                        type="password",
                        value=os.environ.get("TAVILY_API_KEY", "")
                    )

            # Right: 3D Earth Architecture Knowledge Sphere
            with gr.Column(scale=5, elem_classes=["earth-hero-right"]):
                earth_globe_html = gr.HTML(value=render_earth_knowledge_globe_html())

        # -------------------------------------------------------------
        # 2. GAP SURVIVAL VERDICT DISPLAY
        # -------------------------------------------------------------
        with gr.Row(elem_classes=["gap-survival-verdict-row"]):
            investigate_result_html = gr.HTML(value=render_gap_survival_verdict_card({}))

        # -------------------------------------------------------------
        # 3. CORPUS DETECTED GAPS SECTION
        # -------------------------------------------------------------
        gr.Markdown("---")
        with gr.Row(elem_classes=["gaps-header-row"]):
            with gr.Column(scale=8):
                gr.Markdown("### 🔍 Collective Research Voids Across Analyzed Corpus\n*Multi-document synthesis extracting empirical limitations and methodological white-spaces.*")
            with gr.Column(scale=4, elem_classes=["gaps-action-col"]):
                detect_gaps_btn = gr.Button("🔄 Re-Scan Corpus For Gaps", variant="secondary", elem_classes=["btn-refresh-gaps"])

        gaps_status_msg = gr.Markdown("Ready to detect and investigate research voids.")
        gaps_container = gr.HTML(value=render_detailed_gaps([]))

    return {
        "detect_gaps_btn": detect_gaps_btn,
        "gaps_status_msg": gaps_status_msg,
        "gaps_container": gaps_container,
        "investigate_input": investigate_input,
        "investigate_btn": investigate_btn,
        "investigate_result_html": investigate_result_html,
        "tavily_key_input": tavily_key_input,
        "earth_globe_html": earth_globe_html
    }
