import os
import docx
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

file_path = r"C:\Users\Salim Ansari\Downloads\AI_Agent_for_Personal_Goal_Tracking_Project_Report (1).docx"

print("Checking file:", file_path)
if not os.path.exists(file_path):
    print("FILE NOT FOUND!")
    exit(1)

doc = Document(file_path)

print(f"\n--- Document Overview ---")
print(f"Total Paragraphs: {len(doc.paragraphs)}")
print(f"Total Tables: {len(doc.tables)}")
print(f"Total Sections: {len(doc.sections)}")

for idx, section in enumerate(doc.sections):
    print(f"\nSection {idx+1} Margins:")
    print(f"  Top: {section.top_margin.inches} in, Bottom: {section.bottom_margin.inches} in")
    print(f"  Left: {section.left_margin.inches} in, Right: {section.right_margin.inches} in")
    print(f"  Page Width: {section.page_width.inches} in, Height: {section.page_height.inches} in")
    if section.header:
        header_text = "".join([p.text for p in section.header.paragraphs if p.text.strip()])
        print(f"  Header Text: {header_text}")
    if section.footer:
        footer_text = "".join([p.text for p in section.footer.paragraphs if p.text.strip()])
        print(f"  Footer Text: {footer_text}")

print(f"\n--- Styles Analysis ---")
styles_used = set()
font_names = set()
font_sizes = set()
colors_used = set()

for p in doc.paragraphs:
    if p.style:
        styles_used.add(p.style.name)
    for r in p.runs:
        if r.font.name:
            font_names.add(r.font.name)
        if r.font.size:
            font_sizes.add(r.font.size.pt)
        if r.font.color and r.font.color.rgb:
            colors_used.add(str(r.font.color.rgb))

print(f"Styles used: {styles_used}")
print(f"Font Names used: {font_names}")
print(f"Font Sizes used: {sorted(list(font_sizes))}")
print(f"Colors used (RGB Hex): {colors_used}")

print(f"\n--- First 30 Paragraphs Inspection ---")
for i, p in enumerate(doc.paragraphs[:35]):
    if p.text.strip():
        runs_info = []
        for r in p.runs:
            c = str(r.font.color.rgb) if r.font.color and r.font.color.rgb else "Default"
            runs_info.append(f"['{r.text}' | Font:{r.font.name} | Size:{r.font.size.pt if r.font.size else 'None'} | Bold:{r.bold} | Color:{c}]")
        print(f"P{i+1} [Style: {p.style.name if p.style else 'None'} | Align: {p.alignment} | SpaceAfter: {p.paragraph_format.space_after.pt if p.paragraph_format.space_after else 'None'}]:")
        print(f"   Text: {p.text[:120]}...")
        print(f"   Runs: {' '.join(runs_info[:3])}")

print(f"\n--- Tables Inspection ---")
for t_idx, t in enumerate(doc.tables[:4]):
    print(f"\nTable {t_idx+1} ({len(t.rows)} rows x {len(t.columns)} cols):")
    for r_idx, row in enumerate(t.rows[:3]):
        row_texts = [cell.text.replace('\n', ' ')[:40] for cell in row.cells]
        print(f"  Row {r_idx+1}: {' | '.join(row_texts)}")
        # inspect cell formatting
        c0 = row.cells[0]
        c0_runs = c0.paragraphs[0].runs if c0.paragraphs else []
        if c0_runs:
            r0 = c0_runs[0]
            print(f"    Cell 0 Font: {r0.font.name}, Size: {r0.font.size.pt if r0.font.size else 'None'}, Bold: {r0.bold}, Color: {r0.font.color.rgb if r0.font.color else 'None'}")
