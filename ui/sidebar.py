import gradio as gr
from ui.components import render_sidebar_header_html, render_sidebar_footer_html

def create_sidebar_view():
    with gr.Column(scale=0, min_width=235, elem_classes=["sidebar-container"]):
        sidebar_header_display = gr.HTML(value=render_sidebar_header_html())
        
        nav_selector = gr.Radio(
            choices=[
                "🏠 Dashboard",
                "🔎 Search Papers",
                "📂 Upload Papers",
                "🧠 AI Analysis",
                "⚖️ Comparison",
                "🔍 Research Gaps",
                "📖 Literature Review",
                "💬 Chat with Literature"
            ],
            value="🏠 Dashboard",
            show_label=False,
            container=False,
            elem_classes=["nav-tabs-container"]
        )

        sidebar_footer_display = gr.HTML(value=render_sidebar_footer_html())

    return {
        "sidebar_header_display": sidebar_header_display,
        "sidebar_footer_display": sidebar_footer_display,
        "sidebar_status_display": sidebar_footer_display,
        "nav_selector": nav_selector
    }


