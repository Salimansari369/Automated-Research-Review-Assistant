import os
import gradio as gr
from typing import List, Dict, Any, Tuple
from datetime import datetime

from config.settings import (
    APP_NAME, APP_TAGLINE, DEFAULT_TOPIC, DEFAULT_YEAR_START,
    DEFAULT_YEAR_END, DEFAULT_MAX_PAPERS, EXPORTS_DIR
)
from models.session import ResearchSession
from models.paper import Paper
from services.search_aggregator import SearchAggregator
from services.pdf_processor import PDFProcessor
from services.analysis_service import AnalysisService
from services.gap_detector import GapDetector
from services.review_generator import ReviewGenerator
from services.relevance import RelevanceScorer
from exporters.docx_exporter import DocxExporter
from exporters.csv_exporter import CsvExporter

from ui.theme import get_literature_theme
from ui.styles import CUSTOM_CSS
from ui.sidebar import create_sidebar_view
from ui.dashboard import create_dashboard_view, render_hero_banner_html
from ui.search_page import create_search_view, render_search_results_cards
from ui.upload_page import create_upload_view, render_uploaded_table
from ui.analysis_page import create_analysis_view, render_analysis_cards
from ui.comparison_page import create_comparison_view, render_comparison_table, generate_comparison_charts
from ui.gaps_page import create_gaps_view, render_detailed_gaps
from ui.review_page import create_review_view
from ui.chat_page import create_chat_view, render_salim_sidebar_html, INITIAL_WELCOME_MESSAGE, VOICE_SCRIPT_HEAD
from services.chat_rag_service import ChatRAGService
from services.transcription_service import TranscriptionService
from ui.components import (
    render_stat_cards_html, render_pipeline_html, render_uploaded_papers_summary,
    render_top_papers_card, render_gap_intelligence_card, render_ai_insight_card,
    render_sidebar_html, render_sidebar_footer_html
)
from utils.logging_config import logger

def build_app():
    # Load persistent session from disk if available
    initial_session = ResearchSession.load_from_disk()

    with gr.Blocks(title=f"{APP_NAME} • {APP_TAGLINE}") as app:

        # Centralized Session State seeded from disk
        session = gr.State(initial_session)

        with gr.Row(elem_classes=["app-container"]):
            # Sidebar Column
            sidebar_ui = create_sidebar_view()

            # Main Content Column
            with gr.Column(scale=1, elem_classes=["main-content-column"]):
                
                # View Containers
                with gr.Column(visible=True) as view_dashboard:
                    dash_ui = create_dashboard_view(initial_session)

                with gr.Column(visible=False) as view_search:
                    search_ui = create_search_view()

                with gr.Column(visible=False) as view_upload:
                    upload_ui = create_upload_view(initial_session.uploaded_papers)


                with gr.Column(visible=False) as view_analysis:
                    analysis_ui = create_analysis_view()

                with gr.Column(visible=False) as view_comparison:
                    comparison_ui = create_comparison_view()

                with gr.Column(visible=False) as view_gaps:
                    gaps_ui = create_gaps_view()

                with gr.Column(visible=False) as view_review:
                    review_ui = create_review_view()

                with gr.Column(visible=False) as view_chat:
                    chat_ui = create_chat_view()

        # Navigation Router
        def route_view(selected_nav: str, sess: ResearchSession):
            nav = str(selected_nav or "")
            papers = sess.unified_papers if sess else []
            papers_cnt = len(papers)
            cur_topic = sess.research_topic if sess else "Active Workspace"
            profile_html = render_salim_sidebar_html(papers_cnt, cur_topic)
            fig1, fig2 = generate_comparison_charts(papers)
            review_md = (sess.literature_review.get("markdown", "") if (sess and sess.literature_review) else "*Click 'Synthesize Complete Literature Review' to build your document.*")
            review_raw = sess.literature_review.get("markdown", "") if (sess and sess.literature_review) else ""
            
            return (
                gr.update(visible="Dashboard" in nav),
                gr.update(visible="Search" in nav),
                gr.update(visible="Upload" in nav),
                gr.update(visible="Analysis" in nav),
                gr.update(visible="Comparison" in nav),
                gr.update(visible="Gaps" in nav),
                gr.update(visible="Review" in nav),
                gr.update(visible="Chat" in nav),
                render_analysis_cards(papers),
                render_detailed_gaps(sess.detected_gaps if sess else []),
                render_comparison_table(papers),
                fig1,
                fig2,
                review_md,
                review_raw,
                render_stat_cards_html(sess.papers_found_count if sess else 0, sess.highly_relevant_count if sess else 0, sess.gaps_count if sess else 0, sess.review_coverage_percent if sess else 0),
                render_top_papers_card(papers[:4], cur_topic),
                render_gap_intelligence_card(sess.detected_gaps if sess else [], cur_topic),
                render_ai_insight_card(sess.ai_summary if sess else "", cur_topic),
                render_uploaded_table(sess.uploaded_papers if sess else []),
                render_uploaded_papers_summary(sess.uploaded_papers if sess else []),
                profile_html
            )


        sidebar_ui["nav_selector"].change(
            fn=route_view,
            inputs=[sidebar_ui["nav_selector"], session],
            outputs=[
                view_dashboard, view_search, view_upload, view_analysis,
                view_comparison, view_gaps, view_review, view_chat,
                analysis_ui["analysis_container"],
                gaps_ui["gaps_container"],
                comparison_ui["comparison_table_html"],
                comparison_ui["chart_scatter"],
                comparison_ui["chart_hist"],
                review_ui["review_markdown_display"],
                review_ui["review_editor"],
                dash_ui["stats_html"],
                dash_ui["top_papers_html"],
                dash_ui["gaps_html"],
                dash_ui["ai_insight_html"],
                upload_ui["uploaded_table_html"],
                dash_ui["upload_summary_html"],
                chat_ui["salim_profile_display"]
            ]
        )



        # -------------------------------------------------------------
        # CORE WORKFLOW: Start Full Literature Review from Dashboard
        # -------------------------------------------------------------
        def run_full_literature_review(
            sess: ResearchSession,
            topic: str,
            year_from: int,
            year_to: int,
            sources: List[str],
            max_papers: int,
            current_chat: List[Any]
        ):
            logger.info(f"Starting Full Literature Review Workflow for: '{topic}'")
            sess.research_topic = topic
            sess.year_start = int(year_from)
            sess.year_end = int(year_to)
            sess.selected_sources = sources
            sess.max_papers = int(max_papers)

            # Step 1: Search Papers
            sess.set_pipeline(1, 20, "Searching academic databases...", {
                "search": "active", "dedup": "pending", "rank": "pending",
                "analysis": "pending", "gaps": "pending", "review": "pending"
            })
            papers, api_status, errors = SearchAggregator.execute_search(
                topic=topic,
                start_year=sess.year_start,
                end_year=sess.year_end,
                sources=sources,
                max_papers=sess.max_papers
            )
            sess.searched_papers = papers
            sess.api_status.update(api_status)
            sess.errors.extend(errors)

            # Step 2 & 3: Deduplicate & Rank Relevance
            sess.set_pipeline(3, 45, "Deduplicating and ranking relevance...", {
                "search": "completed", "dedup": "completed", "rank": "active",
                "analysis": "pending", "gaps": "pending", "review": "pending"
            })
            unified = sess.unified_papers
            ranked = RelevanceScorer.score_papers(unified, topic)

            # Step 4: AI Analysis
            sess.set_pipeline(4, 68, "Analyzing papers...", {
                "search": "completed", "dedup": "completed", "rank": "completed",
                "analysis": "active", "gaps": "pending", "review": "pending"
            })
            for p in ranked[:8]:
                if not p.analysis:
                    AnalysisService.analyze_paper(p)

            # Step 5: Detect Gaps
            sess.set_pipeline(5, 85, "Synthesizing research gap intelligence...", {
                "search": "completed", "dedup": "completed", "rank": "completed",
                "analysis": "completed", "gaps": "active", "review": "pending"
            })
            gaps = GapDetector.detect_gaps(ranked[:10], topic)
            sess.detected_gaps = gaps

            # Step 6: Generate Review
            sess.set_pipeline(6, 100, "Review complete! Literature review synthesized.", {
                "search": "completed", "dedup": "completed", "rank": "completed",
                "analysis": "completed", "gaps": "completed", "review": "completed"
            })
            review_data = ReviewGenerator.generate_review(topic, ranked[:10], gaps)
            sess.literature_review = review_data
            sess.ai_summary = (
                f"Synthesized review on {topic} based on {len(ranked)} publications. "
                f"Identified {len(gaps)} key empirical gaps across autonomous routing, heterogeneous consensus, and hardware validation."
            )

            # HTML representations
            stats_h = render_stat_cards_html(
                sess.papers_found_count,
                sess.highly_relevant_count,
                sess.gaps_count,
                sess.review_coverage_percent
            )
            pipe_h = render_pipeline_html(100, "Literature review complete! 100%", sess.pipeline_status)
            top_h = render_top_papers_card(ranked[:4], topic)
            gaps_h = render_gap_intelligence_card(gaps, topic)
            insight_h = render_ai_insight_card(sess.ai_summary, topic)
            sidebar_h = render_sidebar_footer_html(sess.api_status)
            search_cards_h = render_search_results_cards(ranked)
            analysis_cards_h = render_analysis_cards(ranked)
            gaps_detail_h = render_detailed_gaps(gaps)
            comp_table_h = render_comparison_table(ranked[:8])
            fig1, fig2 = generate_comparison_charts(ranked[:8])

            # Synchronize Salim Chat & Profile
            top_title = ranked[0].title if ranked else topic
            top_key = ranked[0].citation_key if ranked else "Ref"
            chat_notice = (
                f"**Literature Review Synchronized**\n\n"
                f"I have indexed and analyzed **{len(ranked)} papers** for **\"{topic}\"**.\n"
                f"- **Primary Paper:** [{top_key}] *\"{top_title}\"*\n"
                f"- **Identified Gaps:** {len(gaps)} critical research gap(s) found.\n\n"
                f"I am ready for your questions. You can ask me to compare methodologies, inspect limitations, or cite evidence from these papers."
            )
            chat_hist = list(current_chat or INITIAL_WELCOME_MESSAGE)
            chat_hist.append({"role": "assistant", "content": chat_notice})
            profile_h = render_salim_sidebar_html(len(ranked), topic)

            # Auto-persist session to disk
            sess.save_to_disk()

            return (
                sess,
                stats_h,
                pipe_h,
                top_h,
                gaps_h,
                insight_h,
                sidebar_h,
                search_cards_h,
                analysis_cards_h,
                gaps_detail_h,
                comp_table_h,
                fig1,
                fig2,
                review_data.get("markdown", ""),
                review_data.get("markdown", ""),
                chat_hist,
                profile_h
            )

        dash_ui["start_review_btn"].click(
            fn=run_full_literature_review,
            inputs=[
                session,
                dash_ui["topic_input"],
                dash_ui["year_from"],
                dash_ui["year_to"],
                dash_ui["sources_select"],
                dash_ui["max_papers_input"],
                chat_ui["chatbot"]
            ],
            outputs=[
                session,
                dash_ui["stats_html"],
                dash_ui["pipeline_html"],
                dash_ui["top_papers_html"],
                dash_ui["gaps_html"],
                dash_ui["ai_insight_html"],
                sidebar_ui["sidebar_status_display"],
                search_ui["search_results_container"],
                analysis_ui["analysis_container"],
                gaps_ui["gaps_container"],
                comparison_ui["comparison_table_html"],
                comparison_ui["chart_scatter"],
                comparison_ui["chart_hist"],
                review_ui["review_markdown_display"],
                review_ui["review_editor"],
                chat_ui["chatbot"],
                chat_ui["salim_profile_display"]
            ]
        )


        # Sources Configuration Modal Handlers
        dash_ui["open_sources_modal_btn"].click(
            fn=lambda current_srcs: (gr.update(visible=True), current_srcs),
            inputs=[dash_ui["sources_select"]],
            outputs=[dash_ui["sources_modal"], dash_ui["modal_sources_checkbox"]]
        )

        dash_ui["close_sources_modal_btn"].click(
            fn=lambda: gr.update(visible=False),
            inputs=[],
            outputs=[dash_ui["sources_modal"]]
        )

        dash_ui["close_sources_cancel_btn"].click(
            fn=lambda: gr.update(visible=False),
            inputs=[],
            outputs=[dash_ui["sources_modal"]]
        )

        dash_ui["apply_sources_modal_btn"].click(
            fn=lambda sel: (gr.update(visible=False), sel),
            inputs=[dash_ui["modal_sources_checkbox"]],
            outputs=[dash_ui["sources_modal"], dash_ui["sources_select"]]
        )

        # -------------------------------------------------------------
        # DASHBOARD FILE UPLOAD HANDLER (Full Automated Multi-Doc Pipeline)
        # -------------------------------------------------------------
        def handle_dashboard_file_upload(sess: ResearchSession, files: List[Any], current_chat: List[Any]):
            cur_topic = sess.research_topic if (sess and sess.research_topic) else "Space Communication Networks"
            if not files:
                papers_cnt = len(sess.unified_papers)
                fig1, fig2 = generate_comparison_charts(sess.unified_papers)
                return (
                    sess,
                    cur_topic,
                    render_hero_banner_html(cur_topic),
                    cur_topic,
                    render_uploaded_papers_summary(sess.uploaded_papers),
                    render_uploaded_table(sess.uploaded_papers),
                    render_stat_cards_html(sess.papers_found_count, sess.highly_relevant_count, sess.gaps_count, sess.review_coverage_percent),
                    render_pipeline_html(100 if sess.unified_papers else 68, "Session active", sess.pipeline_status),
                    render_top_papers_card(sess.unified_papers[:4]),
                    render_gap_intelligence_card(sess.detected_gaps),
                    render_ai_insight_card(sess.ai_summary),
                    render_analysis_cards(sess.unified_papers),
                    render_detailed_gaps(sess.detected_gaps),
                    render_comparison_table(sess.unified_papers),
                    fig1, fig2,
                    sess.literature_review.get("markdown", "") if sess.literature_review else "",
                    sess.literature_review.get("markdown", "") if sess.literature_review else "",
                    current_chat or INITIAL_WELCOME_MESSAGE,
                    render_salim_sidebar_html(papers_cnt, cur_topic)
                )

            # 1. Parse and extract each uploaded document
            last_extracted_title = ""
            for f in files:
                file_path = f.name if hasattr(f, "name") else str(f)
                paper, warning = PDFProcessor.process_document(file_path)
                if paper:
                    # Run AI analysis immediately on uploaded document
                    AnalysisService.analyze_paper(paper)
                    sess.add_uploaded_paper(paper)
                    if paper.title and len(paper.title.strip()) > 3:
                        last_extracted_title = paper.title.strip()

            # Set research topic directly to uploaded paper's extracted title
            if last_extracted_title:
                sess.research_topic = last_extracted_title
            
            active_topic = sess.research_topic or "Space Communication Networks"

            # 2. Re-score and rank all unified papers
            ranked = RelevanceScorer.score_papers(sess.unified_papers, active_topic)

            # 3. Detect research gaps across all unified papers
            gaps = GapDetector.detect_gaps(sess.unified_papers, active_topic)
            sess.detected_gaps = gaps

            # 4. Generate AI synthesis and literature review
            review_data = ReviewGenerator.generate_review(active_topic, sess.unified_papers[:10], gaps)
            sess.literature_review = review_data
            sess.ai_summary = (
                f"Synthesized comprehensive review based on {len(sess.unified_papers)} documents for \"{active_topic}\". "
                f"Identified {len(gaps)} critical empirical gaps across the corpus."
            )

            # 5. Set pipeline status
            sess.set_pipeline(6, 100, f"Analysis & comparison complete ({len(sess.unified_papers)} documents) 100%", {
                "search": "completed", "dedup": "completed", "rank": "completed",
                "analysis": "completed", "gaps": "completed", "review": "completed"
            })

            # 6. Render all updated components
            summary_h = render_uploaded_papers_summary(sess.uploaded_papers)
            table_h = render_uploaded_table(sess.uploaded_papers)
            stats_h = render_stat_cards_html(
                sess.papers_found_count,
                sess.highly_relevant_count,
                sess.gaps_count,
                sess.review_coverage_percent
            )
            pipe_h = render_pipeline_html(100, f"Analysis & comparison complete ({len(sess.unified_papers)} documents) 100%", sess.pipeline_status)
            top_h = render_top_papers_card(sess.unified_papers[:4], active_topic)
            gaps_h = render_gap_intelligence_card(gaps, active_topic)
            insight_h = render_ai_insight_card(sess.ai_summary, active_topic)
            analysis_cards_h = render_analysis_cards(sess.unified_papers)
            gaps_detail_h = render_detailed_gaps(gaps)
            comp_table_h = render_comparison_table(sess.unified_papers)
            fig1, fig2 = generate_comparison_charts(sess.unified_papers)
            review_md = review_data.get("markdown", "")
            hero_h = render_hero_banner_html(active_topic)

            # Salim Chat Sync Notification
            count = len(sess.unified_papers)
            uploaded_titles = "\n".join([f"- *\"{p.title}\"*" for p in sess.uploaded_papers[-len(files):]]) if files else ""
            chat_notice = (
                f"**Documents Uploaded, Analyzed & Compared**\n\n"
                f"Successfully parsed, extracted, and compared **{len(files)} document(s)**:\n"
                f"{uploaded_titles}\n\n"
                f"Active research topic set to: **\"{active_topic}\"**.\n"
                f"Total active research collection: **{count} documents**.\n"
                f"- **AI Analysis:** Structured problem, methodology, dataset, and limitations extracted.\n"
                f"- **Comparative Analytics:** Scatter plots and year distributions updated.\n"
                f"- **Research Gaps:** {len(gaps)} collective void(s) synthesized.\n\n"
                f"I am ready to answer any questions about these uploaded documents!"
            )
            chat_hist = list(current_chat or INITIAL_WELCOME_MESSAGE)
            chat_hist.append({"role": "assistant", "content": chat_notice})
            profile_h = render_salim_sidebar_html(count, active_topic)

            # Auto-persist session to disk
            sess.save_to_disk()

            return (
                sess,
                active_topic,
                hero_h,
                active_topic,
                summary_h,
                table_h,
                stats_h,
                pipe_h,
                top_h,
                gaps_h,
                insight_h,
                analysis_cards_h,
                gaps_detail_h,
                comp_table_h,
                fig1,
                fig2,
                review_md,
                review_md,
                chat_hist,
                profile_h
            )

        dash_ui["dashboard_file_upload"].upload(
            fn=handle_dashboard_file_upload,
            inputs=[session, dash_ui["dashboard_file_upload"], chat_ui["chatbot"]],
            outputs=[
                session,
                dash_ui["topic_input"],
                dash_ui["hero_banner_html"],
                search_ui["search_topic_input"],
                dash_ui["upload_summary_html"],
                upload_ui["uploaded_table_html"],
                dash_ui["stats_html"],
                dash_ui["pipeline_html"],
                dash_ui["top_papers_html"],
                dash_ui["gaps_html"],
                dash_ui["ai_insight_html"],
                analysis_ui["analysis_container"],
                gaps_ui["gaps_container"],
                comparison_ui["comparison_table_html"],
                comparison_ui["chart_scatter"],
                comparison_ui["chart_hist"],
                review_ui["review_markdown_display"],
                review_ui["review_editor"],
                chat_ui["chatbot"],
                chat_ui["salim_profile_display"]
            ]
        )

        # -------------------------------------------------------------
        # DEDICATED UPLOAD PAGE HANDLERS (Full Automated Multi-Doc Pipeline)
        # -------------------------------------------------------------
        def handle_upload_page_files(sess: ResearchSession, files: List[Any], current_chat: List[Any]):
            cur_topic = sess.research_topic if (sess and sess.research_topic) else "Space Communication Networks"
            if not files:
                papers_cnt = len(sess.unified_papers)
                fig1, fig2 = generate_comparison_charts(sess.unified_papers)
                return (
                    sess,
                    "No files selected.",
                    render_uploaded_table(sess.uploaded_papers),
                    "",
                    cur_topic,
                    render_hero_banner_html(cur_topic),
                    cur_topic,
                    render_uploaded_papers_summary(sess.uploaded_papers),
                    render_stat_cards_html(sess.papers_found_count, sess.highly_relevant_count, sess.gaps_count, sess.review_coverage_percent),
                    render_pipeline_html(100 if sess.unified_papers else 68, "Session active", sess.pipeline_status),
                    render_top_papers_card(sess.unified_papers[:4]),
                    render_gap_intelligence_card(sess.detected_gaps),
                    render_ai_insight_card(sess.ai_summary),
                    render_analysis_cards(sess.unified_papers),
                    render_detailed_gaps(sess.detected_gaps),
                    render_comparison_table(sess.unified_papers),
                    fig1, fig2,
                    sess.literature_review.get("markdown", "") if sess.literature_review else "",
                    sess.literature_review.get("markdown", "") if sess.literature_review else "",
                    current_chat or INITIAL_WELCOME_MESSAGE,
                    render_salim_sidebar_html(papers_cnt, cur_topic)
                )

            preview_text = ""
            last_extracted_title = ""
            for f in files:
                file_path = f.name if hasattr(f, "name") else str(f)
                paper, warning = PDFProcessor.process_document(file_path)
                if paper:
                    AnalysisService.analyze_paper(paper)
                    sess.add_uploaded_paper(paper)
                    if paper.title and len(paper.title.strip()) > 3:
                        last_extracted_title = paper.title.strip()
                    if not preview_text:
                        preview_text = f"Title: {paper.title}\nDOI: {paper.doi}\n\n" + (paper.raw_text[:2000] or paper.abstract)

            if last_extracted_title:
                sess.research_topic = last_extracted_title

            active_topic = sess.research_topic or "Space Communication Networks"

            # Re-score and rank all unified papers
            ranked = RelevanceScorer.score_papers(sess.unified_papers, active_topic)

            # Detect research gaps across all unified papers
            gaps = GapDetector.detect_gaps(sess.unified_papers, active_topic)
            sess.detected_gaps = gaps

            # Generate AI review
            review_data = ReviewGenerator.generate_review(active_topic, sess.unified_papers[:10], gaps)
            sess.literature_review = review_data
            sess.ai_summary = (
                f"Synthesized comprehensive review based on {len(sess.unified_papers)} documents for \"{active_topic}\". "
                f"Identified {len(gaps)} critical empirical gaps across the corpus."
            )

            sess.set_pipeline(6, 100, f"Analysis & comparison complete ({len(sess.unified_papers)} documents) 100%", {
                "search": "completed", "dedup": "completed", "rank": "completed",
                "analysis": "completed", "gaps": "completed", "review": "completed"
            })

            table_h = render_uploaded_table(sess.uploaded_papers)
            summary_h = render_uploaded_papers_summary(sess.uploaded_papers)
            stats_h = render_stat_cards_html(
                sess.papers_found_count,
                sess.highly_relevant_count,
                sess.gaps_count,
                sess.review_coverage_percent
            )
            pipe_h = render_pipeline_html(100, f"Analysis & comparison complete ({len(sess.unified_papers)} documents) 100%", sess.pipeline_status)
            top_h = render_top_papers_card(sess.unified_papers[:4], active_topic)
            gaps_h = render_gap_intelligence_card(gaps, active_topic)
            insight_h = render_ai_insight_card(sess.ai_summary, active_topic)
            analysis_cards_h = render_analysis_cards(sess.unified_papers)
            gaps_detail_h = render_detailed_gaps(gaps)
            comp_table_h = render_comparison_table(sess.unified_papers)
            fig1, fig2 = generate_comparison_charts(sess.unified_papers)
            review_md = review_data.get("markdown", "")
            hero_h = render_hero_banner_html(active_topic)

            msg = f"Successfully processed, analyzed, and compared {len(files)} document(s)."

            # Salim Chat Sync Notification
            count = len(sess.unified_papers)
            uploaded_titles = "\n".join([f"- *\"{p.title}\"*" for p in sess.uploaded_papers[-len(files):]])
            chat_notice = (
                f"**Documents Uploaded, Analyzed & Compared**\n\n"
                f"Successfully parsed, extracted, and compared **{len(files)} document(s)**:\n"
                f"{uploaded_titles}\n\n"
                f"Active research topic set to: **\"{active_topic}\"**.\n"
                f"Total active research collection: **{count} documents**.\n"
                f"- **AI Analysis:** Structured problem, methodology, dataset, and limitations extracted.\n"
                f"- **Comparative Analytics:** Scatter plots and year distributions updated.\n"
                f"- **Research Gaps:** {len(gaps)} collective void(s) synthesized.\n\n"
                f"Ask me anything about these uploaded documents!"
            )
            chat_hist = list(current_chat or INITIAL_WELCOME_MESSAGE)
            chat_hist.append({"role": "assistant", "content": chat_notice})
            profile_h = render_salim_sidebar_html(count, active_topic)

            # Auto-persist session to disk
            sess.save_to_disk()

            return (
                sess,
                msg,
                table_h,
                preview_text,
                active_topic,
                hero_h,
                active_topic,
                summary_h,
                stats_h,
                pipe_h,
                top_h,
                gaps_h,
                insight_h,
                analysis_cards_h,
                gaps_detail_h,
                comp_table_h,
                fig1,
                fig2,
                review_md,
                review_md,
                chat_hist,
                profile_h
            )

        # Wire both the upload dropzone and the process button on the Upload page
        upload_ui["file_upload"].upload(
            fn=handle_upload_page_files,
            inputs=[session, upload_ui["file_upload"], chat_ui["chatbot"]],
            outputs=[
                session,
                upload_ui["upload_status_msg"],
                upload_ui["uploaded_table_html"],
                upload_ui["text_preview_output"],
                dash_ui["topic_input"],
                dash_ui["hero_banner_html"],
                search_ui["search_topic_input"],
                dash_ui["upload_summary_html"],
                dash_ui["stats_html"],
                dash_ui["pipeline_html"],
                dash_ui["top_papers_html"],
                dash_ui["gaps_html"],
                dash_ui["ai_insight_html"],
                analysis_ui["analysis_container"],
                gaps_ui["gaps_container"],
                comparison_ui["comparison_table_html"],
                comparison_ui["chart_scatter"],
                comparison_ui["chart_hist"],
                review_ui["review_markdown_display"],
                review_ui["review_editor"],
                chat_ui["chatbot"],
                chat_ui["salim_profile_display"]
            ]
        )

        upload_ui["upload_process_btn"].click(
            fn=handle_upload_page_files,
            inputs=[session, upload_ui["file_upload"], chat_ui["chatbot"]],
            outputs=[
                session,
                upload_ui["upload_status_msg"],
                upload_ui["uploaded_table_html"],
                upload_ui["text_preview_output"],
                dash_ui["topic_input"],
                dash_ui["hero_banner_html"],
                search_ui["search_topic_input"],
                dash_ui["upload_summary_html"],
                dash_ui["stats_html"],
                dash_ui["pipeline_html"],
                dash_ui["top_papers_html"],
                dash_ui["gaps_html"],
                dash_ui["ai_insight_html"],
                analysis_ui["analysis_container"],
                gaps_ui["gaps_container"],
                comparison_ui["comparison_table_html"],
                comparison_ui["chart_scatter"],
                comparison_ui["chart_hist"],
                review_ui["review_markdown_display"],
                review_ui["review_editor"],
                chat_ui["chatbot"],
                chat_ui["salim_profile_display"]
            ]
        )


        def clear_uploaded_papers(sess: ResearchSession):
            sess.uploaded_papers = []
            sess.save_to_disk()
            profile_h = render_salim_sidebar_html(len(sess.unified_papers), sess.research_topic)
            fig1, fig2 = generate_comparison_charts(sess.unified_papers)
            return (
                sess,
                "All uploaded papers cleared.",
                render_uploaded_table([]),
                render_uploaded_papers_summary([]),
                render_stat_cards_html(sess.papers_found_count, sess.highly_relevant_count, sess.gaps_count, sess.review_coverage_percent),
                render_analysis_cards(sess.unified_papers),
                render_detailed_gaps(sess.detected_gaps),
                render_comparison_table(sess.unified_papers),
                fig1, fig2,
                profile_h
            )

        upload_ui["clear_uploads_btn"].click(
            fn=clear_uploaded_papers,
            inputs=[session],
            outputs=[
                session,
                upload_ui["upload_status_msg"],
                upload_ui["uploaded_table_html"],
                dash_ui["upload_summary_html"],
                dash_ui["stats_html"],
                analysis_ui["analysis_container"],
                gaps_ui["gaps_container"],
                comparison_ui["comparison_table_html"],
                comparison_ui["chart_scatter"],
                comparison_ui["chart_hist"],
                chat_ui["salim_profile_display"]
            ]
        )

        def handle_reset_all_history():
            ResearchSession.clear_disk_history()
            clean_sess = ResearchSession()
            cur_topic = clean_sess.research_topic
            profile_h = render_salim_sidebar_html(0, cur_topic)
            fig1, fig2 = generate_comparison_charts([])
            return (
                clean_sess,
                "Workspace & session history cleared. Starting completely fresh.",
                render_uploaded_table([]),
                render_uploaded_papers_summary([]),
                render_hero_banner_html(cur_topic),
                cur_topic,
                cur_topic,
                render_stat_cards_html(0, 0, 0, 0),
                render_pipeline_html(0, "Ready to start literature review", clean_sess.pipeline_status),
                render_top_papers_card([], cur_topic),
                render_gap_intelligence_card([], cur_topic),
                render_ai_insight_card("", cur_topic),
                render_search_results_cards([]),
                render_analysis_cards([]),
                render_detailed_gaps([]),
                render_comparison_table([]),
                fig1, fig2,
                "*Click 'Synthesize Complete Literature Review' to build your document.*",
                "",
                profile_h
            )

        upload_ui["reset_all_btn"].click(
            fn=handle_reset_all_history,
            inputs=[],
            outputs=[
                session,
                upload_ui["upload_status_msg"],
                upload_ui["uploaded_table_html"],
                dash_ui["upload_summary_html"],
                dash_ui["hero_banner_html"],
                dash_ui["topic_input"],
                search_ui["search_topic_input"],
                dash_ui["stats_html"],
                dash_ui["pipeline_html"],
                dash_ui["top_papers_html"],
                dash_ui["gaps_html"],
                dash_ui["ai_insight_html"],
                search_ui["search_results_container"],
                analysis_ui["analysis_container"],
                gaps_ui["gaps_container"],
                comparison_ui["comparison_table_html"],
                comparison_ui["chart_scatter"],
                comparison_ui["chart_hist"],
                review_ui["review_markdown_display"],
                review_ui["review_editor"],
                chat_ui["salim_profile_display"]
            ]
        )

        def handle_refresh_from_db():
            sess = ResearchSession.load_from_disk()
            papers = sess.unified_papers
            cur_topic = sess.research_topic or DEFAULT_TOPIC
            fig1, fig2 = generate_comparison_charts(papers)
            review_md = (sess.literature_review.get("markdown", "") if (sess and sess.literature_review) else "*Click 'Synthesize Complete Literature Review' to build your document.*")
            review_raw = sess.literature_review.get("markdown", "") if (sess and sess.literature_review) else ""
            profile_html = render_salim_sidebar_html(len(papers), cur_topic)

            return (
                sess,
                f"Successfully reloaded {len(sess.uploaded_papers)} documents from SQLite database.",
                render_uploaded_table(sess.uploaded_papers),
                render_uploaded_papers_summary(sess.uploaded_papers),
                render_hero_banner_html(cur_topic),
                cur_topic,
                cur_topic,
                render_stat_cards_html(sess.papers_found_count, sess.highly_relevant_count, sess.gaps_count, sess.review_coverage_percent),
                render_pipeline_html(sess.pipeline_progress, sess.pipeline_status_text, sess.pipeline_status),
                render_top_papers_card(papers[:4], cur_topic),
                render_gap_intelligence_card(sess.detected_gaps, cur_topic),
                render_ai_insight_card(sess.ai_summary, cur_topic),
                render_search_results_cards(sess.searched_papers),
                render_analysis_cards(papers),
                render_detailed_gaps(sess.detected_gaps),
                render_comparison_table(papers),
                fig1, fig2,
                review_md,
                review_raw,
                profile_html
            )

        upload_ui["refresh_db_btn"].click(
            fn=handle_refresh_from_db,
            inputs=[],
            outputs=[
                session,
                upload_ui["upload_status_msg"],
                upload_ui["uploaded_table_html"],
                dash_ui["upload_summary_html"],
                dash_ui["hero_banner_html"],
                dash_ui["topic_input"],
                search_ui["search_topic_input"],
                dash_ui["stats_html"],
                dash_ui["pipeline_html"],
                dash_ui["top_papers_html"],
                dash_ui["gaps_html"],
                dash_ui["ai_insight_html"],
                search_ui["search_results_container"],
                analysis_ui["analysis_container"],
                gaps_ui["gaps_container"],
                comparison_ui["comparison_table_html"],
                comparison_ui["chart_scatter"],
                comparison_ui["chart_hist"],
                review_ui["review_markdown_display"],
                review_ui["review_editor"],
                chat_ui["salim_profile_display"]
            ]
        )




        # -------------------------------------------------------------
        # DEDICATED SEARCH PAGE HANDLERS
        # -------------------------------------------------------------
        def handle_search_page_query(
            sess: ResearchSession,
            topic: str,
            year_from: int,
            year_to: int,
            sources: List[str],
            max_p: int,
            current_chat: List[Any]
        ):
            sess.research_topic = topic
            papers, api_status, errors = SearchAggregator.execute_search(
                topic=topic,
                start_year=int(year_from),
                end_year=int(year_to),
                sources=sources,
                max_papers=int(max_p)
            )
            sess.searched_papers = papers
            sess.api_status.update(api_status)

            cards_h = render_search_results_cards(sess.unified_papers)
            msg = f"Retrieved {len(papers)} papers across {len(sources)} academic sources."
            if errors:
                msg += f" (Notices: {', '.join(errors)})"

            stats_h = render_stat_cards_html(
                sess.papers_found_count,
                sess.highly_relevant_count,
                sess.gaps_count,
                sess.review_coverage_percent
            )
            top_h = render_top_papers_card(sess.unified_papers[:4], topic)

            # Salim Chat Sync Notification
            count = len(sess.unified_papers)
            top_sample = f"- *\"{papers[0].title}\"*" if papers else ""
            chat_notice = (
                f"**Search Synchronized**\n\n"
                f"Retrieved and indexed **{len(papers)} paper(s)** on **\"{topic}\"** across {len(sources)} academic sources.\n"
                f"{top_sample}\n\n"
                f"Total active papers: **{count}**. You can now ask me to analyze or compare these papers!"
            )
            chat_hist = list(current_chat or INITIAL_WELCOME_MESSAGE)
            chat_hist.append({"role": "assistant", "content": chat_notice})
            profile_h = render_salim_sidebar_html(count, topic)
            sess.save_to_disk()

            return sess, msg, cards_h, stats_h, top_h, chat_hist, profile_h

        search_ui["search_btn"].click(
            fn=handle_search_page_query,
            inputs=[
                session,
                search_ui["search_topic_input"],
                search_ui["search_year_from"],
                search_ui["search_year_to"],
                search_ui["search_sources"],
                search_ui["search_max_papers"],
                chat_ui["chatbot"]
            ],
            outputs=[
                session,
                search_ui["search_status_box"],
                search_ui["search_results_container"],
                dash_ui["stats_html"],
                dash_ui["top_papers_html"],
                chat_ui["chatbot"],
                chat_ui["salim_profile_display"]
            ]
        )


        # -------------------------------------------------------------
        # AI ANALYSIS PAGE HANDLERS
        # -------------------------------------------------------------
        def handle_run_analysis(sess: ResearchSession):
            papers_to_analyze = sess.unified_papers[:8]
            if not papers_to_analyze:
                return sess, "No papers available to analyze. Please search or upload first.", render_analysis_cards([])

            for p in papers_to_analyze:
                AnalysisService.analyze_paper(p)

            cards_h = render_analysis_cards(papers_to_analyze)
            stats_h = render_stat_cards_html(
                sess.papers_found_count,
                sess.highly_relevant_count,
                sess.gaps_count,
                sess.review_coverage_percent
            )
            msg = f"Completed grounded multi-dimension analysis for {len(papers_to_analyze)} papers."
            sess.save_to_disk()
            return sess, msg, cards_h, stats_h

        analysis_ui["run_analysis_btn"].click(
            fn=handle_run_analysis,
            inputs=[session],
            outputs=[
                session,
                analysis_ui["analysis_progress_text"],
                analysis_ui["analysis_container"],
                dash_ui["stats_html"]
            ]
        )

        # -------------------------------------------------------------
        # COMPARISON & CSV EXPORT HANDLERS
        # -------------------------------------------------------------
        def handle_refresh_comparison(sess: ResearchSession):
            papers = sess.unified_papers[:10]
            table_h = render_comparison_table(papers)
            fig1, fig2 = generate_comparison_charts(papers)
            return table_h, fig1, fig2

        comparison_ui["compare_btn"].click(
            fn=handle_refresh_comparison,
            inputs=[session],
            outputs=[
                comparison_ui["comparison_table_html"],
                comparison_ui["chart_scatter"],
                comparison_ui["chart_hist"]
            ]
        )

        def handle_export_comparison_csv(sess: ResearchSession):
            papers = sess.unified_papers
            if not papers:
                return gr.update(visible=False)
            csv_path = CsvExporter.export_comparison(papers, filename_prefix=f"LiteratureAI_Comparison_{datetime.now().strftime('%Y%m%d_%H%M')}")
            return gr.update(value=csv_path, visible=True)

        comparison_ui["export_csv_btn"].click(
            fn=handle_export_comparison_csv,
            inputs=[session],
            outputs=[comparison_ui["csv_download_file"]]
        )

        # -------------------------------------------------------------
        # RESEARCH GAP DETECTION HANDLERS
        # -------------------------------------------------------------
        def handle_gap_detection(sess: ResearchSession):
            papers = sess.unified_papers[:10]
            if not papers:
                return sess, "No papers available. Search or upload papers first.", render_detailed_gaps([])

            gaps = GapDetector.detect_gaps(papers, sess.research_topic)
            sess.detected_gaps = gaps
            gaps_h = render_detailed_gaps(gaps)
            dash_gaps_h = render_gap_intelligence_card(gaps)
            stats_h = render_stat_cards_html(
                sess.papers_found_count,
                sess.highly_relevant_count,
                sess.gaps_count,
                sess.review_coverage_percent
            )
            msg = f"Identified {len(gaps)} critical research gaps supported by analyzed evidence."
            sess.save_to_disk()
            return sess, msg, gaps_h, dash_gaps_h, stats_h

        gaps_ui["detect_gaps_btn"].click(
            fn=handle_gap_detection,
            inputs=[session],
            outputs=[
                session,
                gaps_ui["gaps_status_msg"],
                gaps_ui["gaps_container"],
                dash_ui["gaps_html"],
                dash_ui["stats_html"]
            ]
        )

        # -------------------------------------------------------------
        # LITERATURE REVIEW SYNTHESIS & EXPORT HANDLERS
        # -------------------------------------------------------------
        def handle_review_synthesis(sess: ResearchSession):
            papers = sess.unified_papers[:10]
            if not papers:
                return sess, "No papers in session.", "*No papers found to synthesize review.*", ""

            review_data = ReviewGenerator.generate_review(sess.research_topic, papers, sess.detected_gaps)
            sess.literature_review = review_data
            md_text = review_data.get("markdown", "")
            msg = f"Synthesized 7-section literature review with {len(review_data.get('references', []))} verified citations."
            sess.save_to_disk()
            return sess, msg, md_text, md_text


        review_ui["generate_review_btn"].click(
            fn=handle_review_synthesis,
            inputs=[session],
            outputs=[
                session,
                review_ui["review_status_msg"],
                review_ui["review_markdown_display"],
                review_ui["review_editor"]
            ]
        )

        dash_ui["footer_generate_btn"].click(
            fn=lambda: "📖 Literature Review",
            inputs=[],
            outputs=[sidebar_ui["nav_selector"]]
        ).then(
            fn=route_view,
            inputs=[sidebar_ui["nav_selector"], session],
            outputs=[
                view_dashboard, view_search, view_upload, view_analysis,
                view_comparison, view_gaps, view_review, view_chat,
                analysis_ui["analysis_container"],
                gaps_ui["gaps_container"],
                comparison_ui["comparison_table_html"],
                comparison_ui["chart_scatter"],
                comparison_ui["chart_hist"],
                review_ui["review_markdown_display"],
                review_ui["review_editor"],
                dash_ui["stats_html"],
                dash_ui["top_papers_html"],
                dash_ui["gaps_html"],
                dash_ui["ai_insight_html"],
                upload_ui["uploaded_table_html"],
                dash_ui["upload_summary_html"],
                chat_ui["salim_profile_display"]
            ]
        )



        def handle_export_docx(sess: ResearchSession):
            if not sess.literature_review:
                # Generate review first if not done
                papers = sess.unified_papers[:10]
                sess.literature_review = ReviewGenerator.generate_review(sess.research_topic, papers, sess.detected_gaps)

            path = DocxExporter.export(
                sess.literature_review,
                filename_prefix=f"LiteratureReview_{datetime.now().strftime('%Y%m%d_%H%M')}"
            )
            return gr.update(value=path, visible=True)

        review_ui["export_docx_btn"].click(
            fn=handle_export_docx,
            inputs=[session],
            outputs=[review_ui["docx_download_file"]]
        )

        def handle_export_txt(sess: ResearchSession):
            md_text = sess.literature_review.get("markdown", "") if sess.literature_review else "No review generated."
            txt_path = str(EXPORTS_DIR / f"LiteratureReview_{datetime.now().strftime('%Y%m%d_%H%M')}.txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(md_text)
            return gr.update(value=txt_path, visible=True)

        # -------------------------------------------------------------
        # CHAT WITH LITERATURE (RAG) HANDLERS
        # -------------------------------------------------------------
        def handle_chat_message(sess: ResearchSession, message: str, history: List[Any]):
            if not message or not message.strip():
                return history or INITIAL_WELCOME_MESSAGE, ""
            
            # Normalize history into list of dicts for Gradio 6
            cleaned_history = []
            if history:
                for item in history:
                    if isinstance(item, dict) and "role" in item and "content" in item:
                        cleaned_history.append(item)
                    elif isinstance(item, (list, tuple)) and len(item) == 2:
                        cleaned_history.append({"role": "user", "content": str(item[0])})
                        cleaned_history.append({"role": "assistant", "content": str(item[1])})

            answer = ChatRAGService.answer_question(message, sess.unified_papers, cleaned_history)
            cleaned_history.append({"role": "user", "content": message})
            cleaned_history.append({"role": "assistant", "content": answer})
            return cleaned_history, ""

        chat_ui["send_btn"].click(
            fn=handle_chat_message,
            inputs=[session, chat_ui["msg_input"], chat_ui["chatbot"]],
            outputs=[chat_ui["chatbot"], chat_ui["msg_input"]]
        )
        chat_ui["msg_input"].submit(
            fn=handle_chat_message,
            inputs=[session, chat_ui["msg_input"], chat_ui["chatbot"]],
            outputs=[chat_ui["chatbot"], chat_ui["msg_input"]]
        )
        chat_ui["clear_btn"].click(
            fn=lambda: INITIAL_WELCOME_MESSAGE,
            inputs=[],
            outputs=[chat_ui["chatbot"]]
        )

        # Quick research trigger buttons
        chat_ui["quick_btn_summary"].click(
            fn=lambda sess, hist: handle_chat_message(sess, "Summarize all loaded research papers and their core contributions.", hist),
            inputs=[session, chat_ui["chatbot"]],
            outputs=[chat_ui["chatbot"], chat_ui["msg_input"]]
        )
        chat_ui["quick_btn_methods"].click(
            fn=lambda sess, hist: handle_chat_message(sess, "Extract and compare the methodologies and simulation datasets used across the papers.", hist),
            inputs=[session, chat_ui["chatbot"]],
            outputs=[chat_ui["chatbot"], chat_ui["msg_input"]]
        )
        chat_ui["quick_btn_gaps"].click(
            fn=lambda sess, hist: handle_chat_message(sess, "Identify empirical research limitations and open future challenges.", hist),
            inputs=[session, chat_ui["chatbot"]],
            outputs=[chat_ui["chatbot"], chat_ui["msg_input"]]
        )
        chat_ui["quick_btn_marl"].click(
            fn=lambda sess, hist: handle_chat_message(sess, "Explain how Multi-Agent Reinforcement Learning (MARL) is applied to autonomous space communication networks.", hist),
            inputs=[session, chat_ui["chatbot"]],
            outputs=[chat_ui["chatbot"], chat_ui["msg_input"]]
        )

        # Voice Dictation & Whisper STT Handlers
        def handle_voice_recording(sess: ResearchSession, audio_path: str, history: List[Any]):
            if not audio_path:
                return history or INITIAL_WELCOME_MESSAGE, None, ""
            
            # Transcribe audio using Whisper
            transcribed_query = TranscriptionService.transcribe(audio_path)
            if not transcribed_query or not transcribed_query.strip():
                return history or INITIAL_WELCOME_MESSAGE, None, ""

            # Process through RAG chat
            updated_history, _ = handle_chat_message(sess, transcribed_query, history)
            return updated_history, None, transcribed_query

        chat_ui["voice_recorder"].stop_recording(
            fn=handle_voice_recording,
            inputs=[session, chat_ui["voice_recorder"], chat_ui["chatbot"]],
            outputs=[chat_ui["chatbot"], chat_ui["voice_recorder"], chat_ui["msg_input"]]
        )

        whisper_visible = gr.State(False)
        def toggle_whisper_ui(is_open):
            new_state = not is_open
            return new_state, gr.update(visible=new_state)

        chat_ui["whisper_toggle_btn"].click(
            fn=toggle_whisper_ui,
            inputs=[whisper_visible],
            outputs=[whisper_visible, chat_ui["voice_recorder_row"]]
        )


        # -------------------------------------------------------------
        # SESSION RESTORATION ON CLIENT LOAD / REFRESH
        # -------------------------------------------------------------

        def restore_session_on_load():
            try:
                sess = ResearchSession.load_from_disk()
                cur_topic = sess.research_topic or DEFAULT_TOPIC
                papers = sess.unified_papers
                count = len(papers)
                fig1, fig2 = generate_comparison_charts(papers)
                review_md = (sess.literature_review.get("markdown", "") if (sess and sess.literature_review) else "*Click 'Synthesize Complete Literature Review' to build your document.*")
                review_raw = sess.literature_review.get("markdown", "") if (sess and sess.literature_review) else ""
                profile_html = render_salim_sidebar_html(count, cur_topic)

                return (
                    sess,
                    cur_topic,
                    render_hero_banner_html(cur_topic),
                    cur_topic,
                    render_stat_cards_html(
                        sess.papers_found_count,
                        sess.highly_relevant_count,
                        sess.gaps_count,
                        sess.review_coverage_percent
                    ),
                    render_pipeline_html(
                        sess.pipeline_progress,
                        sess.pipeline_status_text,
                        sess.pipeline_status
                    ),
                    render_uploaded_papers_summary(sess.uploaded_papers),
                    render_top_papers_card(papers[:4], cur_topic),
                    render_gap_intelligence_card(sess.detected_gaps, cur_topic),
                    render_ai_insight_card(sess.ai_summary, cur_topic),
                    render_search_results_cards(sess.searched_papers),
                    render_uploaded_table(sess.uploaded_papers),
                    render_analysis_cards(papers),
                    render_detailed_gaps(sess.detected_gaps),
                    render_comparison_table(papers),
                    fig1, fig2,
                    review_md,
                    review_raw,
                    profile_html
                )
            except Exception as e:
                logger.error(f"Error in restore_session_on_load: {e}", exc_info=True)
                clean_sess = ResearchSession()
                cur_topic = clean_sess.research_topic
                fig1, fig2 = generate_comparison_charts([])
                return (
                    clean_sess,
                    cur_topic,
                    render_hero_banner_html(cur_topic),
                    cur_topic,
                    render_stat_cards_html(0, 0, 0, 0),
                    render_pipeline_html(0, "Ready to start", clean_sess.pipeline_status),
                    render_uploaded_papers_summary([]),
                    render_top_papers_card([], cur_topic),
                    render_gap_intelligence_card([], cur_topic),
                    render_ai_insight_card("", cur_topic),
                    render_search_results_cards([]),
                    render_uploaded_table([]),
                    render_analysis_cards([]),
                    render_detailed_gaps([]),
                    render_comparison_table([]),
                    fig1, fig2,
                    "*Click 'Synthesize Complete Literature Review' to build your document.*",
                    "",
                    render_salim_sidebar_html(0, cur_topic)
                )


        app.load(
            fn=restore_session_on_load,
            inputs=[],
            outputs=[
                session,
                dash_ui["topic_input"],
                dash_ui["hero_banner_html"],
                search_ui["search_topic_input"],
                dash_ui["stats_html"],
                dash_ui["pipeline_html"],
                dash_ui["upload_summary_html"],
                dash_ui["top_papers_html"],
                dash_ui["gaps_html"],
                dash_ui["ai_insight_html"],
                search_ui["search_results_container"],
                upload_ui["uploaded_table_html"],
                analysis_ui["analysis_container"],
                gaps_ui["gaps_container"],
                comparison_ui["comparison_table_html"],
                comparison_ui["chart_scatter"],
                comparison_ui["chart_hist"],
                review_ui["review_markdown_display"],
                review_ui["review_editor"],
                chat_ui["salim_profile_display"]
            ]
        )

    return app


if __name__ == "__main__":
    theme = get_literature_theme()
    app = build_app()
    base_port = int(os.environ.get("PORT", 7860))
    server_host = os.environ.get("SERVER_NAME", "0.0.0.0")
    share_flag = os.environ.get("GRADIO_SHARE", "False").lower() in ("true", "1")
    
    for p in range(base_port, base_port + 20):
        try:
            _, local_url, share_url = app.launch(
                server_name=server_host,
                server_port=p,
                share=share_flag,
                theme=theme,
                css=CUSTOM_CSS,
                head=VOICE_SCRIPT_HEAD
            )
            if share_url:
                print(f"\n========================================\nPUBLIC LIVE URL: {share_url}\n========================================\n", flush=True)
                os.makedirs("exports", exist_ok=True)
                with open("exports/live_url.txt", "w") as f:
                    f.write(share_url)
            break
        except OSError as e:
            if "empty port" in str(e).lower() or "address already in use" in str(e).lower():
                continue
            raise e
