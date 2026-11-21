import docx
from docx.shared import Inches, Pt, RGBColor
import os

doc = docx.Document("Isaac_Nkansah_AI_IA_Report.docx")
print("=== REPORT VERIFICATION ===")
print("File size:", os.path.getsize("Isaac_Nkansah_AI_IA_Report.docx"), "bytes")
print("Total Sections:", len(doc.sections))
print("Total Paragraphs:", len(doc.paragraphs))
print("Total Tables:", len(doc.tables))

# Verify Figure Placeholders
fig_placeholders = []
for p in doc.paragraphs:
    if p.text.startswith("Figure ") and ":" in p.text:
        fig_placeholders.append(p.text)

print(f"\nTotal Figure Captions Found: {len(fig_placeholders)}")
for f in fig_placeholders:
    print(" -", f[:70])

# Verify Table Captions
tbl_captions = []
for p in doc.paragraphs:
    if p.text.startswith("Table ") and ":" in p.text:
        tbl_captions.append(p.text)

print(f"\nTotal Table Captions Found: {len(tbl_captions)}")
for t in tbl_captions:
    print(" -", t[:70])

# Verify headings
headings = [p.text for p in doc.paragraphs if p.style.name.startswith("Heading")]
print(f"\nTotal Headings Found: {len(headings)}")
for h in headings[:15]:
    print(" -", h)
if len(headings) > 15:
    print(f" ... and {len(headings) - 15} more headings.")

# Verify Color Check (strictly no non-black / non-grey colors)
print("\nColor Check across all runs:")
non_black_runs = 0
for p in doc.paragraphs:
    for r in p.runs:
        if r.font.color and r.font.color.rgb:
            rgb = str(r.font.color.rgb)
            # 000000 is black, grey shades are allowed
            if rgb not in ["000000", "787878", "646464"]:
                print("WARNING: Non-black/grey color found:", rgb, "in text:", r.text[:30])
                non_black_runs += 1

if non_black_runs == 0:
    print("STRICT COLOR COMPLIANCE VERIFIED: 100% black text / permitted greys only!")
else:
    print(f"FAILED: Found {non_black_runs} non-compliant runs!")
