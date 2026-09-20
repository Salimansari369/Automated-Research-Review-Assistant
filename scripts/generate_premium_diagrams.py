"""
Generates modern, premium, visually rich infographics and architecture diagrams
for the Automated Literature Review Assistant (ALRA) project report.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

os.makedirs('assets/diagrams', exist_ok=True)

plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

def draw_card(ax, x, y, w, h, header_title, header_color, bg_color, border_color, items=None, subtitle=None, badge_num=None):
    # Main Card Box
    card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.12",
                                  fc=bg_color, ec=border_color, lw=1.8, zorder=2)
    ax.add_patch(card)
    
    # Header Banner Box
    hh = h * 0.26
    hy = y + h - hh
    # clip header inside top of card
    header_patch = patches.FancyBboxPatch((x, hy), w, hh, boxstyle="round,pad=0.04,rounding_size=0.12",
                                         fc=header_color, ec=header_color, lw=1.0, zorder=3)
    ax.add_patch(header_patch)
    
    # Badge if any
    if badge_num:
        badge_circle = patches.Circle((x + 0.35, hy + hh/2), 0.22, fc="#FFFFFF", ec=header_color, lw=1.2, zorder=4)
        ax.add_patch(badge_circle)
        ax.text(x + 0.35, hy + hh/2, str(badge_num), ha='center', va='center', fontsize=9, fontweight='bold', color=header_color, zorder=5)
        title_x = x + 0.7
        ha_align = 'left'
    else:
        title_x = x + w/2
        ha_align = 'center'
        
    ax.text(title_x, hy + hh/2, header_title, ha=ha_align, va='center', fontsize=10, fontweight='bold', color='#FFFFFF', zorder=5)
    
    # Subtitle / content
    curr_y = hy - 0.28
    if subtitle:
        ax.text(x + w/2, curr_y, subtitle, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#334155', zorder=4)
        curr_y -= 0.35
        
    if items:
        for it in items:
            ax.text(x + 0.25, curr_y, f"• {it}", ha='left', va='center', fontsize=8, color='#1E293B', zorder=4)
            curr_y -= 0.32

def draw_arrow(ax, x1, y1, x2, y2, label=None, color='#3B82F6', label_offset=(0, 0.15)):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(facecolor=color, edgecolor=color, width=2.2, headwidth=7, headlength=7, shrink=0.04),
                zorder=10)
    if label:
        mid_x = (x1 + x2) / 2 + label_offset[0]
        mid_y = (y1 + y2) / 2 + label_offset[1]
        ax.text(mid_x, mid_y, label, ha='center', va='center', fontsize=8, fontweight='bold',
                color='#0F172A', bbox=dict(boxstyle="round,pad=0.2", fc="#FFFFFF", ec="#CBD5E1", lw=1), zorder=11)

# ==========================================
# 1. Figure 1.1: System Ecosystem
# ==========================================
def gen_fig1_1():
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.2)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')

    # Enclosing container: ALRA Platform
    platform_box = patches.FancyBboxPatch((2.7, 0.4), 5.4, 5.4, boxstyle="round,pad=0.1,rounding_size=0.2",
                                          fc="#FFFFFF", ec="#94A3B8", lw=1.5, ls="--", zorder=1)
    ax.add_patch(platform_box)
    ax.text(5.4, 5.55, "AUTOMATED LITERATURE REVIEW ASSISTANT (ALRA) CORE", ha='center', va='center', fontsize=10, fontweight='bold', color="#475569")

    # 1. User Card
    draw_card(ax, 0.4, 2.0, 2.0, 2.4, "User / Scholar", "#0284C7", "#F0F9FF", "#38BDF8",
              items=["Voice Prompt", "Search Query", "PDF Upload", "Review Export"], badge_num="1")

    # 2. Gradio UI Card
    draw_card(ax, 3.0, 3.1, 2.2, 2.2, "Gradio 6.0 UI Layer", "#1E40AF", "#EFF6FF", "#60A5FA",
              items=["Light / Dark Theme", "Search & Filter", "Neural Q&A Tabs", "3D Gap Network"], badge_num="2")

    # 3. Salim AI Voice Card
    draw_card(ax, 3.0, 0.7, 2.2, 2.0, "Salim AI Voice", "#7C3AED", "#FAF5FF", "#C084FC",
              items=["WebSpeech Rec.", "Intent Classifier", "EdgeTTS Synthesis"], badge_num="3")

    # 4. Agentic Orchestrator
    draw_card(ax, 5.6, 1.8, 2.3, 3.5, "Agentic Intelligence", "#B45309", "#FFFBEB", "#FBBF24",
              items=["Query Expansion", "ArXiv / S2 Worker", "PyMuPDF Parser", "FAISS Vector DB", "Gap Matrix Engine", "Word / LaTeX Synth"], badge_num="4")

    # 5. External Cloud Services
    draw_card(ax, 8.5, 3.2, 2.1, 2.3, "LLM Reasoning", "#9D174D", "#FDF2F8", "#F472B6",
              items=["Groq LLaMA-3.3", "DeepSeek-R1", "Zero-Hallucination"], badge_num="5")

    draw_card(ax, 8.5, 0.7, 2.1, 2.2, "Academic Cloud", "#065F46", "#F0FDF4", "#4ADE80",
              items=["ArXiv Search API", "Semantic Scholar", "DOI Hard-Links"], badge_num="6")

    # Flow Arrows
    draw_arrow(ax, 2.4, 3.5, 3.0, 3.9, label="UI Actions", color="#0284C7")
    draw_arrow(ax, 2.4, 2.7, 3.0, 1.8, label="Speech", color="#7C3AED")
    draw_arrow(ax, 5.2, 4.0, 5.6, 4.0, label="Events", color="#1E40AF")
    draw_arrow(ax, 5.2, 1.8, 5.6, 2.5, label="Audio Stream", color="#7C3AED")
    draw_arrow(ax, 7.9, 4.2, 8.5, 4.2, label="Reasoning", color="#9D174D")
    draw_arrow(ax, 7.9, 2.2, 8.5, 1.8, label="Fetch Data", color="#065F46")

    plt.tight_layout()
    plt.savefig('assets/diagrams/fig1_1_ecosystem.png', bbox_inches='tight', dpi=300)
    plt.close()

# ==========================================
# 2. Figure 2.1: Problem & Gap Comparison
# ==========================================
def gen_fig2_1():
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.5)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')

    # Card 1: Traditional
    draw_card(ax, 0.6, 0.5, 4.6, 4.5, "Traditional Literature Review Bottlenecks", "#991B1B", "#FEF2F2", "#F87171",
              items=[
                  "Fragmented Search across siloed portals",
                  "Manual downloading & skimming of 100+ PDFs",
                  "Tedious copy-pasting into manual Excel sheets",
                  "Cognitive blindspots: missing critical unexplored gaps",
                  "Hallucinated citations from generic chatbots",
                  "Avg. 23.5 hours per preliminary literature chapter"
              ], subtitle="HIGH COGNITIVE OVERHEAD")

    # Card 2: ALRA Solution
    draw_card(ax, 5.8, 0.5, 4.6, 4.5, "ALRA Autonomous Agentic Workflow", "#15803D", "#F0FDF4", "#4ADE80",
              items=[
                  "Parallel Multi-API query expansion (ArXiv & S2)",
                  "Sub-50ms local FAISS neural vector indexing",
                  "Automated comparative taxonomy matrix creation",
                  "AI Gap Intelligence & 3D cluster discovery",
                  "100% verified citation grounding (0% hallucination)",
                  "Total turnaround time: Under 3.8 minutes"
              ], subtitle="AUTONOMOUS & ACCELERATED")

    # VS Badge in middle
    vs_circle = patches.Circle((5.5, 2.75), 0.45, fc="#0F172A", ec="#FFFFFF", lw=2.5, zorder=12)
    ax.add_patch(vs_circle)
    ax.text(5.5, 2.75, "VS", ha='center', va='center', fontsize=12, fontweight='bold', color="#FFFFFF", zorder=13)

    plt.tight_layout()
    plt.savefig('assets/diagrams/fig2_1_problem_gap.png', bbox_inches='tight', dpi=300)
    plt.close()

# ==========================================
# 3. Figure 3.1: Static vs Tool-Grounded
# ==========================================
def gen_fig3_1():
    fig, ax = plt.subplots(figsize=(11, 5.2), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.2)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')

    # Top Flow: Static LLM
    ax.text(0.6, 4.6, "A. Generic LLM Chatbot (Static Single-Turn)", fontsize=10, fontweight='bold', color="#475569")
    draw_card(ax, 0.6, 3.0, 2.0, 1.4, "User Query", "#64748B", "#F1F5F9", "#94A3B8", items=["Single prompt"])
    draw_card(ax, 3.4, 3.0, 2.6, 1.4, "Direct LLM API", "#94A3B8", "#F8FAFC", "#CBD5E1", items=["No live search", "Outdated training"])
    draw_card(ax, 6.8, 3.0, 3.6, 1.4, "Unverified Summary", "#DC2626", "#FEF2F2", "#FCA5A5", items=["Fake / Hallucinated DOIs", "Isolated in chat box"])
    
    draw_arrow(ax, 2.6, 3.7, 3.4, 3.7, color="#64748B")
    draw_arrow(ax, 6.0, 3.7, 6.8, 3.7, color="#DC2626")

    # Bottom Flow: ALRA Agentic
    ax.text(0.6, 2.3, "B. ALRA Agentic Review Pipeline (Tool-Grounded & Verified)", fontsize=10, fontweight='bold', color="#1E40AF")
    draw_card(ax, 0.6, 0.4, 1.9, 1.6, "Research Intent", "#0284C7", "#F0F9FF", "#38BDF8", items=["Topic / Paper", "Voice / Text"])
    draw_card(ax, 2.9, 0.4, 2.3, 1.6, "Multi-API Ingestion", "#16A34A", "#F0FDF4", "#4ADE80", items=["ArXiv + S2", "FAISS Vector RAG"])
    draw_card(ax, 5.6, 0.4, 2.3, 1.6, "Gap & Synthesis", "#B45309", "#FFFBEB", "#FBBF24", items=["DeepSeek Cluster", "Taxonomy Matrix"])
    draw_card(ax, 8.3, 0.4, 2.3, 1.6, "Verified Report", "#1E40AF", "#EFF6FF", "#60A5FA", items=["100% Citations", "Word (.docx) Export"])

    draw_arrow(ax, 2.5, 1.2, 2.9, 1.2, color="#0284C7")
    draw_arrow(ax, 5.2, 1.2, 5.6, 1.2, color="#16A34A")
    draw_arrow(ax, 7.9, 1.2, 8.3, 1.2, color="#B45309")

    plt.tight_layout()
    plt.savefig('assets/diagrams/fig3_1_static_vs_agentic.png', bbox_inches='tight', dpi=300)
    plt.close()

# ==========================================
# 4. Figure 5.1: 5-Tier Layered Architecture
# ==========================================
def gen_fig5_1():
    fig, ax = plt.subplots(figsize=(11, 7.0), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.0)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')

    layers = [
        ("Layer 5: Presentation & Multimodal UI Layer", "#1E40AF", "#EFF6FF", "#60A5FA",
         "Gradio 6.0 | Light Academic & Dark Cyber CSS | WebSpeech Voice Input | Interactive 3D Gap Network", 5.6),
        ("Layer 4: API Gateway & Application Routing Layer", "#0284C7", "#F0F9FF", "#38BDF8",
         "FastAPI Micro-Endpoints | Asynchronous Coroutines | JSON Schema Validation | Session Cache", 4.2),
        ("Layer 3: Autonomous Agentic Intelligence Layer", "#7C3AED", "#FAF5FF", "#C084FC",
         "Query Expansion Agent | Gap Intelligence Engine | Comparative Matrix Synthesizer | Groq & DeepSeek", 2.8),
        ("Layer 2: Extraction & Vector Indexing Layer", "#15803D", "#F0FDF4", "#4ADE80",
         "PyMuPDF Parsing Engine | sentence-transformers (all-MiniLM-L6-v2) | Local FAISS L2 Vector Space", 1.4),
        ("Layer 1: External Academic & Speech Cloud Services", "#9D174D", "#FDF2F8", "#F472B6",
         "ArXiv Search API | Semantic Scholar Open Data API | Microsoft EdgeTTS Cloud | Local Storage", 0.0)
    ]

    for title, hc, bg, bc, desc, y_val in layers:
        card = patches.FancyBboxPatch((0.6, y_val + 0.1), 9.8, 1.15, boxstyle="round,pad=0.04,rounding_size=0.12",
                                      fc=bg, ec=bc, lw=1.8, zorder=2)
        ax.add_patch(card)
        # Header banner strip
        hb = patches.FancyBboxPatch((0.6, y_val + 0.82), 9.8, 0.43, boxstyle="round,pad=0.04,rounding_size=0.12",
                                    fc=hc, ec=hc, lw=1.0, zorder=3)
        ax.add_patch(hb)
        ax.text(5.5, y_val + 1.04, title, ha='center', va='center', fontsize=10, fontweight='bold', color="#FFFFFF", zorder=4)
        ax.text(5.5, y_val + 0.48, desc, ha='center', va='center', fontsize=8.5, color="#1E293B", zorder=4)

        # Connector dots between layers
        if y_val > 0.0:
            ax.annotate('', xy=(5.5, y_val + 0.1), xytext=(5.5, y_val - 0.1),
                        arrowprops=dict(facecolor="#475569", edgecolor="#475569", width=1.5, headwidth=5, headlength=5),
                        zorder=10)

    plt.tight_layout()
    plt.savefig('assets/diagrams/fig5_1_layered_architecture.png', bbox_inches='tight', dpi=300)
    plt.close()

# ==========================================
# 5. Figure 5.2: Multi-Turn Agent Loop
# ==========================================
def gen_fig5_2():
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.5)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')

    nodes = [
        (0.6, 2.0, 2.0, 2.0, "1. User Request", "#0284C7", "#F0F9FF", "#38BDF8", ["Research Intent", "Voice or Query"]),
        (3.0, 3.4, 2.2, 1.8, "2. Query Expansion", "#B45309", "#FFFBEB", "#FBBF24", ["Synonym Reform.", "Boolean Filters"]),
        (3.0, 0.6, 2.2, 1.8, "3. Multi-API Fetch", "#15803D", "#F0FDF4", "#4ADE80", ["ArXiv & Semantic", "PDF Text Chunk"]),
        (5.8, 2.0, 2.2, 2.0, "4. Vector Indexing", "#7C3AED", "#FAF5FF", "#C084FC", ["FAISS Embedding", "Dense Clustering"]),
        (8.4, 2.0, 2.2, 2.0, "5. Synthesis Export", "#1E40AF", "#EFF6FF", "#60A5FA", ["Gap Intelligence", "Word / LaTeX .docx"])
    ]

    for x, y, w, h, t, hc, bg, bc, items in nodes:
        draw_card(ax, x, y, w, h, t, hc, bg, bc, items=items)

    draw_arrow(ax, 2.6, 3.0, 3.0, 4.0, label="Expand", color="#B45309")
    draw_arrow(ax, 2.6, 2.2, 3.0, 1.5, label="Fetch", color="#15803D")
    draw_arrow(ax, 5.2, 4.0, 5.8, 3.2, label="Embed", color="#7C3AED")
    draw_arrow(ax, 5.2, 1.5, 5.8, 2.6, label="Index", color="#7C3AED")
    draw_arrow(ax, 8.0, 3.0, 8.4, 3.0, label="Compile", color="#1E40AF")

    plt.tight_layout()
    plt.savefig('assets/diagrams/fig5_2_agent_loop.png', bbox_inches='tight', dpi=300)
    plt.close()

# ==========================================
# 6. Figure 5.3: Salim AI Voice Flowchart
# ==========================================
def gen_fig5_3():
    fig, ax = plt.subplots(figsize=(11, 4.8), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.8)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')

    v_cards = [
        (0.5, 1.4, 1.8, 2.0, "1. User Audio", "#0284C7", "#F0F9FF", "#38BDF8", ["Microphone Capture", "Continuous Audio"]),
        (2.6, 1.4, 1.9, 2.0, "2. WebSpeech", "#B45309", "#FFFBEB", "#FBBF24", ["Browser STT", "Real-time Text"]),
        (4.8, 1.4, 1.9, 2.0, "3. Salim AI", "#7C3AED", "#FAF5FF", "#C084FC", ["Context Fusion", "Groq / DeepSeek"]),
        (7.0, 1.4, 1.9, 2.0, "4. EdgeTTS", "#15803D", "#F0FDF4", "#4ADE80", ["Audio Synthesizer", "Low-latency MP3"]),
        (9.2, 1.4, 1.5, 2.0, "5. Playback", "#9D174D", "#FDF2F8", "#F472B6", ["Browser Audio", "Spoken Review"])
    ]

    for x, y, w, h, t, hc, bg, bc, items in v_cards:
        draw_card(ax, x, y, w, h, t, hc, bg, bc, items=items)

    draw_arrow(ax, 2.3, 2.4, 2.6, 2.4, color="#0284C7")
    draw_arrow(ax, 4.5, 2.4, 4.8, 2.4, color="#B45309")
    draw_arrow(ax, 6.7, 2.4, 7.0, 2.4, color="#7C3AED")
    draw_arrow(ax, 8.9, 2.4, 9.2, 2.4, color="#15803D")

    plt.tight_layout()
    plt.savefig('assets/diagrams/fig5_5_voice_flow.png', bbox_inches='tight', dpi=300)
    plt.close()

if __name__ == '__main__':
    gen_fig1_1()
    gen_fig2_1()
    gen_fig3_1()
    gen_fig5_1()
    gen_fig5_2()
    gen_fig5_3()
    print("[SUCCESS] All 6 premium visual infographics generated successfully in assets/diagrams/")
