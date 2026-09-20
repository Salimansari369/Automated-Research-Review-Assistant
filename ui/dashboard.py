import gradio as gr
from typing import Dict, Any, List
from models.session import ResearchSession
from ui.assets import HERO_ANIME_IMG, USER_AVATAR_IMG, RESEARCHER_WALKER_IMG
from ui.components import (
    render_stat_cards_html, render_pipeline_html,
    render_uploaded_papers_summary, render_top_papers_card,
    render_gap_intelligence_card, render_ai_insight_card,
    render_sources_info_cards_html
)

def render_top_walker_html() -> str:
    return f"""
    <div class="top-walker-track">
      <div class="walker-track-glow"></div>
      <div class="walker-character-box">
        <div class="walker-status-pill">
          <span class="walker-sparkle">🔍</span>
          <span class="walker-status-text">Autonomous Research Scout Active...</span>
        </div>
        <img src="{RESEARCHER_WALKER_IMG}" class="walker-anime-character" alt="Research Scout" />
      </div>
    </div>
    """

def render_hero_banner_html(topic: str = "Space Communication Networks") -> str:
    topic_clean = topic if topic and str(topic).strip() else "Space Communication Networks"
    return f"""
    <div class="hero-banner-card">
      <div class="user-profile-badge-top">
        <img src="{USER_AVATAR_IMG}" class="user-avatar-circle" alt="User" />
        <div class="user-profile-info">
          <div class="user-name">Researcher</div>
          <span class="user-badge-plan">Pro Plan</span>
        </div>
      </div>
      <div class="hero-banner-row">
        <div class="hero-banner-left">
          <div class="hero-header-text">
            <div class="hero-greeting">Welcome back, Researcher! <span>👋</span></div>
            <div class="hero-headline">
              Let's explore the future of <span class="highlight-purple">Agentic AI</span> for <span class="highlight-purple">{topic_clean}</span>.
            </div>
            <div class="hero-subtitle">Transform hundreds of papers into meaningful insights.</div>
          </div>
        </div>
        <div class="hero-banner-right">
          <div class="hero-right-box">
            <img src="{HERO_ANIME_IMG}" class="hero-anime-img-full" alt="Space Researcher" />
          </div>
        </div>
      </div>
    </div>
    """

def create_dashboard_view(initial_session: ResearchSession = None):
    init_topic = initial_session.research_topic if initial_session else "Agentic AI for Autonomous Space Communication Networks"
    init_from = initial_session.year_start if initial_session else 2020
    init_to = initial_session.year_end if initial_session else 2026
    init_sources = initial_session.selected_sources if initial_session else ["Semantic Scholar", "OpenAlex", "Crossref"]
    init_max = initial_session.max_papers if initial_session else 20

    with gr.Column(elem_classes=["dashboard-view"]):

        # ── TOP WALKING RESEARCHER SCOUT ANIMATION ────────────────────────
        top_walker_html = gr.HTML(value=render_top_walker_html())

        # ── SOURCES CONFIGURATION MODAL / POPUP ────────────────────────────
        with gr.Column(visible=False, elem_classes=["sources-modal-backdrop"]) as sources_modal:
            with gr.Column(elem_classes=["sources-modal-box"]):
                with gr.Row(elem_classes=["sources-modal-header"]):
                    gr.HTML("""
                    <div class="modal-title-area">
                        <div class="modal-title">🌐 Academic Repositories & Search Connectors</div>
                        <div class="modal-subtitle">Enable or disable academic registries for multi-source concurrent literature search</div>
                    </div>
                    """)
                    close_sources_modal_btn = gr.Button("✕", elem_classes=["btn-modal-close-icon"])
                
                modal_sources_checkbox = gr.CheckboxGroup(
                    choices=["Semantic Scholar", "OpenAlex", "Crossref", "arXiv", "Tavily"],
                    value=init_sources,
                    label="SELECTED ACTIVE REPOSITORIES",
                    elem_classes=["modal-sources-checklist"]
                )

                gr.HTML(render_sources_info_cards_html())

                with gr.Row(elem_classes=["sources-modal-actions"]):
                    close_sources_cancel_btn = gr.Button("Cancel", elem_classes=["btn-modal-cancel"])
                    apply_sources_modal_btn = gr.Button("✓ Save & Apply Sources", variant="primary", elem_classes=["btn-modal-apply"])

        # ── 1. MAIN HERO BANNER CARD (Target height: ~180px, single clean HTML card) ──
        hero_banner_html = gr.HTML(value=render_hero_banner_html(init_topic))

        # ── 2. RESEARCH CONTROL CARD (Target height: ~155px, separate card) ──
        with gr.Column(elem_classes=["research-control-card"]):
            # Row 1: Full-width topic input
            topic_input = gr.Textbox(
                label="RESEARCH TOPIC",
                value=init_topic,
                placeholder="Enter any research topic...",
                lines=1,
                elem_classes=["hero-topic-textbox"]
            )


            # Row 2: YEAR RANGE | SOURCES | MAX PAPERS | START REVIEW
            with gr.Row(elem_classes=["hero-filter-subrow"], equal_height=False):
                # 1. YEAR RANGE
                with gr.Column(scale=2, min_width=180, elem_classes=["filter-group-col", "filter-col-years"]):
                    gr.HTML('<div class="filter-header-label">YEAR RANGE</div>')
                    with gr.Row(elem_classes=["years-flex-row"]):
                        year_from = gr.Dropdown(
                            choices=list(range(2015, 2031)),
                            value=init_from,
                            scale=1,
                            allow_custom_value=False,
                            show_label=False,
                            container=False,
                            elem_classes=["year-select-box"]
                        )
                        gr.HTML('<span class="year-hyphen">-</span>')
                        year_to = gr.Dropdown(
                            choices=list(range(2015, 2031)),
                            value=init_to,
                            scale=1,
                            allow_custom_value=False,
                            show_label=False,
                            container=False,
                            elem_classes=["year-select-box"]
                        )

                # 2. SOURCES
                with gr.Column(scale=3, min_width=210, elem_classes=["filter-group-col", "filter-col-sources"]):
                    with gr.Row(elem_classes=["sources-header-row"]):
                        gr.HTML('<div class="filter-header-label">SOURCES</div>')
                        open_sources_modal_btn = gr.Button("⚙️ Manage", elem_classes=["btn-sources-config-icon"])
                    sources_select = gr.CheckboxGroup(
                        choices=["Semantic Scholar", "OpenAlex", "Crossref", "arXiv", "Tavily"],
                        value=init_sources,
                        show_label=False,
                        container=False,
                        elem_classes=["sources-chips-group"]
                    )

                # 3. MAX PAPERS
                with gr.Column(scale=1, min_width=85, elem_classes=["filter-group-col", "filter-col-max"]):
                    gr.HTML('<div class="filter-header-label">MAX PAPERS</div>')
                    max_papers_input = gr.Dropdown(
                        choices=[10, 15, 20, 30, 40, 50],
                        value=init_max,
                        show_label=False,
                        container=False,
                        elem_classes=["max-select-box"]
                    )

                # 4. START REVIEW BUTTON
                with gr.Column(scale=3, min_width=220, elem_classes=["filter-group-col", "filter-col-btn"]):
                    gr.HTML('<div class="filter-header-label filter-label-empty">&nbsp;</div>')
                    start_review_btn = gr.Button(
                        "🚀 Start Literature Review",
                        variant="primary",
                        elem_classes=["btn-start-review-main"]
                    )

        # ── 3. STATISTICS (~125px) ────────────────────────────────────────────
        init_stats = (
            render_stat_cards_html(
                initial_session.papers_found_count,
                initial_session.highly_relevant_count,
                initial_session.gaps_count,
                initial_session.review_coverage_percent
            ) if initial_session else render_stat_cards_html(42, 18, 7, 84)
        )
        stats_html = gr.HTML(value=init_stats)

        # ── 4. PIPELINE (55%) + UPLOAD (45%) (~195px) ─────────────────────────
        init_pipe = (
            render_pipeline_html(
                initial_session.pipeline_progress,
                initial_session.pipeline_status_text,
                initial_session.pipeline_status
            ) if initial_session and initial_session.pipeline_progress > 0 else render_pipeline_html(68, "Analyzing papers... 68%")
        )
        with gr.Row(elem_classes=["middle-dashboard-row"], equal_height=True):
            with gr.Column(scale=55, elem_classes=["pipeline-col"]):
                pipeline_html = gr.HTML(value=init_pipe)
            with gr.Column(scale=45, elem_classes=["upload-col", "upload-card-wrapper"]):
                with gr.Row(elem_classes=["upload-inner-split"], equal_height=True):
                    with gr.Column(scale=50, elem_classes=["upload-drop-col"]):
                        dashboard_file_upload = gr.File(
                            label="☁️ Drop PDF, DOCX, or TXT files here",
                            file_count="multiple",
                            file_types=[".pdf", ".docx", ".doc", ".txt", ".md"],
                            container=False,
                            show_label=False,
                            elem_classes=["dropzone-box-tight"]
                        )
                        gr.HTML("""<div class="upload-btn-row">
                          <button class="upload-action-btn" onclick="
                            var inp = this.closest('.upload-drop-col').querySelector('input[type=file]');
                            if(inp) inp.click();
                          ">📂 Upload Documents</button>
                        </div>""")

                    with gr.Column(scale=50, elem_classes=["upload-list-col"]):
                        upload_summary_html = gr.HTML(value=render_uploaded_papers_summary(initial_session.uploaded_papers if initial_session else []))

        # ── 5. LOWER CONTENT (3 Expanded Columns: Full Width ~310px) ─────────
        init_top_papers = render_top_papers_card(
            initial_session.unified_papers[:4] if initial_session else [],
            init_topic
        )
        init_gaps = render_gap_intelligence_card(
            initial_session.detected_gaps if initial_session else [],
            init_topic
        )
        init_insight = render_ai_insight_card(
            initial_session.ai_summary if initial_session else "",
            init_topic
        )
        with gr.Row(elem_classes=["bottom-dashboard-row"], equal_height=True):
            with gr.Column(scale=33):
                top_papers_html = gr.HTML(value=init_top_papers)
            with gr.Column(scale=34):
                gaps_html = gr.HTML(value=init_gaps)
            with gr.Column(scale=33):
                ai_insight_html = gr.HTML(value=init_insight)


        # ── 6. BOTTOM CTA BANNER ──────────────────────────────────────────────
        with gr.Row(elem_classes=["footer-cta-row"]):
            gr.HTML("""
            <div class="footer-cta-left">
              <span class="footer-sparkle">✨</span>
              <span><strong>From thousands of papers to one clear direction.</strong> LiteratureAI turns research chaos into clarity.</span>
            </div>
            """)
            footer_generate_btn = gr.Button(
                "🚀 Generate Literature Review →",
                variant="primary",
                elem_classes=["btn-primary-gradient", "btn-footer-cta"]
            )

    return {
        "topic_input": topic_input,
        "year_from": year_from,
        "year_to": year_to,
        "sources_select": sources_select,
        "open_sources_modal_btn": open_sources_modal_btn,
        "sources_modal": sources_modal,
        "modal_sources_checkbox": modal_sources_checkbox,
        "close_sources_modal_btn": close_sources_modal_btn,
        "close_sources_cancel_btn": close_sources_cancel_btn,
        "apply_sources_modal_btn": apply_sources_modal_btn,
        "max_papers_input": max_papers_input,
        "start_review_btn": start_review_btn,
        "stats_html": stats_html,
        "pipeline_html": pipeline_html,
        "dashboard_file_upload": dashboard_file_upload,
        "upload_summary_html": upload_summary_html,
        "top_papers_html": top_papers_html,
        "gaps_html": gaps_html,
        "ai_insight_html": ai_insight_html,
        "hero_banner_html": hero_banner_html,
        "footer_generate_btn": footer_generate_btn
    }

