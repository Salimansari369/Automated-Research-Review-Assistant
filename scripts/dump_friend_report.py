import os
import docx
from docx import Document

file_path = r"C:\Users\Salim Ansari\Downloads\AI_Agent_for_Personal_Goal_Tracking_Project_Report (1).docx"
doc = Document(file_path)

output_file = r"scripts/friend_report_dump.txt"

with open(output_file, "w", encoding="utf-8") as f:
    f.write("=== DOCUMENT PROPERTIES ===\n")
    for i, s in enumerate(doc.sections):
        f.write(f"Section {i+1}:\n")
        f.write(f"  Page Size: {s.page_width.inches:.2f} x {s.page_height.inches:.2f} in\n")
        f.write(f"  Margins: Top={s.top_margin.inches:.2f}, Bottom={s.bottom_margin.inches:.2f}, Left={s.left_margin.inches:.2f}, Right={s.right_margin.inches:.2f}\n")
        f.write(f"  Different First Page: {s.different_first_page_header_footer}\n")
    
    f.write("\n=== PARAGRAPHS & RUNS (FIRST 100) ===\n")
    for idx, p in enumerate(doc.paragraphs[:120]):
        if not p.text.strip():
            continue
        align = str(p.alignment)
        style = p.style.name if p.style else "None"
        line_spacing = p.paragraph_format.line_spacing
        space_before = p.paragraph_format.space_before.pt if p.paragraph_format.space_before else "None"
        space_after = p.paragraph_format.space_after.pt if p.paragraph_format.space_after else "None"
        
        f.write(f"\n[{idx+1}] Style: {style} | Align: {align} | LineSp: {line_spacing} | Before: {space_before}pt | After: {space_after}pt\n")
        f.write(f"TEXT: {p.text}\n")
        for r_i, r in enumerate(p.runs):
            font = r.font.name
            size = r.font.size.pt if r.font.size else "None"
            bold = r.bold
            italic = r.italic
            color = str(r.font.color.rgb) if r.font.color and r.font.color.rgb else "None"
            f.write(f"  Run {r_i+1}: text='{r.text}' | Font={font} | Size={size} | Bold={bold} | Italic={italic} | Color={color}\n")

    f.write("\n=== TABLES (ALL TABLES) ===\n")
    for t_i, t in enumerate(doc.tables):
        f.write(f"\n--- TABLE {t_i+1} ({len(t.rows)} rows x {len(t.columns)} cols) ---\n")
        for r_i, row in enumerate(t.rows):
            row_text = [cell.text.replace('\n', ' ') for cell in row.cells]
            f.write(f"  Row {r_i+1}: {' | '.join(row_text)}\n")
            # print styling of first cell in row
            if row.cells and row.cells[0].paragraphs and row.cells[0].paragraphs[0].runs:
                r0 = row.cells[0].paragraphs[0].runs[0]
                f.write(f"     [Style Cell 0]: Font={r0.font.name}, Size={r0.font.size.pt if r0.font.size else 'None'}, Bold={r0.bold}, Color={r0.font.color.rgb if r0.font.color else 'None'}\n")

print("Dump completed successfully!")
