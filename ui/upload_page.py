import gradio as gr
from typing import List
from models.paper import Paper
from models.session import ResearchSession

def render_uploaded_table(papers: List[Paper]) -> str:
    if not papers:
        return """
        <div style="text-align: center; padding: 40px; background: #080b1a; border-radius: 16px; border: 1px dashed #1e2548; margin-top: 16px;">
          <div style="font-size: 32px; margin-bottom: 8px;">📂</div>
          <div style="font-size: 15px; font-weight: 700; color: #f8fafc;">No documents uploaded yet</div>
          <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">Drag & drop PDF, Word (.docx, .doc), or Text (.txt, .md) research papers to extract metadata and full text.</div>
        </div>
        """

    rows = []
    for idx, p in enumerate(papers, 1):
        status_tag = "<span style='color: #34d399; font-weight: 700;'>✓ Ready</span>"
        if "Scanned" in (p.abstract or ""):
            status_tag = "<span style='color: #fbbf24; font-weight: 700;'>⚠️ Scanned Layer</span>"

        ext_icon = "📄" if (p.file_path or "").endswith(".pdf") else ("📝" if ".doc" in (p.file_path or "") else "📃")

        rows.append(f"""
        <tr style="border-bottom: 1px solid #1e2548; background: {('#0d1126' if idx % 2 == 0 else '#080b1a')};">
          <td style="padding: 12px 14px; font-weight: 700; color: #a78bfa;">#{idx}</td>
          <td style="padding: 12px 14px;">
            <div style="font-weight: 700; color: #f8fafc; font-size: 13px;">{ext_icon} {p.title}</div>
            <div style="font-size: 11px; color: #94a3b8; margin-top: 2px;">👤 {p.formatted_authors} • {p.source}</div>
          </td>
          <td style="padding: 12px 14px; font-size: 12px; color: #cbd5e1;">{p.year or 'Auto-detected'}</td>
          <td style="padding: 12px 14px; font-size: 12px; color: #cbd5e1;">{p.file_size_mb or 0.0:.1f} MB</td>
          <td style="padding: 12px 14px; font-size: 11px; color: #8b5cf6;">{p.doi or 'None'}</td>
          <td style="padding: 12px 14px; font-size: 12px;">{status_tag}</td>
        </tr>
        """)

    table_body = "".join(rows)
    return f"""
    <div style="background: #0d1126; border-radius: 16px; border: 1px solid #1e2548; overflow: hidden; box-shadow: var(--card-shadow); margin-top: 16px;">
      <table style="width: 100%; border-collapse: collapse; text-align: left;">
        <thead style="background: #080b1a; border-bottom: 2px solid #1e2548; font-size: 11px; font-weight: 800; color: #a78bfa; text-transform: uppercase; letter-spacing: 0.5px;">
          <tr>
            <th style="padding: 12px 14px;">#</th>
            <th style="padding: 12px 14px;">Document Title & Authors</th>
            <th style="padding: 12px 14px;">Year</th>
            <th style="padding: 12px 14px;">File Size</th>
            <th style="padding: 12px 14px;">DOI</th>
            <th style="padding: 12px 14px;">Status</th>
          </tr>
        </thead>
        <tbody>
          {table_body}
        </tbody>
      </table>
    </div>
    """

def create_upload_view():
    with gr.Column(elem_classes=["upload-view", "upload-page-container"]):
        gr.Markdown("## 📂 Upload Personal Research Papers & Documents\n*Integrate your own PDF, Word DOCX/DOC, and Text research files directly into the unified research session.*")

        with gr.Row():
            file_upload = gr.File(
                label="Select or Drag & Drop Documents (.pdf, .docx, .doc, .txt, .md — multi-file enabled, max 50MB each)",
                file_count="multiple",
                file_types=[".pdf", ".docx", ".doc", ".txt", ".md"],
                elem_classes=["dropzone-box"]
            )

        with gr.Row():
            upload_process_btn = gr.Button("📑 Process & Extract Documents (PDF / DOCX / TXT)", variant="primary", elem_classes=["btn-primary-gradient"])
            clear_uploads_btn = gr.Button("🗑️ Clear Uploaded Documents", elem_classes=["btn-whisper-toggle"])

        upload_status_msg = gr.Markdown("Ready to upload and process documents.")
        uploaded_table_html = gr.HTML(value=render_uploaded_table([]))

        with gr.Accordion("🔍 Extracted Text & Metadata Preview", open=False):
            text_preview_output = gr.Textbox(
                label="Extracted Text Snippet (First 2,000 characters)",
                lines=10,
                interactive=False
            )

    return {
        "file_upload": file_upload,
        "upload_process_btn": upload_process_btn,
        "clear_uploads_btn": clear_uploads_btn,
        "upload_status_msg": upload_status_msg,
        "uploaded_table_html": uploaded_table_html,
        "text_preview_output": text_preview_output
    }

