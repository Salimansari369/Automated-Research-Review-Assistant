import gradio as gr
from typing import Dict, Any

def create_review_view():
    with gr.Column(elem_classes=["review-view"]):
        gr.Markdown("## 📖 Academic Literature Review Synthesizer\n*Full 7-section academic synthesis with grounded [1], [2] citations and verified references.*")

        with gr.Row():
            generate_review_btn = gr.Button("📖 Synthesize Complete Literature Review", variant="primary", elem_classes=["btn-primary-gradient"])
            export_docx_btn = gr.Button("📄 Export DOCX Document")
            export_txt_btn = gr.Button("📝 Export TXT File")

        with gr.Row():
            docx_download_file = gr.File(label="Download DOCX", visible=False)
            txt_download_file = gr.File(label="Download TXT", visible=False)

        review_status_msg = gr.Markdown("Ready to synthesize literature review.")

        with gr.Tabs():
            with gr.TabItem("📄 Formatted Academic Document"):
                review_markdown_display = gr.Markdown(value="*Click 'Synthesize Complete Literature Review' to build your document.*")
            
            with gr.TabItem("✏️ Markdown Editor"):
                review_editor = gr.Textbox(
                    label="Full Review Markdown",
                    lines=20,
                    placeholder="Synthesized review content will appear here for editing...",
                    interactive=True
                )

    return {
        "generate_review_btn": generate_review_btn,
        "export_docx_btn": export_docx_btn,
        "export_txt_btn": export_txt_btn,
        "docx_download_file": docx_download_file,
        "txt_download_file": txt_download_file,
        "review_status_msg": review_status_msg,
        "review_markdown_display": review_markdown_display,
        "review_editor": review_editor
    }
