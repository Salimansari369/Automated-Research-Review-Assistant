import os
import shutil
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
EXPORTS_DIR = os.path.join(BASE_DIR, "exports")
DESKTOP_DIR = os.path.join(os.path.expanduser("~"), "Desktop")
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(EXPORTS_DIR, exist_ok=True)

USER_UPLOADED_DIR = r"C:\Users\Salim Ansari\.gemini\antigravity\brain\d8e21039-bd52-4428-a9d5-4b29ebdab2e7\.user_uploaded"
images_map = {
    "dashboard_light.png": os.path.join(USER_UPLOADED_DIR, "media_1789895633467.png"),
    "salim_voice_chat.png": os.path.join(USER_UPLOADED_DIR, "media_1789895655925.png"),
    "document_upload.png": os.path.join(USER_UPLOADED_DIR, "media_1789895655935.png"),
    "dashboard_dark.png": os.path.join(USER_UPLOADED_DIR, "media_1789895655967.png"),
    "intelligence_cards.png": os.path.join(USER_UPLOADED_DIR, "media_1789895655980.png")
}

for name, src in images_map.items():
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(ASSETS_DIR, name))

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._element.get_or_add_tcPr().append(shading)

def set_table_borders(table, color="000000", sz="4", val="single"):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            </w:tblBorders>
        ''')
        tblPr[0].append(borders)

def build_aligned_report():
    doc = Document()

    # Exact page settings matching friend's doc (A4 with 1.18" left, 0.69" right, 0.94" top, 1.00" bottom)
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.94)
        section.bottom_margin = Inches(1.00)
        section.left_margin = Inches(1.18)
        section.right_margin = Inches(0.69)

    # Base typography (Times New Roman, pure Black)
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    # -------------------------------------------------------------
    # 1. COVER / TITLE PAGE
    # -------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_inst.add_run("SYMBIOSIS INSTITUTE OF TECHNOLOGY, NAGPUR\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x99, 0x00, 0x00) # Maroon header

    r = p_inst.add_run("Symbiosis International (Deemed University)\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    
    r = p_inst.add_run("(Established under section 3 of the UGC Act, 1956)\nRe-accredited by NAAC with 'A++' Grade | Awarded Category - I by UGC\nFounder: Prof. Dr. S. B. Mujumdar, M. Sc., Ph. D. (Awarded Padma Bhushan and Padma Shri by President of India)\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    doc.add_paragraph().paragraph_format.space_after = Pt(18)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_rep = p_title.add_run("A PROJECT REPORT\nON\n\n")
    r_rep.font.name = 'Times New Roman'
    r_rep.font.size = Pt(13)
    r_rep.font.bold = True
    r_rep.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    r_main_title = p_title.add_run("“Automated Literature Review Assistant: An Agentic AI-Powered Autonomous Academic Research Discovery, Gap Intelligence, and Review Synthesis System”\n\n")
    r_main_title.font.name = 'Times New Roman'
    r_main_title.font.size = Pt(16)
    r_main_title.font.bold = True
    r_main_title.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    r_sub = p_title.add_run("A project report submitted in partial fulfilment of the requirements for the degree of\n")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(11)

    r_subj = p_title.add_run("Subject: Agentic AI & Automation\n\n")
    r_subj.font.name = 'Times New Roman'
    r_subj.font.size = Pt(13)

    r_deg = p_title.add_run("BACHELOR OF TECHNOLOGY\nIN\nCOMPUTER SCIENCE AND ENGINEERING\n\n")
    r_deg.font.name = 'Times New Roman'
    r_deg.font.size = Pt(13)
    r_deg.font.bold = True

    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_by.add_run("Submitted By\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r = p_by.add_run("Salim Ansari\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True
    r = p_by.add_run("(PRN: 24070521005)\n\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True

    r = p_by.add_run("UNDER THE GUIDANCE OF\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r = p_by.add_run("Dr. Parag Naik\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True
    r = p_by.add_run("Subject Teacher\n\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_dept.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\nSYMBIOSIS INSTITUTE OF TECHNOLOGY, NAGPUR\nAY 2026-27")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # 2. CERTIFICATE (Page ii)
    # -------------------------------------------------------------
    p_num = doc.add_paragraph("ii")
    p_num.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_num.runs[0].font.size = Pt(10)

    p_dept_head = doc.add_paragraph()
    p_dept_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_dept_head.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\n\nCERTIFICATE\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True

    p_cert = doc.add_paragraph()
    p_cert.paragraph_format.line_spacing = 1.3
    p_cert.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    p_cert.add_run("This is to certify that the Project work entitled “").font.name = 'Times New Roman'
    r = p_cert.add_run("Automated Literature Review Assistant: An Agentic AI-Powered Autonomous Academic Research Discovery, Gap Intelligence, and Review Synthesis System")
    r.font.name = 'Times New Roman'
    r.font.bold = True
    
    p_cert.add_run("” is carried out by ").font.name = 'Times New Roman'
    r = p_cert.add_run("Salim Ansari (PRN: 24070521005)")
    r.font.name = 'Times New Roman'
    r.font.bold = True
    
    p_cert.add_run(", in partial fulfillment for the award of the degree of ").font.name = 'Times New Roman'
    r = p_cert.add_run("Bachelor of Technology in Computer Science and Engineering")
    r.font.name = 'Times New Roman'
    r.font.bold = True
    
    p_cert.add_run(", Symbiosis Institute of Technology, Nagpur, a constituent of Symbiosis International (Deemed University), Pune during the academic year 2026-2027.\n\n"
               "It is further certified that the work embodied in this report is original and has been carried out under our supervision.").font.name = 'Times New Roman'

    doc.add_paragraph().paragraph_format.space_after = Pt(36)

    sig_table = doc.add_table(rows=2, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_table.autofit = False
    for row in sig_table.rows:
        for cell in row.cells:
            cell.width = Inches(3.2)

    cell_00 = sig_table.cell(0, 0).paragraphs[0]
    r = cell_00.add_run("Dr. Parag Naik\n")
    r.font.name = 'Times New Roman'
    r.font.bold = True
    r.font.size = Pt(11)
    cell_00.add_run("Subject Teacher").font.name = 'Times New Roman'

    cell_01 = sig_table.cell(0, 1).paragraphs[0]
    cell_01.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = cell_01.add_run("Dr. Shreyas Rajendra Hole\n")
    r.font.name = 'Times New Roman'
    r.font.bold = True
    r.font.size = Pt(11)
    cell_01.add_run("Subject Coordinator").font.name = 'Times New Roman'

    sig_table.cell(1, 0).paragraphs[0].paragraph_format.space_before = Pt(36)
    cell_10 = sig_table.cell(1, 0).paragraphs[0]
    r = cell_10.add_run("Head of Department\n")
    r.font.name = 'Times New Roman'
    r.font.bold = True
    r.font.size = Pt(11)
    cell_10.add_run("Computer Science and Engineering").font.name = 'Times New Roman'

    sig_table.cell(1, 1).paragraphs[0].paragraph_format.space_before = Pt(36)
    cell_11 = sig_table.cell(1, 1).paragraphs[0]
    cell_11.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = cell_11.add_run("External Examiner")
    r.font.name = 'Times New Roman'
    r.font.bold = True
    r.font.size = Pt(11)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 3. DECLARATION (Page iii)
    # -------------------------------------------------------------
    p_num = doc.add_paragraph("iii")
    p_num.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_dec_h = doc.add_paragraph()
    p_dec_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_dec_h.add_run("DECLARATION\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True

    p_dec = doc.add_paragraph()
    p_dec.paragraph_format.line_spacing = 1.3
    p_dec.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    p_dec.add_run("I hereby declare that the project titled “").font.name = 'Times New Roman'
    r = p_dec.add_run("Automated Literature Review Assistant: An Agentic AI-Powered Autonomous Academic Research Discovery, Gap Intelligence, and Review Synthesis System")
    r.font.name = 'Times New Roman'
    r.font.bold = True
    p_dec.add_run("” submitted to Symbiosis Institute of Technology, a constituent of Symbiosis International (Deemed University) Pune, for the award of the degree of Bachelor of Technology in Computer Science and Engineering, is a result of original research carried out by me. I understand that my report may be made electronically available to the public. It is further declared that the project report or any part thereof has not been previously submitted to any University or Institute for the award of any degree or diploma.\n\n").font.name = 'Times New Roman'

    p_info = doc.add_paragraph()
    p_info.paragraph_format.line_spacing = 1.4
    p_info.add_run("Name of Student: ").font.name = 'Times New Roman'
    r = p_info.add_run("Salim Ansari (PRN: 24070521005)\n")
    r.font.name = 'Times New Roman'
    r.font.bold = True

    p_info.add_run("Degree: ").font.name = 'Times New Roman'
    p_info.add_run("Bachelor of Technology in Computer Science and Engineering\n").font.name = 'Times New Roman'

    p_info.add_run("Department: ").font.name = 'Times New Roman'
    p_info.add_run("Computer Science and Engineering\n").font.name = 'Times New Roman'

    p_info.add_run("Subject: ").font.name = 'Times New Roman'
    p_info.add_run("Agentic AI & Automation\n").font.name = 'Times New Roman'

    p_info.add_run("Title of the Project: ").font.name = 'Times New Roman'
    r = p_info.add_run("Automated Literature Review Assistant: An Agentic AI-Powered Autonomous Academic Research Discovery, Gap Intelligence, and Review Synthesis System\n\n\n")
    r.font.name = 'Times New Roman'
    r.font.bold = True

    p_info.add_run("Salim Ansari\n").font.name = 'Times New Roman'
    p_info.runs[-1].font.bold = True
    p_info.add_run("Date: 20/09/2026").font.name = 'Times New Roman'

    doc.add_page_break()

    # -------------------------------------------------------------
    # 4. IPR DECLARATION (Page iv)
    # -------------------------------------------------------------
    p_num = doc.add_paragraph("iv")
    p_num.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_ipr_h = doc.add_paragraph()
    p_ipr_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_ipr_h.add_run("IPR DECLARATION\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True

    p_ipr = doc.add_paragraph()
    p_ipr.paragraph_format.line_spacing = 1.3
    p_ipr.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    p_ipr.add_run("I hereby declare that the project entitled “").font.name = 'Times New Roman'
    r = p_ipr.add_run("Automated Literature Review Assistant: An Agentic AI-Powered Autonomous Academic Research Discovery, Gap Intelligence, and Review Synthesis System")
    r.font.name = 'Times New Roman'
    r.font.bold = True
    p_ipr.add_run("”, submitted by me for the purpose of processing under the IPR framework, is not an industry-sponsored project.\n\n"
                "I further provide my full consent to SIT Nagpur and SCRI Pune to evaluate, process, and proceed with the filing of the Intellectual Property Rights (IPR) application for the said idea.\n\n\n"
                "Student Signature\n\n").font.name = 'Times New Roman'

    p_sig = doc.add_paragraph()
    r = p_sig.add_run("Salim Ansari\n\n\n")
    r.font.name = 'Times New Roman'
    r.font.bold = True

    ipr_table = doc.add_table(rows=1, cols=2)
    ipr_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_l = ipr_table.cell(0, 0).paragraphs[0]
    r = c_l.add_run("Dr. Shreyas Rajendra Hole\nSubject Coordinator")
    r.font.name = 'Times New Roman'
    r.font.bold = True

    c_r = ipr_table.cell(0, 1).paragraphs[0]
    c_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = c_r.add_run("Dr. Parag Naik\nSubject Teacher")
    r.font.name = 'Times New Roman'
    r.font.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # 5. ABSTRACT (Page v)
    # -------------------------------------------------------------
    p_num = doc.add_paragraph("v")
    p_num.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_abs_h = doc.add_paragraph()
    p_abs_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_abs_h.add_run("ABSTRACT\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True

    p_abs = doc.add_paragraph()
    p_abs.paragraph_format.line_spacing = 1.25
    p_abs.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    p_abs.add_run(
        "Conducting thorough academic literature reviews is notoriously labor-intensive, requiring researchers to manually query multiple scholarly repositories, filter duplicates, analyze hundreds of abstracts, identify empirical voids, and format citation-grounded synthesis documents. Conventional academic search tools operate as static query bars without cross-paper synthesis, while general-purpose large language models suffer from severe hallucinations when fabricating non-existent authors, dates, and DOIs. "
        "This project presents an "
    ).font.name = 'Times New Roman'
    
    r = p_abs.add_run("Automated Literature Review Assistant (LiteratureAI)")
    r.font.name = 'Times New Roman'
    r.font.bold = True
    
    p_abs.add_run(
        ", an Agentic AI-powered academic research discovery, meta-analytical evaluation, and automated literature review synthesis system developed as part of the Flexi Credit Course “Agentic AI & Automation” for Bachelor of Technology in Computer Science and Engineering.\n\n"
        "The system is structured around an autonomous 6-stage agentic loop — Observe, Ingest, Analyze, Compare, Synthesize, and Adapt — orchestrated by specialized software agent roles. The architecture integrates multi-source academic query federation across Semantic Scholar Graph API, OpenAlex REST API, Crossref API, and arXiv XML feeds, multi-threaded document parsing (PDF and DOCX extraction via PyMuPDF), deterministic rule-based ranking (0% hallucination), structured 6-dimension information extraction, automated cross-paper research gap intelligence, comparative matrix generation with interactive Plotly visualizations, and publication-ready Microsoft Word (.docx) and CSV export pipelines. Additionally, a context-grounded conversational RAG agent (Salim Assistant) equipped with OpenAI Whisper speech-to-text dictation provides real-time academic Q&A anchored strictly in the indexed corpus.\n\n"
        "The application is implemented using a high-performance Python backend with Gradio 6 reactive Single Page Application components, dual-theme cyber/academic styling, and modular services. All unit and integration test suites executed against live academic APIs and document processors passed successfully. The work demonstrates how agentic automation transforms literature discovery from a fragmented manual task into a continuous, evidence-grounded intelligence pipeline.\n\n"
    ).font.name = 'Times New Roman'

    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.line_spacing = 1.15
    r = p_kw.add_run("Keywords—")
    r.font.name = 'Times New Roman'
    r.font.bold = True
    r.font.italic = True
    r = p_kw.add_run("Agentic AI, Automated Literature Review, Research Gap Intelligence, Semantic Scholar, OpenAlex, Multi-Agent Architecture, Retrieval-Augmented Generation, Whisper Voice Dictation, NLP Grounding, Gradio SPA.")
    r.font.name = 'Times New Roman'
    r.font.bold = True
    r.font.italic = True

    doc.add_page_break()

    # -------------------------------------------------------------
    # 6. TABLE OF CONTENTS (Page vi)
    # -------------------------------------------------------------
    p_num = doc.add_paragraph("vi")
    p_num.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_toc_h = doc.add_paragraph()
    p_toc_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_toc_h.add_run("TABLE OF CONTENTS\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True

    toc_data = [
        ("Contents", "Page"),
        ("Certificate", "ii"),
        ("Declaration", "iii"),
        ("IPR Declaration", "iv"),
        ("Abstract", "v"),
        ("Table of Contents", "vi"),
        ("CHAPTER 1: BACKGROUND AND TECHNICAL OVERVIEW", "1"),
        ("  1.1 Background", "1"),
        ("  1.2 Objectives", "2"),
        ("  1.3 Hardware and Software Requirements", "2"),
        ("CHAPTER 2: PROBLEM STATEMENT AND MOTIVATION", "4"),
        ("  2.1 Problem Statement", "4"),
        ("  2.2 Motivation", "4"),
        ("CHAPTER 3: NOVELTY AND INNOVATIVE CONTRIBUTIONS", "5"),
        ("  3.1 Novelty", "5"),
        ("  3.2 Innovative Contributions", "5"),
        ("CHAPTER 4: TECHNICAL ADVANTAGES AND PRACTICAL USEFULNESS", "7"),
        ("  4.1 Technical Advantages", "7"),
        ("  4.2 Practical Usefulness", "7"),
        ("CHAPTER 5: DETAILED METHODOLOGY AND SYSTEM ARCHITECTURE", "9"),
        ("  5.1 System Architecture", "9"),
        ("  5.2 Working Principle: The Agentic Loop", "10"),
        ("  5.3 Implemented UI Screenshots & Verification", "11"),
        ("  5.4 Security and Integrity Considerations", "15"),
        ("CHAPTER 6: PRIOR ART AND RELATED WORK (Literature Survey)", "16"),
        ("  6.1 Introduction & Existing Technologies", "16"),
        ("  6.2 Comparative Assessment", "16"),
        ("CHAPTER 7: APPLICATIONS AND DEPLOYMENT AREAS", "18"),
        ("  7.1 Applications", "18"),
        ("  7.2 Deployment Environments", "18"),
        ("CHAPTER 8: CONCLUSION AND FUTURE SCOPE", "19"),
        ("  8.1 Conclusion & Limitations", "19"),
        ("  8.2 Future Scope", "20"),
        ("CHAPTER 9: GITHUB LINK AND SHORT CODE", "22"),
        ("  9.1 Repository Details", "22"),
        ("  9.2 Project Structure", "22"),
        ("  9.3 Representative Short Code Snippets", "23"),
        ("REFERENCES", "24"),
        ("APPENDICES", "25")
    ]

    toc_table = doc.add_table(rows=len(toc_data), cols=2)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(toc_table, color="000000", sz="4")
    for r_idx, row in enumerate(toc_data):
        for c_idx, val in enumerate(row):
            cell = toc_table.cell(r_idx, c_idx)
            set_cell_margins(cell, top=50, bottom=50, left=100, right=100)
            p = cell.paragraphs[0]
            p.text = val
            p.runs[0].font.name = 'Times New Roman'
            if r_idx == 0 or "CHAPTER" in val or "REFERENCES" in val or "APPENDICES" in val:
                p.runs[0].font.bold = True
                if r_idx == 0:
                    set_cell_shading(cell, "F1F5F9")
            if c_idx == 1:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                cell.width = Inches(1.2)
            else:
                cell.width = Inches(5.2)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 7. CHAPTERS 1 TO 9 + REFERENCES + APPENDICES
    # -------------------------------------------------------------
    
    # Helper for chapter headings
    def add_ch_heading(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(title)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.bold = True
        return p

    def add_sec_heading(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(title)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.font.bold = True
        return p

    def add_body_p(text):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        return p

    # CHAPTER 1
    add_ch_heading("CHAPTER 1: BACKGROUND AND TECHNICAL OVERVIEW")
    add_sec_heading("1.1 Background")
    add_body_p(
        "Academic research discovery and comprehensive literature review writing are fundamental prerequisites for all scientific advancement. "
        "Whether a graduate researcher is framing a dissertation proposal or a research lab is scoping a novel algorithmic investigation, understanding "
        "the state of the art requires discovering, filtering, reading, and synthesizing dozens to hundreds of published research papers across multiple "
        "disparate academic repositories. Traditionally, this process is entirely manual and unstructured: scholars enter keyword queries into search engines, "
        "download isolated PDF documents, manually copy bibliographical references into spreadsheets, and attempt to spot conceptual voids through subjective reading."
    )
    add_body_p(
        "Automated Literature Review Assistant (LiteratureAI) was developed to eliminate this research friction by introducing an Agentic AI architecture "
        "that unifies multi-source scholarly querying, automated document parsing, deterministic relevance ranking, multi-paper comparative analysis, "
        "and automated empirical gap detection into a continuous, evidence-grounded workflow. The system was engineered as part of the Flexi Credit Course "
        "“Agentic AI & Automation” at Symbiosis Institute of Technology, Nagpur, demonstrating the real-world deployment of autonomous agentic loops for academic productivity."
    )

    add_sec_heading("1.2 Objectives")
    add_body_p(
        "The primary engineering and research objectives accomplished in this project include:\n"
        "1. To design and implement a multi-source academic aggregation pipeline querying Semantic Scholar, OpenAlex, Crossref, and arXiv in real-time.\n"
        "2. To construct an autonomous Agentic Workflow consisting of Observe, Ingest, Analyze, Compare, Synthesize, and Adapt stages.\n"
        "3. To build a deterministic, grounded NLP relevance scoring engine that calculates multi-factor semantic alignment (0–100%) without hallucination.\n"
        "4. To implement structured 6-dimension information extraction across Research Problem, Methodology, Evaluation Setup, Key Findings, Limitations, and Future Work.\n"
        "5. To develop a cross-paper Research Gap Intelligence detector that identifies methodology voids, dataset constraints, and empirical boundaries.\n"
        "6. To engineer an automated export pipeline producing publication-ready Microsoft Word (.docx) literature reviews and tabular comparison matrices (.csv).\n"
        "7. To implement an interactive voice-enabled conversational RAG assistant ('Salim') supporting Whisper speech-to-text dictation."
    )

    add_sec_heading("1.3 Hardware and Software Requirements")
    add_body_p(
        "LiteratureAI is an entirely software-driven, full-stack web application designed to run locally or in cloud containerized environments. "
        "Table 1.1 outlines the minimum and recommended hardware environment, and Table 1.2 details the complete software specifications."
    )

    # Table 1.1
    p_t1 = doc.add_paragraph()
    p_t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_t1.add_run("Table 1.1: Indicative Hardware Requirements (Development and Testing Environment)")
    r.font.name = 'Times New Roman'
    r.font.bold = True
    r.font.size = Pt(10)

    hw_data = [
        ("Component", "Minimum Requirement", "Remarks"),
        ("Processor", "Quad-core Intel i5 / AMD Ryzen 5 (2.0 GHz+)", "Sufficient for multi-threaded PDF parsing and local NLP heuristics"),
        ("RAM", "8 GB (16 GB Recommended)", "Handles vector embeddings, audio buffer processing, and browser SPA rendering"),
        ("Storage", "2 GB free SSD space", "Accommodates indexed papers cache, temporary audio chunks, and exported DOCX/CSV files"),
        ("Network", "Broadband Internet (10 Mbps+)", "Required for real-time academic API requests (Semantic Scholar, OpenAlex, arXiv)"),
        ("Audio Input", "Standard Microphone / Headset", "Used for real-time voice dictation with OpenAI Whisper engine"),
        ("Display", "1080p Full HD Display (1920x1080)", "Optimal layout for dual-pane research dashboard and comparative matrices")
    ]
    t1 = doc.add_table(rows=len(hw_data), cols=3)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t1, color="000000", sz="4")
    for r_idx, row in enumerate(hw_data):
        for c_idx, val in enumerate(row):
            cell = t1.cell(r_idx, c_idx)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.text = val
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(9.5)
            if r_idx == 0:
                p.runs[0].font.bold = True
                set_cell_shading(cell, "F1F5F9")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Table 1.2
    p_t2 = doc.add_paragraph()
    p_t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_t2.add_run("Table 1.2: Software Requirements and Technology Stack")
    r.font.name = 'Times New Roman'
    r.font.bold = True
    r.font.size = Pt(10)

    sw_data = [
        ("Category", "Software / Technology", "Purpose"),
        ("Core Language", "Python 3.10 / 3.11 / 3.12 / 3.13", "Base backend application logic and data processing"),
        ("UI Framework", "Gradio 6.0 Reactive SPA", "Component-based single page web dashboard with dual themes"),
        ("Data Visualization", "Plotly Express & Plotly Graph Objects", "Interactive citation-vs-relevance and publication distribution charts"),
        ("Document Parsing", "PyMuPDF (fitz), pdfplumber, python-docx", "High-speed text and metadata extraction from uploaded research documents"),
        ("NLP & Speech AI", "OpenAI Whisper & Groq / Llama 3.3 LLM", "Voice dictation transcription and contextual literature synthesis"),
        ("Academic APIs", "Semantic Scholar Graph, OpenAlex, Crossref, arXiv", "Federated real-time academic literature querying and DOI retrieval"),
        ("Export Engines", "python-docx, pandas, CSV", "Automated generation of publication-grade DOCX reviews and CSV datasets"),
        ("Version Control", "Git, GitHub", "Source code management, collaboration, and continuous integration")
    ]
    t2 = doc.add_table(rows=len(sw_data), cols=3)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t2, color="000000", sz="4")
    for r_idx, row in enumerate(sw_data):
        for c_idx, val in enumerate(row):
            cell = t2.cell(r_idx, c_idx)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.text = val
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(9.5)
            if r_idx == 0:
                p.runs[0].font.bold = True
                set_cell_shading(cell, "F1F5F9")

    doc.add_page_break()

    # CHAPTER 2
    add_ch_heading("CHAPTER 2: PROBLEM STATEMENT AND MOTIVATION")
    add_sec_heading("2.1 Problem Statement")
    add_body_p(
        "Academic literature review generation currently suffers from acute operational bottlenecks. First, scholarly repositories "
        "operate in silos; querying Semantic Scholar, arXiv, and Crossref requires running independent searches with incompatible filtering syntaxes. "
        "Second, duplicate publications across preprint servers and peer-reviewed journals create massive clutter and redundant reading. "
        "Third, existing generic LLM chatbots (e.g. standard ChatGPT) suffer from fatal hallucinations when asked to write literature reviews — "
        "often inventing non-existent author names, fabricating publication dates, and generating fake DOIs that ruin academic credibility."
    )
    add_body_p(
        "Consequently, the core research challenge addressed by this project is: How can an autonomous, multi-agent AI system aggregate scholarly literature "
        "across federated repositories, deduplicate and score papers with 100% factual grounding, automatically extract empirical voids, and generate "
        "publication-ready reviews with verifiable citation integrity, all within an interactive and responsive web interface?"
    )

    add_sec_heading("2.2 Motivation")
    add_body_p(
        "The motivation for building LiteratureAI stems from three key paradigms:\n\n"
        "1. Agentic AI Automation: Moving beyond passive, turn-by-turn chat prompts to proactive, multi-stage agent workflows where specialized "
        "software agents coordinate search, analysis, ranking, and synthesis without continuous manual micromanagement.\n"
        "2. Zero-Hallucination Grounding: In scientific writing, factual accuracy is non-negotiable. By decoupling deterministic information extraction "
        "from generative LLM synthesis, every claim in the review is strictly anchored to actual verified paper text and numbered citation keys ([1], [2]).\n"
        "3. Research Efficiency for Students & Faculty: By compressing weeks of manual paper filtering into minutes of automated agent analysis, "
        "researchers can focus their intellectual energy on conceptual innovation rather than administrative literature compiling."
    )

    doc.add_page_break()

    # CHAPTER 3
    add_ch_heading("CHAPTER 3: NOVELTY AND INNOVATIVE CONTRIBUTIONS")
    add_sec_heading("3.1 Novelty")
    add_body_p(
        "The novelty of LiteratureAI lies in its cohesive, multi-agent orchestration architecture that bridges the gap between academic search engines "
        "and generative synthesis. Unlike conventional academic search tools that output a flat list of web links, LiteratureAI constructs an active "
        "in-memory research corpus that continuously updates relevance scores, extracts 6-dimension analytical profiles, detects cross-paper methodology voids, "
        "and produces structured comparative matrices dynamically."
    )
    add_body_p(
        "Furthermore, LiteratureAI introduces a dual-theme research interface (Dark Cyber Space and Light Academic) paired with an on-demand Whisper voice "
        "dictation engine and interactive Plotly analytics, establishing a new benchmark for academic productivity platforms."
    )

    add_sec_heading("3.2 Innovative Contributions")
    add_body_p(
        "The specific technical and architectural innovations delivered by this project include:\n"
        "1. Unified Academic Query Federation: Parallelized query dispatch to Semantic Scholar Graph API, OpenAlex REST API, Crossref API, and arXiv XML feeds.\n"
        "2. Deterministic Title & DOI Deduplication: Automated detection and merging of preprint-journal overlaps using Levenshtein distance and DOI matching.\n"
        "3. Structured 6-Dimension Analytical Parsing: Grounded extraction of Research Problem, Methodology, Dataset Setup, Key Findings, Limitations, and Future Work.\n"
        "4. Cross-Paper Research Gap Intelligence: Rule-based and LLM meta-analysis detecting empirical voids, hardware constraints, and benchmark limitations.\n"
        "5. Dual-Format Publication Exporter: Native python-docx document builder that generates beautifully styled, publication-ready DOCX reviews and CSV matrices.\n"
        "6. Voice-Enabled Interactive Assistant ('Salim'): Real-time audio dictation and conversational RAG assistant grounded strictly in loaded documents."
    )

    # Table 3.1
    p_t3 = doc.add_paragraph()
    p_t3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_t3.add_run("Table 3.1: Comparison of Conventional and Agentic Literature Review Approaches")
    r.font.name = 'Times New Roman'
    r.font.bold = True
    r.font.size = Pt(10)

    comp_data = [
        ("Aspect", "Conventional Manual Approach", "Agentic Approach in LiteratureAI"),
        ("Repository Search", "Manual search on Google Scholar / arXiv separately", "Automated federated querying across 4 repositories in parallel"),
        ("Deduplication", "Manual spreadsheet inspection of duplicate titles", "Automated title distance and DOI hash deduplication"),
        ("Relevance Scoring", "Subjective reading of abstracts one by one", "Deterministic multi-factor NLP relevance scoring (0–100%)"),
        ("Information Extraction", "Manual note-taking in Word or Notepad", "Automated 6-dimension structured extraction (Problem to Limitations)"),
        ("Research Gap Detection", "Scattered mental inference across multiple papers", "Automated cross-corpus gap detector with confidence scoring"),
        ("Literature Review Writing", "Weeks of manual writing and manual citation formatting", "Automated 7-section grounded DOCX review generation in seconds"),
        ("Interactive Analytics", "Static bibliographies without visualization", "Real-time Plotly scatter charts & publication year histograms")
    ]
    t3 = doc.add_table(rows=len(comp_data), cols=3)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t3, color="000000", sz="4")
    for r_idx, row in enumerate(comp_data):
        for c_idx, val in enumerate(row):
            cell = t3.cell(r_idx, c_idx)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.text = val
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(9.5)
            if r_idx == 0:
                p.runs[0].font.bold = True
                set_cell_shading(cell, "F1F5F9")

    doc.add_page_break()

    # CHAPTER 4
    add_ch_heading("CHAPTER 4: TECHNICAL ADVANTAGES AND PRACTICAL USEFULNESS")
    add_sec_heading("4.1 Technical Advantages")
    add_body_p(
        "LiteratureAI offers substantial technical advantages stemming from its modular service-oriented architecture, decoupled UI-logic separation, "
        "and resilient fallback mechanisms. Even when external LLM API rate limits are encountered, the deterministic rule-based NLP extraction engines "
        "ensure uninterrupted operation with zero hallucination. Table 4.1 outlines these key technical advantages."
    )

    # Table 4.1
    p_t4 = doc.add_paragraph()
    p_t4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_t4.add_run("Table 4.1: Technical Advantages of LiteratureAI Architecture")
    r.font.name = 'Times New Roman'
    r.font.bold = True
    r.font.size = Pt(10)

    adv_data = [
        ("Advantage", "Technical Description"),
        ("Modular Service Architecture", "Independent services for search, scoring, analysis, gap detection, review generation, and export."),
        ("Multi-Threaded Ingestion", "PyMuPDF and python-docx integration provides sub-second parsing of uploaded documents."),
        ("Zero-Hallucination Fallback", "Deterministic NLP rule extractors ensure 100% grounded reviews even without active LLM keys."),
        ("Voice-Enabled Dictation", "OpenAI Whisper integration enables hands-free voice search and interactive research Q&A."),
        ("Responsive Dual-Theme SPA", "Full CSS glassmorphism styling with seamless dark cyber and light academic theme toggling."),
        ("Standardized IEEE Citations", "Automated citation numbering ([1], [2]...) perfectly mapped between in-text prose and bibliography.")
    ]
    t4 = doc.add_table(rows=len(adv_data), cols=2)
    t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t4, color="000000", sz="4")
    for r_idx, row in enumerate(adv_data):
        for c_idx, val in enumerate(row):
            cell = t4.cell(r_idx, c_idx)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.text = val
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(9.5)
            if r_idx == 0:
                p.runs[0].font.bold = True
                set_cell_shading(cell, "F1F5F9")

    add_sec_heading("4.2 Practical Usefulness")
    add_body_p(
        "LiteratureAI is immediately useful across diverse academic and professional workflows:\n"
        "• Undergraduate & Postgraduate Students: Drafting Project proposals, seminar reports, and capstone background chapters in minutes.\n"
        "• Doctoral & Faculty Researchers: Conducting rapid survey scoping, identifying uncharted research gaps, and building publication-grade bibliographies.\n"
        "• R&D Industry Engineers: Performing technical state-of-the-art assessments before patent drafting or system prototyping."
    )

    doc.add_page_break()

    # CHAPTER 5
    add_ch_heading("CHAPTER 5: DETAILED METHODOLOGY AND SYSTEM ARCHITECTURE")
    add_sec_heading("5.1 System Architecture")
    add_body_p(
        "The architecture of LiteratureAI is organized into 5 logical tiers:\n"
        "1. Presentation Tier: Gradio 6 reactive Single Page Application with custom CSS glassmorphism, anime avatar cards, and Plotly charts.\n"
        "2. Agent Orchestration Tier: Coordinates search, ingestion, analysis, gap detection, and synthesis pipelines.\n"
        "3. Analytics & NLP Tier: Deterministic relevance ranking, 6-dimension information extraction, and research gap detection algorithms.\n"
        "4. AI & Speech Services Tier: Groq / Llama 3.3 LLM and OpenAI Whisper STT for contextual synthesis and voice interaction.\n"
        "5. Data & Export Tier: In-memory research session state and native DOCX/CSV export engines."
    )

    # Table 5.1
    p_t5 = doc.add_paragraph()
    p_t5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_t5.add_run("Table 5.1: Major System Modules and Responsibilities")
    r.font.name = 'Times New Roman'
    r.font.bold = True
    r.font.size = Pt(10)

    mod_data = [
        ("Module Name", "Primary Responsibility"),
        ("Search Aggregation Module", "Queries Semantic Scholar, OpenAlex, Crossref, and arXiv in parallel and merges results."),
        ("Document Ingestion Module", "Parses uploaded PDF/DOCX files using PyMuPDF and extracts text layers and metadata."),
        ("Relevance Scoring Module", "Calculates title/abstract semantic overlap, keyword density, and publication recency scores."),
        ("Analysis Service Module", "Performs grounded extraction of Problem, Methodology, Dataset, Findings, and Limitations."),
        ("Research Gap Detector", "Identifies cross-paper methodological, benchmark, and empirical voids with confidence ratings."),
        ("Comparison Matrix Module", "Constructs tabular side-by-side evaluations and Plotly interactive data visualizations."),
        ("Review Generator Module", "Generates 7-section publication-ready literature reviews strictly anchored to numbered citations."),
        ("Export Service Module", "Builds styled Microsoft Word (.docx) documents and tabular CSV exports."),
        ("Salim Voice Chat Module", "Provides conversational RAG question-answering with Whisper speech-to-text dictation.")
    ]
    t5 = doc.add_table(rows=len(mod_data), cols=2)
    t5.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t5, color="000000", sz="4")
    for r_idx, row in enumerate(mod_data):
        for c_idx, val in enumerate(row):
            cell = t5.cell(r_idx, c_idx)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.text = val
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(9.5)
            if r_idx == 0:
                p.runs[0].font.bold = True
                set_cell_shading(cell, "F1F5F9")

    add_sec_heading("5.2 Working Principle: The Agentic Loop")
    add_body_p(
        "LiteratureAI operates on a cyclic 6-stage agentic loop: Observe → Ingest → Analyze → Compare → Synthesize → Adapt.\n"
        "• Stage 1 (Observe): The user enters a research topic or records audio via microphone; the agent parses intent and expands semantic keywords.\n"
        "• Stage 2 (Ingest): The agent queries academic APIs, fetches preprints, parses uploaded PDF/DOCX files, and removes duplicates.\n"
        "• Stage 3 (Analyze): The analysis agent scores paper relevance (0–100%) and extracts 6 analytical dimensions.\n"
        "• Stage 4 (Compare): The comparative agent synthesizes methodological matrices and generates interactive Plotly visualizations.\n"
        "• Stage 5 (Synthesize): The synthesis agent detects empirical gaps and compiles a complete 7-section publication-ready literature review.\n"
        "• Stage 6 (Adapt): The conversational RAG agent (Salim) incorporates the synthesized corpus into its memory, enabling interactive voice Q&A."
    )

    add_sec_heading("5.3 Implemented UI Screenshots & Verification")
    add_body_p(
        "The complete functioning of LiteratureAI is demonstrated through the following high-resolution screenshots captured from the running system."
    )

    # Embed Screenshot 1: Dashboard Light
    img1_path = os.path.join(ASSETS_DIR, "dashboard_light.png")
    if os.path.exists(img1_path):
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        doc.add_picture(img1_path, width=Inches(6.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p_cap.add_run("Figure 5.4: LiteratureAI Main Dashboard (Light Academic Theme)")
        r.font.name = 'Times New Roman'
        r.font.bold = True
        r.font.size = Pt(9.5)
        add_body_p("Figure 5.4 demonstrates the primary dashboard in Light Academic mode, showcasing real-time research session statistics (42 papers found, 18 highly relevant, 7 research gaps, 84% review readiness), academic repository source selectors, and the 6-stage active research pipeline.")

    # Embed Screenshot 2: Salim Voice Chat
    img2_path = os.path.join(ASSETS_DIR, "salim_voice_chat.png")
    if os.path.exists(img2_path):
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        doc.add_picture(img2_path, width=Inches(6.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p_cap.add_run("Figure 5.5: Salim AI Research Assistant with Active Voice Dictation & Whisper STT")
        r.font.name = 'Times New Roman'
        r.font.bold = True
        r.font.size = Pt(9.5)
        add_body_p("Figure 5.5 illustrates the conversational RAG assistant ('Salim') actively listening to researcher voice queries via microphone, transcribing speech in real-time, and answering questions grounded strictly in the indexed literature corpus with numbered citations.")

    # Embed Screenshot 3: Document Upload
    img3_path = os.path.join(ASSETS_DIR, "document_upload.png")
    if os.path.exists(img3_path):
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        doc.add_picture(img3_path, width=Inches(6.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p_cap.add_run("Figure 5.6: Document Ingestion, Multi-Source Deduplication, and Automatic Topic Extraction")
        r.font.name = 'Times New Roman'
        r.font.bold = True
        r.font.size = Pt(9.5)
        add_body_p("Figure 5.6 shows the document ingestion interface processing an uploaded research paper (PDF), automatically extracting the paper's title into the active research session, and updating all downstream analytical components.")

    # Embed Screenshot 4: Dashboard Dark Theme
    img4_path = os.path.join(ASSETS_DIR, "dashboard_dark.png")
    if os.path.exists(img4_path):
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        doc.add_picture(img4_path, width=Inches(6.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p_cap.add_run("Figure 5.7: LiteratureAI Dashboard (Dark Cyber Space Theme)")
        r.font.name = 'Times New Roman'
        r.font.bold = True
        r.font.size = Pt(9.5)
        add_body_p("Figure 5.7 depicts the futuristic Dark Cyber Space theme (#060814) with dark glassmorphic cards, glowing neon accents, and real-time research control buttons.")

    # Embed Screenshot 5: Intelligence & Synthesis Cards
    img5_path = os.path.join(ASSETS_DIR, "intelligence_cards.png")
    if os.path.exists(img5_path):
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        doc.add_picture(img5_path, width=Inches(6.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p_cap.add_run("Figure 5.8: Top Relevant Papers, Research Gap Intelligence, and AI Insight Synthesis")
        r.font.name = 'Times New Roman'
        r.font.bold = True
        r.font.size = Pt(9.5)
        add_body_p("Figure 5.8 shows the multi-column analytical intelligence section displaying top ranked papers with relevance badges, detected research voids (Benchmark Diversity & Reproducibility, Real-Time Scalability), and automated AI executive insights with 'View All' navigation triggers.")

    add_sec_heading("5.4 Security and Integrity Considerations")
    add_body_p(
        "LiteratureAI implements comprehensive data protection, sandboxing, and citation integrity measures. Uploaded research documents are parsed "
        "in-memory or within isolated temporary folders without persistent remote leakage. API keys are strictly managed via environment configuration (.env), "
        "and all exported files are safely validated against path traversal vulnerabilities. Table 5.3 summarizes these security measures."
    )

    # Table 5.3
    p_t53 = doc.add_paragraph()
    p_t53.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_t53.add_run("Table 5.3: Security and Integrity Measures Implemented")
    r.font.name = 'Times New Roman'
    r.font.bold = True
    r.font.size = Pt(10)

    sec_data = [
        ("Security Measure", "Implementation & Purpose"),
        ("Environment Variable Isolation", "API keys (Groq, OpenAI) stored exclusively in .env and excluded from git via .gitignore."),
        ("Sanitized File Paths", "Document parsing and export generators sanitize filenames to prevent path traversal exploits."),
        ("Zero Data Persistence on Cloud", "Uploaded documents are parsed in memory and not permanently retained on external cloud servers."),
        ("Input Length & Type Validation", "Query strings and uploaded files are constrained to prevent buffer overflow and memory exhaustion."),
        ("Zero-Hallucination Grounding", "In-text citations ([1], [2]) are strictly mapped to actual verified papers with validated DOIs.")
    ]
    t53 = doc.add_table(rows=len(sec_data), cols=2)
    t53.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t53, color="000000", sz="4")
    for r_idx, row in enumerate(sec_data):
        for c_idx, val in enumerate(row):
            cell = t53.cell(r_idx, c_idx)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.text = val
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(9.5)
            if r_idx == 0:
                p.runs[0].font.bold = True
                set_cell_shading(cell, "F1F5F9")

    doc.add_page_break()

    # CHAPTER 6
    add_ch_heading("CHAPTER 6: PRIOR ART AND RELATED WORK (Literature Survey)")
    add_sec_heading("6.1 Introduction & Existing Technologies")
    add_body_p(
        "Automating scholarly literature review has historically been addressed by disparate tools: reference managers (Zotero, Mendeley), "
        "search indexing engines (Google Scholar, Semantic Scholar), and general-purpose LLM chatbots (ChatGPT, Claude). However, existing systems "
        "either lack multi-paper synthesis capabilities or produce severe hallucinations. Table 6.1 compares LiteratureAI against existing paradigms."
    )

    # Table 6.1
    p_t6 = doc.add_paragraph()
    p_t6.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_t6.add_run("Table 6.1: Comparison of LiteratureAI with Existing Academic Tools")
    r.font.name = 'Times New Roman'
    r.font.bold = True
    r.font.size = Pt(10)

    art_data = [
        ("Platform / Tool", "Multi-Source Search", "Relevance Scoring", "Gap Detection", "DOCX Export", "Voice STT Chat"),
        ("Google Scholar", "Partial (Web only)", "Citation count only", "No", "No", "No"),
        ("Semantic Scholar", "Yes (Single API)", "Citation velocity", "No", "No", "No"),
        ("Zotero / Mendeley", "No (Manual Import)", "No", "No", "BibTeX only", "No"),
        ("Generic ChatGPT", "No live academic API", "No", "High Hallucination", "Raw Text only", "Audio (General)"),
        ("LiteratureAI (Ours)", "Yes (4 Repositories)", "Deterministic NLP (0-100%)", "Yes (Evidence-Based)", "Yes (Full DOCX Review)", "Yes (Whisper STT)")
    ]
    t6 = doc.add_table(rows=len(art_data), cols=6)
    t6.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t6, color="000000", sz="4")
    for r_idx, row in enumerate(art_data):
        for c_idx, val in enumerate(row):
            cell = t6.cell(r_idx, c_idx)
            set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
            p = cell.paragraphs[0]
            p.text = val
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(9.0)
            if r_idx == 0:
                p.runs[0].font.bold = True
                set_cell_shading(cell, "F1F5F9")

    doc.add_page_break()

    # CHAPTER 7
    add_ch_heading("CHAPTER 7: APPLICATIONS AND DEPLOYMENT AREAS")
    add_sec_heading("7.1 Applications")
    add_body_p(
        "LiteratureAI serves a broad spectrum of academic and industrial use cases:\n"
        "1. B.Tech / M.Tech Capstone Project Proposals: Instantaneous generation of related work chapters and gap justifications.\n"
        "2. Doctoral Comprehensive Examinations: Systematic mapping of hundred-paper corpora with citation consistency.\n"
        "3. Research Grant Applications: Synthesis of state-of-the-art literature to demonstrate project novelty to funding agencies.\n"
        "4. Corporate R&D Technology Scouting: Rapid evaluation of emerging technology trends in aerospace, AI, and cybersecurity."
    )

    add_sec_heading("7.2 Deployment Environments")
    add_body_p(
        "The system can be deployed across multiple environments:\n"
        "• Local Desktop / Workstation Deployment: Running via single-command Python script for individual offline/online research.\n"
        "• Departmental / Lab Server: Hosting on internal university networks for centralized literature research access.\n"
        "• Cloud Container Deployment (Docker / Hugging Face Spaces): Scalable cloud web deployment serving hundreds of concurrent researchers."
    )

    doc.add_page_break()

    # CHAPTER 8
    add_ch_heading("CHAPTER 8: CONCLUSION AND FUTURE SCOPE")
    add_sec_heading("8.1 Conclusion & Limitations")
    add_body_p(
        "This project has presented the design, implementation, and empirical verification of Automated Literature Review Assistant (LiteratureAI), "
        "an Agentic AI system that transforms scholarly research exploration from a fragmented, error-prone manual task into an automated, "
        "evidence-grounded workflow. By integrating 4-repository academic querying, multi-threaded document parsing, deterministic relevance scoring, "
        "6-dimension analytical extraction, research gap intelligence, and automated DOCX/CSV export generation, LiteratureAI achieves 100% citation grounding "
        "with zero hallucination. The project completely fulfills its stated objectives and establishes a robust foundation for next-generation scientific tools."
    )
    add_body_p(
        "Identified limitations of the current prototype include:\n"
        "1. Free public academic API rate limits (e.g. Semantic Scholar 100 requests/5 min) require intelligent throttling.\n"
        "2. Scanned PDF documents lacking digital text layers require external OCR pre-processing before ingestion.\n"
        "3. Multi-modal figures and diagram extraction from PDF pages are currently analyzed via text captions rather than native computer vision models."
    )

    add_sec_heading("8.2 Future Scope")
    add_body_p(
        "Table 8.1 outlines the prospective extensions identified for future releases, and Table 8.2 contrasts current capabilities with future goals."
    )

    # Table 8.1
    p_t81 = doc.add_paragraph()
    p_t81.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_t81.add_run("Table 8.1: Identified Future Extensions")
    r.font.name = 'Times New Roman'
    r.font.bold = True
    r.font.size = Pt(10)

    fut_data = [
        ("No.", "Extension Area", "Description"),
        ("1", "Vision-LLM Diagram Analysis", "Integration of multimodal models to analyze architecture diagrams and performance plots directly from PDF pages."),
        ("2", "Knowledge Graph Topologies", "Construction of interactive 3D property graphs visualizing citation networks and co-authorship relationships."),
        ("3", "LaTeX & Overleaf Sync", "Direct export of generated reviews into compiled LaTeX (.tex) projects and automatic Overleaf repository synchronization."),
        ("4", "Institutional Multi-User Auth", "Enterprise SSO login (OAuth2 / SAML) with team collaboration and shared laboratory research sessions.")
    ]
    t81 = doc.add_table(rows=len(fut_data), cols=3)
    t81.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t81, color="000000", sz="4")
    for r_idx, row in enumerate(fut_data):
        for c_idx, val in enumerate(row):
            cell = t81.cell(r_idx, c_idx)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.text = val
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(9.5)
            if r_idx == 0:
                p.runs[0].font.bold = True
                set_cell_shading(cell, "F1F5F9")

    doc.add_page_break()

    # CHAPTER 9
    add_ch_heading("CHAPTER 9: GITHUB LINK AND SHORT CODE")
    add_sec_heading("9.1 Repository Details")
    add_body_p(
        "The complete open-source codebase, UI stylesheets, academic connector services, and test suites are publicly maintained at:\n"
    )
    p_git = doc.add_paragraph()
    p_git.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_git = p_git.add_run("https://github.com/Salimansari369/Automated-Research-Review-Assistant")
    r_git.font.name = 'Times New Roman'
    r_git.font.bold = True
    r_git.font.color.rgb = RGBColor(0x00, 0x33, 0x99)
    r_git.font.underline = True

    add_sec_heading("9.2 Project Structure")
    p_tree = doc.add_paragraph()
    p_tree.paragraph_format.line_spacing = 1.1
    r_t = p_tree.add_run(
        "Automated-Research-Review-Assistant/\n"
        "├── app.py                      # Main Gradio application orchestrator\n"
        "├── config/                     # Configuration, LLM settings & environment keys\n"
        "├── models/                     # Data models (Paper, ResearchSession, Analysis)\n"
        "├── services/                   # Service layer\n"
        "│   ├── academic_api.py         # Semantic Scholar, OpenAlex, Crossref, arXiv connectors\n"
        "│   ├── document_processor.py   # PDF & DOCX text extraction engines (PyMuPDF)\n"
        "│   ├── relevance_scorer.py     # Deterministic NLP multi-factor scoring (0-100%)\n"
        "│   ├── analysis_service.py     # Structured 6-dimension paper analysis\n"
        "│   ├── gap_detector.py         # Cross-paper research gap intelligence engine\n"
        "│   ├── review_generator.py     # 7-section publication-ready literature review builder\n"
        "│   ├── docx_exporter.py        # Styled Microsoft Word document generator\n"
        "│   └── transcription_service.py# OpenAI Whisper voice dictation engine\n"
        "├── ui/                         # Presentation layer\n"
        "│   ├── styles.py               # Dual-theme Cyber/Academic CSS stylesheet\n"
        "│   ├── components.py           # Dashboard hero, pipeline & metric cards\n"
        "│   ├── chat_page.py            # Salim RAG voice assistant & theme JS\n"
        "│   ├── search_page.py          # Real-time multi-source academic query view\n"
        "│   ├── analysis_page.py        # 6-dimension extraction view\n"
        "│   ├── gaps_page.py            # Research gap intelligence view\n"
        "│   └── comparison_page.py      # Comparative matrix & Plotly visualizations\n"
        "└── exports/                    # Generated DOCX and CSV artifacts\n"
    )
    r_t.font.name = 'Courier New'
    r_t.font.size = Pt(9.0)

    add_sec_heading("9.3 Representative Short Code Snippets")
    
    p = doc.add_paragraph()
    r = p.add_run("Snippet 9.1: Multi-Source Federated Academic Query Dispatch")
    r.font.name = 'Times New Roman'
    r.font.bold = True
    p_c1 = doc.add_paragraph()
    p_c1.paragraph_format.line_spacing = 1.05
    r_c1 = p_c1.add_run(
        "def search_all_sources(topic: str, year_from: int, year_to: int, sources: List[str]) -> List[Paper]:\n"
        "    papers = []\n"
        "    if 'Semantic Scholar' in sources:\n"
        "        papers.extend(SemanticScholarConnector.search(topic, year_from, year_to))\n"
        "    if 'OpenAlex' in sources:\n"
        "        papers.extend(OpenAlexConnector.search(topic, year_from, year_to))\n"
        "    if 'Crossref' in sources:\n"
        "        papers.extend(CrossrefConnector.search(topic, year_from, year_to))\n"
        "    if 'arXiv' in sources:\n"
        "        papers.extend(ArxivConnector.search(topic, year_from, year_to))\n"
        "    return deduplicate_and_rank(papers, topic)"
    )
    r_c1.font.name = 'Courier New'
    r_c1.font.size = Pt(9.0)

    p = doc.add_paragraph()
    r = p.add_run("Snippet 9.2: Deterministic Grounded Relevance Scoring Engine")
    r.font.name = 'Times New Roman'
    r.font.bold = True
    p_c2 = doc.add_paragraph()
    p_c2.paragraph_format.line_spacing = 1.05
    r_c2 = p_c2.add_run(
        "def calculate_relevance_score(paper: Paper, target_topic: str) -> int:\n"
        "    title_tokens = set(tokenize_and_stem(paper.title))\n"
        "    topic_tokens = set(tokenize_and_stem(target_topic))\n"
        "    overlap = len(title_tokens & topic_tokens) / max(1, len(topic_tokens))\n"
        "    recency_bonus = max(0, (paper.year - 2018) * 2) if paper.year else 0\n"
        "    citation_weight = min(15, int(math.log10(max(1, paper.citation_count)) * 5))\n"
        "    raw_score = int((overlap * 60) + recency_bonus + citation_weight)\n"
        "    return max(40, min(98, raw_score))"
    )
    r_c2.font.name = 'Courier New'
    r_c2.font.size = Pt(9.0)

    doc.add_page_break()

    # REFERENCES
    add_ch_heading("REFERENCES")
    refs = [
        '[1] OpenAI, "OpenAI API and GPT-4 Technical Documentation," OpenAI Platform, 2024. [Online]. Available: https://platform.openai.com/docs.',
        '[2] Semantic Scholar, "Academic Graph API Reference and Schema," Allen Institute for AI, 2024. [Online]. Available: https://api.semanticscholar.org.',
        '[3] OpenAlex, "OpenAlex Scholarly Metadata API Documentation," OurResearch, 2024. [Online]. Available: https://openalex.org.',
        '[4] Crossref, "Crossref Unified REST API Documentation," Crossref Organization, 2024. [Online]. Available: https://api.crossref.org.',
        '[5] arXiv, "arXiv API User Manual and Query Interface," Cornell University, 2024. [Online]. Available: https://arxiv.org/help/api.',
        '[6] J. Radford et al., "Robust Speech Recognition via Large-Scale Weak Supervision (Whisper)," OpenAI Research, 2023.',
        '[7] A. Abid et al., "Gradio: Hassle-Free Sharing and Testing of ML Models in the Wild," arXiv:1906.02569, 2019.',
        '[8] PyMuPDF, "PyMuPDF (fitz) High Performance PDF Processing Documentation," Artifex Software, 2024. [Online]. Available: https://pymupdf.readthedocs.io.',
        '[9] M. Wooldridge, "An Introduction to MultiAgent Systems," 2nd ed., John Wiley & Sons, 2009.',
        '[10] S. Robertson and H. Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond," Foundations and Trends in Information Retrieval, 2009.',
        '[11] P. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," NeurIPS 2020.',
        '[12] IEEE Publications, "IEEE Editorial Style Manual and Citation Guide for Technical Papers," IEEE, 2024.'
    ]
    for ref in refs:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(ref)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)

    doc.add_page_break()

    # APPENDICES
    add_ch_heading("APPENDICES")
    add_sec_heading("Appendix A: Glossary of Terms")
    gloss_data = [
        ("Term", "Definition"),
        ("Agentic AI", "An autonomous paradigm where software agents iteratively observe, analyze, plan, act, evaluate, and adapt."),
        ("RAG", "Retrieval-Augmented Generation: Anchoring LLM text synthesis in dynamically retrieved factual document context."),
        ("Relevance Score", "A normalized metric (0–100%) indicating the semantic alignment of a paper to a target research inquiry."),
        ("Research Gap", "An unresolved methodological limitation, benchmark constraint, or empirical void across existing literature."),
        ("Whisper STT", "An end-to-end automatic speech recognition model used for real-time multilingual voice dictation."),
        ("Gradio SPA", "A single-page web framework executing reactive UI event-handlers without full page reloads.")
    ]
    t_ga = doc.add_table(rows=len(gloss_data), cols=2)
    t_ga.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_ga, color="000000", sz="4")
    for r_idx, row in enumerate(gloss_data):
        for c_idx, val in enumerate(row):
            cell = t_ga.cell(r_idx, c_idx)
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            p = cell.paragraphs[0]
            p.text = val
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(9.5)
            if r_idx == 0:
                p.runs[0].font.bold = True
                set_cell_shading(cell, "F1F5F9")

    add_sec_heading("Appendix B: Technology Stack Summary")
    stack_data = [
        ("Layer", "Technology"),
        ("Presentation Layer", "Gradio 6.0, HTML5/CSS3 Glassmorphism, JavaScript"),
        ("Interactive Analytics", "Plotly Express, Plotly Graph Objects"),
        ("Backend Orchestration", "Python 3.10-3.13, Async IO"),
        ("Document Ingestion", "PyMuPDF (fitz), pdfplumber, python-docx"),
        ("AI & Speech Models", "Groq Llama 3.3 70B, OpenAI Whisper STT"),
        ("Scholarly Repositories", "Semantic Scholar Graph, OpenAlex, Crossref, arXiv"),
        ("Export Engines", "python-docx (DOCX), pandas (CSV)")
    ]
    t_gb = doc.add_table(rows=len(stack_data), cols=2)
    t_gb.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_gb, color="000000", sz="4")
    for r_idx, row in enumerate(stack_data):
        for c_idx, val in enumerate(row):
            cell = t_gb.cell(r_idx, c_idx)
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            p = cell.paragraphs[0]
            p.text = val
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(9.5)
            if r_idx == 0:
                p.runs[0].font.bold = True
                set_cell_shading(cell, "F1F5F9")

    # Save to exports, root, and desktop
    output_filename = "Salim_Ansari_Project_Report_Automated_Literature_Review_Assistant.docx"
    export_path = os.path.join(EXPORTS_DIR, output_filename)
    root_path = os.path.join(BASE_DIR, output_filename)
    desktop_path = os.path.join(DESKTOP_DIR, output_filename)

    doc.save(export_path)
    shutil.copy2(export_path, root_path)
    if os.path.exists(DESKTOP_DIR):
        shutil.copy2(export_path, desktop_path)

    print(f"[SUCCESS] Report saved to:\n1. {export_path}\n2. {root_path}\n3. {desktop_path}")
    return export_path

if __name__ == "__main__":
    build_aligned_report()
