import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from typing import Dict, Any, List
from config.settings import EXPORTS_DIR
from utils.logging_config import logger

def _set_cell_background(cell, fill_hex):
    """Sets background color of a docx table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

class DocxExporter:
    @classmethod
    def export(cls, review_data: Dict[str, Any], filename_prefix: str = "Literature_Review") -> str:
        """Exports review_data to a styled Word (.docx) document."""
        doc = Document()

        # Page margins
        for section in doc.sections:
            section.top_margin = Inches(1.0)
            section.bottom_margin = Inches(1.0)
            section.left_margin = Inches(1.0)
            section.right_margin = Inches(1.0)

        # Document Title
        title_p = doc.add_paragraph()
        title_p.paragraph_format.space_before = Pt(0)
        title_p.paragraph_format.space_after = Pt(6)
        title_p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        title_run = title_p.add_run(f"Literature Review: {review_data.get('topic', 'Autonomous Systems')}")
        title_run.font.name = "Calibri"
        title_run.font.size = Pt(22)
        title_run.font.bold = True
        title_run.font.color.rgb = RGBColor(79, 70, 229)  # Deep indigo

        # Subtitle
        sub_p = doc.add_paragraph()
        sub_p.paragraph_format.space_after = Pt(18)
        sub_run = sub_p.add_run("Synthesized by LiteratureAI • AI-Powered Automated Literature Review Assistant")
        sub_run.font.name = "Calibri"
        sub_run.font.size = Pt(11)
        sub_run.font.italic = True
        sub_run.font.color.rgb = RGBColor(100, 116, 139)

        # Horizontal separator line
        sections = review_data.get("sections", {})
        
        for heading, body in sections.items():
            # Section Heading
            h_p = doc.add_paragraph()
            h_p.paragraph_format.space_before = Pt(14)
            h_p.paragraph_format.space_after = Pt(6)
            h_run = h_p.add_run(heading)
            h_run.font.name = "Calibri"
            h_run.font.size = Pt(14)
            h_run.font.bold = True
            h_run.font.color.rgb = RGBColor(67, 56, 202)

            # Check if this section has markdown table
            if "|" in body and "---" in body:
                lines = [line.strip() for line in body.split("\n") if line.strip()]
                table_lines = [l for l in lines if l.startswith("|") and l.endswith("|")]
                if len(table_lines) >= 3:
                    headers = [c.strip() for c in table_lines[0].strip("|").split("|")]
                    rows_data = []
                    for row_line in table_lines[2:]:
                        rows_data.append([c.strip() for c in row_line.strip("|").split("|")])

                    # Create docx table
                    table = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
                    table.autofit = False
                    
                    # Style Header
                    for col_idx, h_text in enumerate(headers):
                        cell = table.cell(0, col_idx)
                        cell.text = h_text
                        _set_cell_background(cell, "EEF2FF")
                        p = cell.paragraphs[0]
                        p.runs[0].font.bold = True
                        p.runs[0].font.size = Pt(9.5)
                        p.runs[0].font.color.rgb = RGBColor(67, 56, 202)

                    # Style Rows
                    for row_idx, r_data in enumerate(rows_data):
                        for col_idx, val in enumerate(r_data):
                            if col_idx < len(headers):
                                cell = table.cell(row_idx + 1, col_idx)
                                cell.text = val
                                p = cell.paragraphs[0]
                                if p.runs:
                                    p.runs[0].font.size = Pt(9)
                                    p.runs[0].font.name = "Calibri"
                    continue

            # Standard body paragraphs
            paragraphs = body.split("\n\n")
            for para_text in paragraphs:
                if not para_text.strip():
                    continue
                p = doc.add_paragraph()
                p.paragraph_format.space_after = Pt(6)
                p.paragraph_format.line_spacing = 1.15
                
                # Check for bullet points
                if para_text.strip().startswith("- "):
                    p.paragraph_format.left_indent = Inches(0.25)
                    run = p.add_run(para_text.strip()[2:])
                else:
                    run = p.add_run(para_text.strip())

                run.font.name = "Calibri"
                run.font.size = Pt(10.5)
                run.font.color.rgb = RGBColor(30, 41, 59)

        # Output file path
        safe_prefix = "".join(c for c in filename_prefix if c.isalnum() or c in ("-", "_"))[:30]
        out_path = str(EXPORTS_DIR / f"{safe_prefix}.docx")
        doc.save(out_path)
        logger.info(f"Generated DOCX literature review: {out_path}")
        return out_path
