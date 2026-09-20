"""
Generates publication-quality architecture diagrams, flowcharts, 
and system workflows for the Automated Literature Review Assistant.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('assets/diagrams', exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# 1. Figure 1.1: System Ecosystem
def gen_fig1_1():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    ax.axis('off')

    # Background canvas
    fig.patch.set_facecolor('#ffffff')

    # User Box
    ax.add_patch(patches.FancyBboxPatch((0.4, 2.0), 1.8, 1.5, boxstyle="round,pad=0.1", fc="#E0F2FE", ec="#0284C7", lw=1.5))
    ax.text(1.3, 2.9, "Academic Researcher\n/ Scholar", ha='center', va='center', fontsize=10, fontweight='bold', color="#0369A1")
    ax.text(1.3, 2.3, "(Voice / UI Input)", ha='center', va='center', fontsize=8.5, color="#075985")

    # Gradio UI Box
    ax.add_patch(patches.FancyBboxPatch((2.7, 1.2), 2.2, 3.1, boxstyle="round,pad=0.1", fc="#F1F5F9", ec="#475569", lw=1.5))
    ax.text(3.8, 4.0, "Gradio 6.0 Presentation Layer", ha='center', va='center', fontsize=9.5, fontweight='bold', color="#1E293B")
    ax.text(3.8, 3.3, "• Dual-Theme Dashboard\n• Search & Filter Papers\n• Neural Paper Analysis\n• Gap Intelligence Graph\n• Salim AI Voice Assistant", ha='center', va='center', fontsize=8, color="#334155")


    # Agentic Orchestrator Box
    ax.add_patch(patches.FancyBboxPatch((5.4, 1.2), 2.1, 3.1, boxstyle="round,pad=0.1", fc="#FEF3C7", ec="#D97706", lw=1.5))
    ax.text(6.45, 4.0, "ALRA Agentic Engine", ha='center', va='center', fontsize=9.5, fontweight='bold', color="#92400E")
    ax.text(6.45, 3.3, "• Query Expansion Agent\n• ArXiv/S2 Fetcher\n• PDF Parser (PyMuPDF)\n• FAISS Vector Store\n• Matrix Synthesis Agent", ha='center', va='center', fontsize=8, color="#78350F")

    # External APIs & LLMs
    ax.add_patch(patches.FancyBboxPatch((8.0, 2.9), 1.7, 1.8, boxstyle="round,pad=0.1", fc="#FCE7F3", ec="#DB2777", lw=1.5))
    ax.text(8.85, 4.2, "AI Reasoning", ha='center', va='center', fontsize=9, fontweight='bold', color="#9D174D")
    ax.text(8.85, 3.5, "• Groq LLaMA-3.3\n• DeepSeek-R1\n• EdgeTTS Voice", ha='center', va='center', fontsize=7.5, color="#831843")

    ax.add_patch(patches.FancyBboxPatch((8.0, 0.8), 1.7, 1.8, boxstyle="round,pad=0.1", fc="#DCFCE7", ec="#16A34A", lw=1.5))
    ax.text(8.85, 2.1, "Academic Repos", ha='center', va='center', fontsize=9, fontweight='bold', color="#15803D")
    ax.text(8.85, 1.4, "• ArXiv API\n• Semantic Scholar\n• Local Vector DB", ha='center', va='center', fontsize=7.5, color="#166534")

    # Arrows
    arrow = dict(facecolor='#334155', edgecolor='#334155', width=1.5, headwidth=6, shrink=0.05)
    ax.annotate('', xy=(2.7, 2.75), xytext=(2.2, 2.75), arrowprops=arrow)
    ax.annotate('', xy=(2.2, 2.65), xytext=(2.7, 2.65), arrowprops=arrow)
    ax.annotate('', xy=(5.4, 2.75), xytext=(4.9, 2.75), arrowprops=arrow)
    ax.annotate('', xy=(4.9, 2.65), xytext=(5.4, 2.65), arrowprops=arrow)
    ax.annotate('', xy=(8.0, 3.8), xytext=(7.5, 3.8), arrowprops=arrow)
    ax.annotate('', xy=(7.5, 3.6), xytext=(8.0, 3.6), arrowprops=arrow)
    ax.annotate('', xy=(8.0, 1.7), xytext=(7.5, 1.7), arrowprops=arrow)
    ax.annotate('', xy=(7.5, 1.5), xytext=(8.0, 1.5), arrowprops=arrow)

    plt.tight_layout()
    plt.savefig('assets/diagrams/fig1_1_ecosystem.png', bbox_inches='tight', dpi=300)
    plt.close()

# 2. Figure 2.1: Problem Gaps vs ALRA Solution
def gen_fig2_1():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')
    fig.patch.set_facecolor('#ffffff')

    # Traditional Side
    ax.add_patch(patches.FancyBboxPatch((0.5, 0.6), 4.2, 3.8, boxstyle="round,pad=0.1", fc="#FEE2E2", ec="#DC2626", lw=1.5))
    ax.text(2.6, 4.0, "TRADITIONAL LITERATURE REVIEW", ha='center', va='center', fontsize=10, fontweight='bold', color="#991B1B")
    t_items = [
        "[X] Manual keyword searching across siloed sites",
        "[X] Overwhelming reading volume (100+ PDF downloads)",
        "[X] Tedious copy-pasting into manual Excel matrices",
        "[X] Incomplete coverage & missed critical research gaps",
        "[X] High hallucination risk in generic LLM chatbots"
    ]
    for i, item in enumerate(t_items):
        ax.text(0.8, 3.4 - (i * 0.6), item, ha='left', va='center', fontsize=8.5, color="#7F1D1D")

    # ALRA Autonomous Side
    ax.add_patch(patches.FancyBboxPatch((5.3, 0.6), 4.2, 3.8, boxstyle="round,pad=0.1", fc="#DCFCE7", ec="#16A34A", lw=1.5))
    ax.text(7.4, 4.0, "ALRA AGENTIC AUTOMATION", ha='center', va='center', fontsize=10, fontweight='bold', color="#166534")
    a_items = [
        "[+] Automated multi-source querying (ArXiv & S2)",
        "[+] Instant neural section extraction & local FAISS RAG",
        "[+] Autonomous taxonomy synthesis with IEEE references",
        "[+] AI Gap Intelligence & 3D cluster discovery",
        "[+] 100% citation grounding with 0% hallucination"
    ]
    for i, item in enumerate(a_items):
        ax.text(5.6, 3.4 - (i * 0.6), item, ha='left', va='center', fontsize=8.5, color="#14532D")

    plt.tight_layout()
    plt.savefig('assets/diagrams/fig2_1_problem_gap.png', bbox_inches='tight', dpi=300)
    plt.close()

# 3. Figure 3.1: Static Search vs Agentic Review
def gen_fig3_1():
    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.8)
    ax.axis('off')
    fig.patch.set_facecolor('#ffffff')

    # Box 1: Static LLM Chat
    ax.add_patch(patches.FancyBboxPatch((0.5, 0.5), 4.2, 3.8, boxstyle="round,pad=0.1", fc="#F1F5F9", ec="#64748B", lw=1.5))
    ax.text(2.6, 3.9, "Static LLM / Chatbot Approach", ha='center', va='center', fontsize=10, fontweight='bold', color="#334155")
    ax.text(2.6, 2.2, "User Query\n↓\nSingle Prompt to LLM\n↓\nUnverified Text Summary\n(Isolated in transcript, fake citations)", ha='center', va='center', fontsize=8.5, color="#475569")

    # Box 2: ALRA Agentic
    ax.add_patch(patches.FancyBboxPatch((5.3, 0.5), 4.2, 3.8, boxstyle="round,pad=0.1", fc="#EFF6FF", ec="#2563EB", lw=1.5))
    ax.text(7.4, 3.9, "ALRA Tool-Grounded Agentic Pipeline", ha='center', va='center', fontsize=10, fontweight='bold', color="#1E40AF")
    ax.text(7.4, 2.2, "Research Intent\n↓\nQuery Expansion & Multi-API Call\n↓\nDense FAISS Vector Indexing\n↓\nGap Intelligence + Verified Review Matrix\n↓\nPublication-Ready Word (.docx) & LaTeX", ha='center', va='center', fontsize=8.5, color="#1D4ED8")

    plt.tight_layout()
    plt.savefig('assets/diagrams/fig3_1_static_vs_agentic.png', bbox_inches='tight', dpi=300)
    plt.close()

# 4. Figure 5.1: Layered System Architecture
def gen_fig5_1():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis('off')
    fig.patch.set_facecolor('#ffffff')

    layers = [
        ("Layer 5: Presentation & Multimodal UI", "#E0F2FE", "#0284C7", "Gradio 6.0 Dashboard | Dual Themes (Academic/Cyber) | Salim AI Voice WebSpeech | 3D Graph Visualizer", 5.2),
        ("Layer 4: API Gateway & Application Routing", "#FEF3C7", "#D97706", "FastAPI Micro-Endpoints | Asynchronous Coroutines | JSON Schema Validators | Session Manager", 3.9),
        ("Layer 3: Autonomous Agentic Intelligence Layer", "#EDE9FE", "#7C3AED", "Query Expansion Agent | Research Gap Engine | Review Matrix Synthesizer | Groq LLaMA-3.3 & DeepSeek", 2.6),
        ("Layer 2: Extraction & Vector Indexing Layer", "#DCFCE7", "#16A34A", "PyMuPDF Document Parser | sentence-transformers (all-MiniLM-L6-v2) | Local FAISS L2 Vector Index", 1.3),
        ("Layer 1: External Data & Services Layer", "#FCE7F3", "#DB2777", "ArXiv Search API | Semantic Scholar Graph API | Microsoft EdgeTTS Speech Cloud | Local File Storage", 0.0)
    ]

    for title, fc, ec, desc, y_pos in layers:
        ax.add_patch(patches.FancyBboxPatch((0.5, y_pos + 0.1), 9.0, 1.0, boxstyle="round,pad=0.08", fc=fc, ec=ec, lw=1.5))
        ax.text(5.0, y_pos + 0.8, title, ha='center', va='center', fontsize=10, fontweight='bold', color="#1E293B")
        ax.text(5.0, y_pos + 0.4, desc, ha='center', va='center', fontsize=8.5, color="#334155")

    plt.tight_layout()
    plt.savefig('assets/diagrams/fig5_1_layered_architecture.png', bbox_inches='tight', dpi=300)
    plt.close()

# 5. Figure 5.2: Tool Calling Loop Flowchart
def gen_fig5_2():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')
    fig.patch.set_facecolor('#ffffff')

    steps = [
        (1.0, 2.5, "User Query /\nVoice Input", "#E0F2FE", "#0284C7"),
        (3.0, 2.5, "Query Expansion\nAgent", "#FEF3C7", "#D97706"),
        (5.0, 3.5, "ArXiv / S2\nAPI Calls", "#DCFCE7", "#16A34A"),
        (5.0, 1.5, "Local PDF RAG\nFAISS Search", "#EDE9FE", "#7C3AED"),
        (7.0, 2.5, "LLM Synthesis\n& Gap Engine", "#FCE7F3", "#DB2777"),
        (9.0, 2.5, "Export Report\n(.docx / LaTeX)", "#CFFAFE", "#0891B2")
    ]

    for x, y, text, fc, ec in steps:
        ax.add_patch(patches.FancyBboxPatch((x - 0.75, y - 0.5), 1.5, 1.0, boxstyle="round,pad=0.08", fc=fc, ec=ec, lw=1.4))
        ax.text(x, y, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color="#1E293B")

    arrow = dict(facecolor='#475569', edgecolor='#475569', width=1.2, headwidth=5, shrink=0.08)
    ax.annotate('', xy=(2.25, 2.5), xytext=(1.75, 2.5), arrowprops=arrow)
    ax.annotate('', xy=(4.25, 3.5), xytext=(3.75, 2.8), arrowprops=arrow)
    ax.annotate('', xy=(4.25, 1.5), xytext=(3.75, 2.2), arrowprops=arrow)
    ax.annotate('', xy=(6.25, 2.8), xytext=(5.75, 3.5), arrowprops=arrow)
    ax.annotate('', xy=(6.25, 2.2), xytext=(5.75, 1.5), arrowprops=arrow)
    ax.annotate('', xy=(8.25, 2.5), xytext=(7.75, 2.5), arrowprops=arrow)

    plt.tight_layout()
    plt.savefig('assets/diagrams/fig5_2_agent_loop.png', bbox_inches='tight', dpi=300)
    plt.close()

# 6. Figure 5.5: Voice Agent Flowchart
def gen_fig5_5():
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.5)
    ax.axis('off')
    fig.patch.set_facecolor('#ffffff')

    v_steps = [
        (1.2, 2.25, "User Speech\n(Microphone)", "#E0F2FE", "#0284C7"),
        (3.4, 2.25, "Web Speech API\nSpeech-to-Text", "#FEF3C7", "#D97706"),
        (5.6, 2.25, "Salim AI Agent\nContext Fusion", "#EDE9FE", "#7C3AED"),
        (7.8, 2.25, "EdgeTTS Engine\nAudio Stream", "#DCFCE7", "#16A34A"),
        (9.4, 2.25, "Voice Output\n(Speaker)", "#FCE7F3", "#DB2777")
    ]

    for x, y, text, fc, ec in v_steps:
        ax.add_patch(patches.FancyBboxPatch((x - 0.8, y - 0.6), 1.6, 1.2, boxstyle="round,pad=0.08", fc=fc, ec=ec, lw=1.4))
        ax.text(x, y, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color="#1E293B")

    arrow = dict(facecolor='#475569', edgecolor='#475569', width=1.2, headwidth=5, shrink=0.08)
    ax.annotate('', xy=(2.6, 2.25), xytext=(2.0, 2.25), arrowprops=arrow)
    ax.annotate('', xy=(4.8, 2.25), xytext=(4.2, 2.25), arrowprops=arrow)
    ax.annotate('', xy=(7.0, 2.25), xytext=(6.4, 2.25), arrowprops=arrow)
    ax.annotate('', xy=(8.6, 2.25), xytext=(8.4, 2.25), arrowprops=arrow)

    plt.tight_layout()
    plt.savefig('assets/diagrams/fig5_5_voice_flow.png', bbox_inches='tight', dpi=300)
    plt.close()

if __name__ == '__main__':
    gen_fig1_1()
    gen_fig2_1()
    gen_fig3_1()
    gen_fig5_1()
    gen_fig5_2()
    gen_fig5_5()
    print("[SUCCESS] All 6 high-res architecture diagrams and flowcharts generated in assets/diagrams/")
