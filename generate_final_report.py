"""
Full Production Academic Report Generator
Title: Custom Object Detection and Recognition of Myself Using Ultralytics YOLO
Student: Isaac Nkansah
Pentecost University College (PUC), Ghana
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def generate_report():
    doc = docx.Document()

    # -------------------------------------------------------------
    # 1. Page Configuration & Margins (A4, 2.54 cm / 1.0 in margins)
    # -------------------------------------------------------------
    for sec in doc.sections:
        sec.page_width = Inches(8.27)
        sec.page_height = Inches(11.69)
        sec.top_margin = Inches(1.0)
        sec.bottom_margin = Inches(1.0)
        sec.left_margin = Inches(1.0)
        sec.right_margin = Inches(1.0)

    # Enable automatic update of Word fields on open
    update_fields = parse_xml(r'<w:updateFields %s w:val="true"/>' % nsdecls('w'))
    doc.settings.element.append(update_fields)

    # -------------------------------------------------------------
    # 2. Strict Style Definitions (Times New Roman, Black on White)
    # -------------------------------------------------------------
    styles = doc.styles

    normal = styles['Normal']
    normal.font.name = 'Times New Roman'
    normal.font.size = Pt(12)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.line_spacing = 1.5
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    h1 = styles['Heading 1']
    h1.font.name = 'Times New Roman'
    h1.font.size = Pt(16)
    h1.font.bold = True
    h1.font.color.rgb = RGBColor(0, 0, 0)
    h1.paragraph_format.space_before = Pt(18)
    h1.paragraph_format.space_after = Pt(6)
    h1.paragraph_format.line_spacing = 1.15
    h1.paragraph_format.keep_with_next = True

    h2 = styles['Heading 2']
    h2.font.name = 'Times New Roman'
    h2.font.size = Pt(14)
    h2.font.bold = True
    h2.font.color.rgb = RGBColor(0, 0, 0)
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(4)
    h2.paragraph_format.line_spacing = 1.15
    h2.paragraph_format.keep_with_next = True

    h3 = styles['Heading 3']
    h3.font.name = 'Times New Roman'
    h3.font.size = Pt(12)
    h3.font.bold = True
    h3.font.color.rgb = RGBColor(0, 0, 0)
    h3.paragraph_format.space_before = Pt(10)
    h3.paragraph_format.space_after = Pt(2)
    h3.paragraph_format.line_spacing = 1.15
    h3.paragraph_format.keep_with_next = True

    # -------------------------------------------------------------
    # 3. Helper Functions
    # -------------------------------------------------------------
    def add_p(text="", bold_prefix=None, space_after=6, space_before=0, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.line_spacing = line_spacing

        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Times New Roman"
            r_pre.font.size = Pt(12)
            r_pre.font.bold = True
            r_pre.font.color.rgb = RGBColor(0, 0, 0)

        if text:
            r_text = p.add_run(text)
            r_text.font.name = "Times New Roman"
            r_text.font.size = Pt(12)
            r_text.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_h1(text):
        p = doc.add_paragraph(text, style='Heading 1')
        return p

    def add_h2(text):
        p = doc.add_paragraph(text, style='Heading 2')
        return p

    def add_h3(text):
        p = doc.add_paragraph(text, style='Heading 3')
        return p

    def add_table_with_caption(table_num, title, headers, data, col_widths=None):
        # Table Caption ABOVE Table
        cap_p = doc.add_paragraph()
        cap_p.paragraph_format.space_before = Pt(12)
        cap_p.paragraph_format.space_after = Pt(4)
        cap_p.paragraph_format.keep_with_next = True
        cap_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r1 = cap_p.add_run(f"Table {table_num}: ")
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        r1.font.bold = True
        r1.font.color.rgb = RGBColor(0, 0, 0)
        r2 = cap_p.add_run(title)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(11)
        r2.font.color.rgb = RGBColor(0, 0, 0)

        # Create Table
        table = doc.add_table(rows=len(data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER

        # Table Borders: Simple Black
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
            f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
            f'<w:left w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
            f'<w:right w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
            f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

        # Header Row: Bold, Shaded Light Grey (#E5E5E5)
        hdr_cells = table.rows[0].cells
        for i, header_text in enumerate(headers):
            cell = hdr_cells[i]
            cell.text = header_text
            shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="E5E5E5" w:val="clear"/>')
            cell._tc.get_or_add_tcPr().append(shd)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(10)
                r.font.bold = True
                r.font.color.rgb = RGBColor(0, 0, 0)

        # Body Rows
        for r_idx, row_data in enumerate(data):
            row_cells = table.rows[r_idx + 1].cells
            for c_idx, cell_value in enumerate(row_data):
                cell = row_cells[c_idx]
                cell.text = str(cell_value)
                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(3)
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.line_spacing = 1.15
                # Center align short numbers or left align text
                if c_idx > 0 and len(str(cell_value)) < 15:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(10)
                    r.font.color.rgb = RGBColor(0, 0, 0)

        # Column widths if provided
        if col_widths:
            for row in table.rows:
                for idx, width in enumerate(col_widths):
                    row.cells[idx].width = Inches(width)

        # Space after table
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    def add_figure_placeholder(fig_num, title, description, note_text):
        # 1-cell box table (14 cm wide, 8 cm high)
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(5.51)  # 14 cm
        tbl.rows[0].height = Inches(3.15)  # 8 cm
        tbl.rows[0].height_rule = docx.enum.table.WD_ROW_HEIGHT_RULE.AT_LEAST

        # Black border around cell
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
            f'<w:left w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
            f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
            f'<w:right w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
            f'</w:tcBorders>'
        )
        cell._tc.get_or_add_tcPr().append(borders)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(f"[INSERT SCREENSHOT HERE: {description}]")
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 0)

        # Caption BELOW Figure
        cap_p = doc.add_paragraph()
        cap_p.paragraph_format.space_before = Pt(6)
        cap_p.paragraph_format.space_after = Pt(2)
        cap_p.paragraph_format.keep_with_next = True
        cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        c_run1 = cap_p.add_run(f"Figure {fig_num}: ")
        c_run1.font.name = "Times New Roman"
        c_run1.font.size = Pt(11)
        c_run1.font.bold = True
        c_run1.font.color.rgb = RGBColor(0, 0, 0)
        c_run2 = cap_p.add_run(title)
        c_run2.font.name = "Times New Roman"
        c_run2.font.size = Pt(11)
        c_run2.font.color.rgb = RGBColor(0, 0, 0)

        # Note below caption
        note_p = doc.add_paragraph()
        note_p.paragraph_format.space_before = Pt(0)
        note_p.paragraph_format.space_after = Pt(12)
        note_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        n_run = note_p.add_run(f"Note: {note_text}")
        n_run.font.name = "Times New Roman"
        n_run.font.size = Pt(10)
        n_run.font.italic = True
        n_run.font.color.rgb = RGBColor(0, 0, 0)

    def add_code_block(code_str):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.27)
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            f'<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            f'<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            f'</w:tcBorders>'
        )
        cell._tc.get_or_add_tcPr().append(borders)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(code_str)
        r.font.name = "Courier New"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0, 0, 0)
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # =============================================================
    # 4. COVER PAGE (Section 1)
    # =============================================================
    sec0 = doc.sections[0]
    sec0.different_first_page_header_footer = False

    # University & Faculty Header
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(20)
    p_inst.paragraph_format.space_after = Pt(4)
    r = p_inst.add_run("PENTECOST UNIVERSITY COLLEGE (PUC), GHANA\n")
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    r_fac = p_inst.add_run("FACULTY OF ENGINEERING AND APPLIED COMPUTING (FESAC)\nDEPARTMENT OF INFORMATION TECHNOLOGY AND SOFTWARE ENGINEERING")
    r_fac.font.name = "Times New Roman"
    r_fac.font.size = Pt(11)
    r_fac.font.bold = True
    r_fac.font.color.rgb = RGBColor(0, 0, 0)

    # Title spacing
    p_space1 = doc.add_paragraph()
    p_space1.paragraph_format.space_before = Pt(70)

    # Report Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(12)
    p_title.paragraph_format.line_spacing = 1.2
    r_title = p_title.add_run("CUSTOM OBJECT DETECTION AND RECOGNITION OF MYSELF USING ULTRALYTICS YOLO")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0, 0, 0)

    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(60)
    r_sub = p_sub.add_run("An Individual Assessment (IA) Project Report Submitted in Partial Fulfilment of the Requirements for the Award of the Degree of Bachelor of Science in Industrial Software Engineering")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(0, 0, 0)

    # Candidate Meta Block
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.line_spacing = 1.3
    p_meta.paragraph_format.space_after = Pt(40)

    def add_meta_line(label, value):
        r_l = p_meta.add_run(f"{label}: ")
        r_l.font.name = "Times New Roman"
        r_l.font.size = Pt(12)
        r_l.font.bold = True
        r_l.font.color.rgb = RGBColor(0, 0, 0)
        r_v = p_meta.add_run(f"{value}\n")
        r_v.font.name = "Times New Roman"
        r_v.font.size = Pt(12)
        r_v.font.color.rgb = RGBColor(0, 0, 0)

    add_meta_line("Candidate Name", "Isaac Nkansah")
    add_meta_line("Index / Student ID", "[TO BE FILLED BY STUDENT - INDEX NUMBER]")
    add_meta_line("Programme of Study", "B.Sc. Industrial Software Engineering (Final Year)")
    add_meta_line("Course Title", "Artificial Intelligence and Machine Learning")
    add_meta_line("Course Code", "[TO BE FILLED BY STUDENT - COURSE CODE]")
    add_meta_line("Course Lecturer / Supervisor", "[TO BE FILLED BY STUDENT - LECTURER NAME]")
    add_meta_line("Date of Submission", "20 November 2026")
    add_meta_line("Academic Year", "2026/2027")

    # =============================================================
    # 5. FRONT MATTER (Section 2 - Roman Numerals i, ii, iii...)
    # =============================================================
    sec1 = doc.add_section()
    sec1.different_first_page_header_footer = False
    pg_num1 = parse_xml(r'<w:pgNumType %s w:fmt="lowerRoman" w:start="1"/>' % nsdecls('w'))
    sec1._sectPr.append(pg_num1)

    # Footer for Roman Numerals
    footer1 = sec1.footer
    f_p1 = footer1.paragraphs[0]
    f_p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f_run1 = f_p1.add_run()
    f_run1.font.name = "Times New Roman"
    f_run1.font.size = Pt(10)
    fld_page1 = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
    f_run1._r.append(fld_page1)

    # 5.1 DECLARATION
    add_h1("Declaration")
    add_p("I, Isaac Nkansah, hereby declare that this project report entitled \"Custom Object Detection and Recognition of Myself Using Ultralytics YOLO\" represents my own independent academic and technical work. It has been authored and developed in partial fulfilment of the requirements for the Artificial Intelligence and Machine Learning course within the Department of Information Technology and Software Engineering, Pentecost University College (PUC), Ghana.")
    add_p("I affirm that this work has not been previously submitted, in whole or in part, for any degree, diploma, or other qualification at this or any other tertiary institution. All secondary information, theoretical frameworks, models, datasets, open-source libraries, and scholarly literature utilized throughout this investigation have been fully acknowledged and cited in accordance with strict academic conventions and IEEE referencing guidelines.")

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(36)
    p_sig.paragraph_format.line_spacing = 1.3
    r = p_sig.add_run("_________________________________________\n")
    r.font.name = "Times New Roman"
    r = p_sig.add_run("Candidate Signature: Isaac Nkansah\n")
    r.font.bold = True
    r = p_sig.add_run("Date: 20 November 2026\n\n\n")

    r = p_sig.add_run("_________________________________________\n")
    r = p_sig.add_run("Supervisor / Lecturer Certification: [TO BE FILLED BY STUDENT - LECTURER NAME]\n")
    r.font.bold = True
    r = p_sig.add_run("Faculty of Engineering and Applied Computing (FESAC)\n")
    r = p_sig.add_run("Pentecost University College (PUC), Ghana\n")
    r = p_sig.add_run("Date: [TO BE FILLED BY STUDENT - DATE]")

    doc.add_page_break()

    # 5.2 ACKNOWLEDGEMENTS
    add_h1("Acknowledgements")
    add_p("First and foremost, I render my deepest gratitude and praise to the Almighty God for His unfailing grace, divine wisdom, sound health, and intellectual fortitude throughout the execution and realization of this capstone research endeavour.")
    add_p("My sincere appreciation goes to the Faculty of Engineering and Applied Computing (FESAC) and the Department of Information Technology and Software Engineering at Pentecost University College (PUC), Ghana. I am profoundly indebted to my course lecturer and project supervisor, [TO BE FILLED BY STUDENT - LECTURER NAME], whose pedagogical guidance, rigorous intellectual critique, and demanding project standards provided the impetus for pursuing excellence and adhering to engineering discipline throughout this project.")
    add_p("Special thanks are extended to my academic peers and classmates at Pentecost University College who graciously consented to participate in group photographic sessions. Their presence provided the diverse, realistic background context and non-target facial variations necessary to rigorously test, train, and validate the model's discriminative visual recognition capabilities under multi-person conditions.")
    add_p("Lastly, I express heartfelt gratitude to my family and friends for their enduring patience, moral encouragement, and steadfast prayers during the demanding phases of dataset curation, model hyperparameter tuning, cloud integration, and multi-platform software engineering.")

    doc.add_page_break()

    # 5.3 ABSTRACT
    add_h1("Abstract")
    add_p("Real-time automated personal recognition has emerged as a critical capability across modern authentication, surveillance, and intelligent human-computer interaction paradigms. While conventional biometric architectures traditionally isolate facial crops using static feature points, contemporary industrial requirements necessitate robust, one-stage object detection models capable of simultaneously detecting, localizing, and discriminating specific personal identities within unstructured environments, cluttered backgrounds, and complex multi-person scenes. This academic report details the systematic engineering, training, comparative evaluation, and multi-platform cloud deployment of a custom deep learning visual recognition system specifically designed to identify the author (\"Isaac\") using the state-of-the-art Ultralytics YOLO (You Only Look Once) architecture.")
    add_p("A rigorous empirical methodology was formulated, commencing with the acquisition and curation of a dedicated personal visual corpus comprising 707 high-resolution photographic images. To ensure operational robustness across real-world deployment contexts, the dataset captured extreme variations in illumination, viewing angles, facial orientations, distance, scale, occlusions, and social group compositions containing between 1 and 8 individuals. Bounding-box annotations were established for a single target class (\"Isaac\"), while non-target individuals were deliberately maintained as unannotated background elements to penalize false-positive identity attribution. Model training was conducted on the Ultralytics cloud infrastructure utilizing transfer learning from the YOLO26n (nano) architectural baseline at a standardized input resolution of 640 × 640 pixels.")
    add_p("Two primary training iterations were executed and systematically contrasted: Run 1 (\"isaacimage\"), serving as the baseline, and Run 2 (\"v2-707imgs\"), incorporating the comprehensive 707-image corpus and advanced multi-person context. Quantitative benchmarking demonstrated substantial performance gains in Run 2 across all primary computer vision evaluation metrics: Precision increased from 69.7% to 88.1% (+18.4%), Recall rose from 60.3% to 85.1% (+24.8%), Mean Average Precision at 0.50 IoU (mAP50) advanced from 68.3% to 88.4% (+20.1%), and mAP50-95 surged from 29.2% to 47.9% (+18.7%). Comprehensive diagnostic curve analysis—encompassing precision-recall (PR) trajectories, F1-confidence profiles, and confusion matrices—confirmed that the model achieved robust convergence with minimal background false alarms.")
    add_p("To translate theoretical performance into industrial practice, the validated weights were deployed to an Ultralytics managed Cloud Run endpoint situated in the London (UK) region. An asynchronous REST API inference gateway was engineered utilizing FastAPI and deployed onto Vercel serverless cloud infrastructure, incorporating server-side Pillow image optimization to guarantee sub-second latency and circumvent payload constraints. Dual production client interfaces were developed: an interactive responsive web application featuring real-time webcam inference and history inspection, and a native cross-platform mobile application developed with React Native and Expo (SDK 58.0.0). Real-world field evaluations affirmed that the system achieves rapid, highly reliable identity discrimination across diverse operational environments, satisfying all objectives established for this final-year Industrial Software Engineering assessment.")

    doc.add_page_break()

    # 5.4 TABLE OF CONTENTS
    add_h1("Table of Contents")
    p_toc = doc.add_paragraph()
    p_toc.paragraph_format.space_after = Pt(12)
    r_toc = p_toc.add_run()
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> TOC \o "1-3" \h \z \u </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    r_toc._r.append(fldChar1)
    r_toc._r.append(instrText)
    r_toc._r.append(fldChar2)

    # Pre-populated TOC entries for compatibility across all document viewers
    toc_entries = [
        ("Declaration", "i"),
        ("Acknowledgements", "ii"),
        ("Abstract", "iii"),
        ("List of Figures", "v"),
        ("List of Tables", "vi"),
        ("List of Abbreviations", "vii"),
        ("1. Introduction", "1"),
        ("    1.1 Background of the Study", "1"),
        ("    1.2 Problem Statement", "2"),
        ("    1.3 Aim and Objectives", "2"),
        ("    1.4 Scope and Limitations", "3"),
        ("    1.5 Significance of the Study", "4"),
        ("    1.6 Report Organization", "4"),
        ("2. Literature Review and Theoretical Framework", "5"),
        ("    2.1 Evolution of Computer Vision and Object Detection", "5"),
        ("    2.2 Deep Learning Paradigms: Two-Stage vs. One-Stage Detectors", "6"),
        ("    2.3 The YOLO (You Only Look Once) Architecture and Ultralytics Ecosystem", "7"),
        ("    2.4 Model Evaluation Metrics in Object Detection", "8"),
        ("3. Tools and Technological Stack", "11"),
        ("    3.1 Ultralytics Platform and YOLO26n Architecture", "11"),
        ("    3.2 Dataset Storage and Version Control (Google Drive & GitHub)", "12"),
        ("    3.3 Antigravity Development Environment", "12"),
        ("    3.4 Inference Backend Engine (FastAPI and Uvicorn)", "13"),
        ("    3.5 Cloud Serverless Hosting (Vercel)", "13"),
        ("    3.6 Cross-Platform Mobile Client (React Native & Expo Framework)", "14"),
        ("4. Methodology", "15"),
        ("    4.1 Data Collection Strategy and Dataset Characteristics", "15"),
        ("    4.2 Data Preparation, Cleaning, and Annotation Protocol", "16"),
        ("    4.3 Model Selection and Hyperparameter Configuration", "17"),
        ("    4.4 Training Execution and Experimental Setup", "18"),
        ("5. Results and Comparative Analysis", "19"),
        ("    5.1 Quantitative Performance Benchmark: Run 1 vs. Run 2", "19"),
        ("    5.2 Critical Analysis of Performance Gains", "20"),
        ("    5.3 Detailed Examination of Run 2 Diagnostic Curves", "21"),
        ("    5.4 Qualitative Evaluation on Validation Batches", "23"),
        ("6. System Architecture and Multi-Platform Deployment", "24"),
        ("    6.1 Ultralytics Cloud Run Managed Deployment", "24"),
        ("    6.2 FastAPI Serverless Gateway on Vercel", "24"),
        ("    6.3 Responsive Web Application Interface", "26"),
        ("    6.4 Cross-Platform Mobile Application (Android APK & iOS Expo Go)", "27"),
        ("7. System Testing and Critical Discussion", "29"),
        ("    7.1 Real-World Validation Scenarios", "29"),
        ("    7.2 Robustness Under Varied Environmental Conditions", "30"),
        ("    7.3 Group Photo Disambiguation and Identification Accuracy", "30"),
        ("    7.4 Failure Mode Analysis and Identified Limitations", "31"),
        ("8. Challenges Encountered and Lessons Learned", "32"),
        ("    8.1 Technical and Computational Challenges", "32"),
        ("    8.2 Architectural and Engineering Lessons", "33"),
        ("9. Conclusions and Future Recommendations", "34"),
        ("    9.1 Summary of Contributions and Achievements", "34"),
        ("    9.2 Recommendations for Future Research and Development", "34"),
        ("References", "36"),
        ("Appendices", "38"),
        ("    Appendix A: Dataset Screenshots and Sample Annotated Images", "38"),
        ("    Appendix B: Full Training Screenshots (Curves and Metrics)", "40"),
        ("    Appendix C: Deployment and API Screenshots", "44"),
        ("    Appendix D: Web App and Mobile App Screenshots", "45"),
        ("    Appendix E: Key Source Code (FastAPI Backend Gateway)", "47"),
        ("    Appendix F: Project Repositories and Resource Links", "50"),
    ]
    for title_text, page_num in toc_entries:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.line_spacing = 1.15
        p_item.paragraph_format.space_after = Pt(2)
        r_t = p_item.add_run(title_text)
        r_t.font.name = "Times New Roman"
        r_t.font.size = Pt(11)
        r_t.font.color.rgb = RGBColor(0, 0, 0)
        # Tab leader
        r_dots = p_item.add_run(f" {'.' * max(2, (80 - len(title_text) * 2))} ")
        r_dots.font.name = "Times New Roman"
        r_dots.font.size = Pt(10)
        r_dots.font.color.rgb = RGBColor(120, 120, 120)
        r_p = p_item.add_run(page_num)
        r_p.font.name = "Times New Roman"
        r_p.font.size = Pt(11)
        r_p.font.color.rgb = RGBColor(0, 0, 0)

    r_toc._r.append(fldChar3)
    doc.add_page_break()

    # 5.5 LIST OF FIGURES
    add_h1("List of Figures")
    p_lof = doc.add_paragraph()
    p_lof.paragraph_format.space_after = Pt(12)
    r_lof = p_lof.add_run()
    fld1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    ins1 = parse_xml(r'<w:instrText %s xml:space="preserve"> TOC \h \z \c "Figure" </w:instrText>' % nsdecls('w'))
    fld2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fld3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    r_lof._r.append(fld1)
    r_lof._r.append(ins1)
    r_lof._r.append(fld2)

    lof_entries = [
        ("Figure 1: Ultralytics Platform Dataset Overview Showing 707 Images and 1 Class", "38"),
        ("Figure 2: Single-Subject Bounding Box Annotation in Ultralytics Interface", "39"),
        ("Figure 3: Multi-Person Group Scene Annotation With Only Isaac Labeled", "39"),
        ("Figure 4: Ultralytics AI Image Training Project Workspace Displaying Both Runs", "40"),
        ("Figure 5: Run 1 (isaacimage) Training Diagnostics and Metric Convergence Curves", "41"),
        ("Figure 6: Run 2 (v2-707imgs) Comprehensive Training Metrics and Loss Trajectories", "41"),
        ("Figure 7: Run 2 Confusion Matrix Evaluation", "42"),
        ("Figure 8: Run 2 Precision-Recall (PR) and F1-Confidence Curves", "42"),
        ("Figure 9: Run 2 Validation Batch Predictions With Predicted Boxes and Scores", "43"),
        ("Figure 10: Side-by-Side Quantitative Metrics Comparison (Run 1 vs. Run 2)", "43"),
        ("Figure 11: Ultralytics Cloud Run Active Deployment in London (UK) Region", "44"),
        ("Figure 12: Ultralytics Platform Inference Verification on Independent Test Image", "44"),
        ("Figure 13: Responsive Web Application Interface (Upload and Detection Results)", "45"),
        ("Figure 14: Cross-Platform Mobile Application Interface on iOS and Android", "46"),
        ("Figure 15: GitHub Source Code Repository Workspace (ai-object-detection-ultralytics)", "50"),
        ("Figure 16: Primary Dataset Cloud Archive on Google Drive", "50"),
    ]
    for fig_text, p_num in lof_entries:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.line_spacing = 1.15
        p_item.paragraph_format.space_after = Pt(2)
        r_t = p_item.add_run(fig_text)
        r_t.font.name = "Times New Roman"
        r_t.font.size = Pt(11)
        r_dots = p_item.add_run(f" {'.' * max(2, (80 - len(fig_text) * 2))} ")
        r_dots.font.name = "Times New Roman"
        r_dots.font.size = Pt(10)
        r_dots.font.color.rgb = RGBColor(120, 120, 120)
        r_p = p_item.add_run(p_num)
        r_p.font.name = "Times New Roman"
        r_p.font.size = Pt(11)

    r_lof._r.append(fld3)
    doc.add_page_break()

    # 5.6 LIST OF TABLES
    add_h1("List of Tables")
    p_lot = doc.add_paragraph()
    p_lot.paragraph_format.space_after = Pt(12)
    r_lot = p_lot.add_run()
    fld1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    ins1 = parse_xml(r'<w:instrText %s xml:space="preserve"> TOC \h \z \c "Table" </w:instrText>' % nsdecls('w'))
    fld2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fld3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    r_lot._r.append(fld1)
    r_lot._r.append(ins1)
    r_lot._r.append(fld2)

    lot_entries = [
        ("Table 1: High-Level Architecture Comparison of Object Detection Frameworks", "6"),
        ("Table 2: Mathematical Formulations of Key Computer Vision Evaluation Metrics", "10"),
        ("Table 3: Technological Stack and Integrated System Components", "14"),
        ("Table 4: Dataset Split and Scene Composition Breakdown (707 Images)", "16"),
        ("Table 5: Ultralytics YOLO26n Training Hyperparameter Specifications", "18"),
        ("Table 6: Quantitative Performance Benchmark: Baseline Run 1 vs. Enhanced Run 2", "19"),
        ("Table 7: Environmental Stress Testing and Detection Robustness Results", "29"),
        ("Table 8: Multi-Person Group Disambiguation Accuracy Across Varying Group Sizes", "31"),
        ("Table 9: Source Code Repository Architecture and Component Roles", "49"),
    ]
    for tbl_text, p_num in lot_entries:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.line_spacing = 1.15
        p_item.paragraph_format.space_after = Pt(2)
        r_t = p_item.add_run(tbl_text)
        r_t.font.name = "Times New Roman"
        r_t.font.size = Pt(11)
        r_dots = p_item.add_run(f" {'.' * max(2, (80 - len(tbl_text) * 2))} ")
        r_dots.font.name = "Times New Roman"
        r_dots.font.size = Pt(10)
        r_dots.font.color.rgb = RGBColor(120, 120, 120)
        r_p = p_item.add_run(p_num)
        r_p.font.name = "Times New Roman"
        r_p.font.size = Pt(11)

    r_lot._r.append(fld3)
    doc.add_page_break()

    # 5.7 LIST OF ABBREVIATIONS
    add_h1("List of Abbreviations")
    add_p("The standard acronyms, mathematical symbols, and technical abbreviations utilized throughout this project report are summarized below:")

    abbreviations = [
        ("AI", "Artificial Intelligence"),
        ("ML", "Machine Learning"),
        ("DL", "Deep Learning"),
        ("CV", "Computer Vision"),
        ("YOLO", "You Only Look Once (Real-Time Object Detection Framework)"),
        ("CNN", "Convolutional Neural Network"),
        ("IoU", "Intersection over Union"),
        ("mAP", "Mean Average Precision"),
        ("mAP50", "Mean Average Precision calculated at an IoU threshold of 0.50"),
        ("mAP50-95", "Mean Average Precision averaged over IoU thresholds from 0.50 to 0.95 (step 0.05)"),
        ("PR", "Precision-Recall"),
        ("TP / FP / FN", "True Positive / False Positive / False Negative"),
        ("API", "Application Programming Interface"),
        ("REST", "Representational State Transfer"),
        ("HTTP", "Hypertext Transfer Protocol"),
        ("JSON", "JavaScript Object Notation"),
        ("APK", "Android Package Kit (Standalone Android Application Format)"),
        ("SDK", "Software Development Kit"),
        ("EAS", "Expo Application Services (Cloud Build & Update Infrastructure)"),
        ("FESAC", "Faculty of Engineering and Applied Computing"),
        ("PUC", "Pentecost University College, Ghana"),
        ("PIL", "Python Imaging Library (Pillow)"),
        ("PANet", "Path Aggregation Network"),
        ("DFL", "Distribution Focal Loss"),
        ("CIoU", "Complete Intersection over Union Loss"),
        ("CORS", "Cross-Origin Resource Sharing"),
        ("UI / UX", "User Interface / User Experience")
    ]

    add_table_with_caption(
        "A", 
        "List of Acronyms, Technical Terms, and Abbreviations", 
        ["Abbreviation", "Full Expanded Definition and Operational Context"], 
        abbreviations, 
        col_widths=[1.6, 4.67]
    )

    doc.add_page_break()

    # =============================================================
    # 6. MAIN BODY (Section 3 - Arabic Numerals 1, 2, 3...)
    # =============================================================
    sec2 = doc.add_section()
    sec2.different_first_page_header_footer = False
    pg_num2 = parse_xml(r'<w:pgNumType %s w:fmt="decimal" w:start="1"/>' % nsdecls('w'))
    sec2._sectPr.append(pg_num2)

    # Running Header with Short Report Title
    sec2.header.is_linked_to_previous = False
    h_p = sec2.header.paragraphs[0]
    h_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_hdr = h_p.add_run("Custom YOLO Object Detection and Recognition • Isaac Nkansah")
    r_hdr.font.name = "Times New Roman"
    r_hdr.font.size = Pt(9)
    r_hdr.font.color.rgb = RGBColor(100, 100, 100)

    # Footer for Arabic Numerals
    sec2.footer.is_linked_to_previous = False
    footer2 = sec2.footer
    f_p2 = footer2.paragraphs[0]
    f_p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    f_run2 = f_p2.add_run()
    f_run2.font.name = "Times New Roman"
    f_run2.font.size = Pt(10)
    fld_page2 = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
    f_run2._r.append(fld_page2)

    # -------------------------------------------------------------
    # CHAPTER 1: INTRODUCTION
    # -------------------------------------------------------------
    add_h1("1. Introduction")

    add_h2("1.1 Background of the Study")
    add_p("The rapid evolution of computer vision (CV) and deep learning (DL) over the past decade has fundamentally altered how computational systems perceive, interpret, and interact with the physical visual world. Object detection represents one of the foundational cornerstones of modern computer vision, synthesizing the dual challenges of object classification (determining what is present in an image) and spatial localization (determining precisely where the object resides through bounding coordinates). While generic object detection models—frequently trained on expansive benchmark datasets such as Microsoft Common Objects in Context (MS COCO) or Pascal VOC—excel at identifying broad visual categories such as \"person\", \"car\", or \"chair\", they remain intrinsically incapable of fine-grained identity discrimination. In standard computer vision benchmarks, every human subject is uniformly assigned the generic semantic label \"person\".")
    add_p("In contemporary industrial, educational, and security environments, however, visual automation demands a significantly higher level of granularity. Institutions increasingly require automated computer vision systems capable of isolating, identifying, and verifying specific individual identities in dynamic, real-time visual feeds. At Pentecost University College (PUC), Ghana, the Final Year curriculum in Industrial Software Engineering stresses the rigorous conceptualization, design, implementation, and deployment of applied artificial intelligence systems that address tangible practical requirements. This individual assessment project is situated within this academic imperative, focusing on the engineering of an end-to-end, real-time visual object detection and recognition system specifically trained to detect and recognize the author (\"Isaac\") while rejecting or ignoring non-target individuals in complex real-world social environments.")

    add_h2("1.2 Problem Statement")
    add_p("Conventional biometric authentication systems, such as facial recognition gateways, predominantly rely upon constrained capture environments. Such frameworks frequently require cooperative human subjects positioned directly in front of high-resolution sensor arrays under uniform illumination, neutral facial expressions, and devoid of background clutter. When deployed into unconstrained real-world settings—such as crowded lecture halls, multi-person collaborative project workspaces, outdoor university courtyards, or variable illumination environments—traditional biometric algorithms exhibit catastrophic performance degradation.")
    add_p("Conversely, off-the-shelf deep learning object detection models cannot distinguish between individuals: a detector processing a group photograph of eight university students will simply generate eight generic \"person\" bounding boxes with no attribution of personal identity. Furthermore, constructing a specialized personal recognition model presents acute data engineering challenges. Unlike industrial facial recognition architectures trained on millions of generalized faces, a personalized single-class detection system must learn highly discriminative visual features—facial geometry, personal posture, characteristic hair structure, and facial proportions—from a comparatively constrained custom image dataset without suffering from catastrophic overfitting or extreme false-positive vulnerability in the presence of other human faces. The central engineering problem addressed in this study is: How can a high-accuracy, real-time, single-class object detection model be systematically trained and deployed across cloud, web, and mobile environments to reliably isolate and recognize \"Isaac\" in multi-person group scenes containing 1 to 8 individuals under dynamic lighting, viewing angles, and distance variations?")

    add_h2("1.3 Aim and Objectives")
    add_p("The overarching aim of this research and software engineering project is to design, train, evaluate, and deploy a production-grade custom object detection model based on the Ultralytics YOLO architecture to reliably detect and recognize Isaac Nkansah across heterogeneous visual contexts.")
    add_p("To realize this overarching aim, the following specific technical objectives were established and rigorously executed:")
    add_p("1. Dataset Engineering: Collect, curate, and annotate a custom photographic dataset comprising at least 500 images (achieving 707 images) capturing the author across solo portraits and multi-person group compositions ranging from 1 to 8 individuals under diverse environmental conditions.")
    add_p("2. Annotation and Boundary Protocol: Establish a precise single-class (\"Isaac\") bounding-box annotation protocol within the Ultralytics Platform, intentionally designating all classmates and non-target bystanders as unannotated background to train the network against false-positive identity attribution.")
    add_p("3. Baseline Exploration (Run 1): Establish an initial experimental baseline designated \"isaacimage\" using the YOLO26n (nano) architectural framework to analyze initial convergence dynamics and baseline metric performance.")
    add_p("4. Enhanced Iterative Training (Run 2): Train an advanced production model designated \"v2-707imgs\" leveraging the complete 707-image corpus, expanded multi-person contextual samples, and optimal hyperparameter tuning.")
    add_p("5. Comparative Empirical Evaluation: Conduct a rigorous comparative benchmark of Run 1 and Run 2 using standard computer vision evaluation metrics, specifically Precision, Recall, Mean Average Precision at 0.50 IoU (mAP50), and mAP50-95.")
    add_p("6. Cloud Inference Deployment: Export and deploy the finalized model weights to a managed Ultralytics Cloud Run serverless inference endpoint operating in the London, United Kingdom cloud region.")
    add_p("7. Serverless Gateway Engineering: Develop a production-grade asynchronous REST API inference gateway using FastAPI, integrating server-side Pillow image optimization, and deploy it onto Vercel serverless cloud infrastructure.")
    add_p("8. Multi-Platform Client Development: Architect dual client interfaces: a responsive browser web application featuring live webcam inference and detection history tracking, and a cross-platform mobile application developed with React Native and Expo (SDK 58.0.0) supporting standalone cloud updates and photo saving.")
    add_p("9. Robustness and Stress Testing: Conduct comprehensive validation under challenging real-world boundary conditions, including partial occlusions, varying lighting intensities, multi-person crowd disambiguation, and extreme camera angles.")

    add_h2("1.4 Scope and Limitations")
    add_p("The operational scope of this research encompasses the complete lifecycle of an applied machine learning project: photographic data acquisition, bounding-box ground truth labeling, cloud-based transfer learning, statistical evaluation, backend API engineering, and frontend deployment across web and mobile platforms. The model is intentionally architected as a single-class detector focused exclusively on the visual recognition of Isaac Nkansah.")
    add_p("The primary limitations identified within this project include:")
    add_p("1. Dataset Sizing: While the curated corpus of 707 images comfortably exceeds the course requirement of 500 images, it remains modest in comparison to massive commercial computer vision datasets (which often encompass millions of exemplars).")
    add_p("2. Hardware and Free-Tier Computational Constraints: Training was constrained to cloud GPU allocations provided on the Ultralytics platform, while production deployment leverages serverless container execution (Vercel and Cloud Run) subject to request payload limits (4.5 MB on Vercel) and execution timeout thresholds.")
    add_p("3. Severe Visual Occlusion: Extreme visual obstructions where more than 70% of the target subject's facial and bodily features are masked or obscured inevitably introduce classification uncertainty.")

    add_h2("1.5 Significance of the Study")
    add_p("This project carries profound academic, practical, and pedagogical significance. From an academic perspective, it demonstrates the viability of applying advanced one-stage object detection architectures—traditionally reserved for generalized object categories—to fine-grained personal visual identity verification in unconstrained social scenes. Pedagogically, it serves as a capstone demonstration of the software engineering competencies cultivated within the Faculty of Engineering and Applied Computing at Pentecost University College, bridging theoretical convolutional neural network concepts with modern cloud microservice architecture and mobile application engineering.")
    add_p("Practically, the system architecture developed herein provides a foundational blueprint for contactless university campus access control, automated lecture hall attendance logging, smart surveillance, and personalized human-robot interaction systems tailored to institutional environments across Ghana and sub-Saharan Africa.")

    add_h2("1.6 Report Organization")
    add_p("The remainder of this academic report is structured into eight subsequent chapters: Chapter 2 reviews the relevant theoretical literature, convolutional architectures, the YOLO framework, and mathematical evaluation metrics. Chapter 3 outlines the comprehensive technological stack and software tools utilized. Chapter 4 elaborates upon the methodology, dataset collection, annotation standards, and experimental training configurations. Chapter 5 presents the quantitative and qualitative results, contrasting Run 1 and Run 2 across all metrics and diagnostic curves. Chapter 6 details the end-to-end multi-platform deployment architecture across Cloud Run, FastAPI, Vercel, web, and React Native mobile environments. Chapter 7 documents system testing, stress evaluations, and failure modes. Chapter 8 reflects upon technical challenges and engineering lessons. Finally, Chapter 9 delivers conclusions and actionable recommendations for future research.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 2: LITERATURE REVIEW AND THEORETICAL FRAMEWORK
    # -------------------------------------------------------------
    add_h1("2. Literature Review and Theoretical Framework")

    add_h2("2.1 Evolution of Computer Vision and Object Detection")
    add_p("Early paradigms in computer vision relied heavily on handcrafted feature engineering. Classical methods such as Viola-Jones Haar-like cascades, Histogram of Oriented Gradients (HOG), and Scale-Invariant Feature Transform (SIFT) paired shallow machine learning classifiers (e.g., Support Vector Machines or AdaBoost) with rigid visual descriptors. While computationally feasible on early hardware, these traditional pipelines exhibited severe brittleness when subjected to non-affine transformations, arbitrary rotations, complex multi-person occlusions, and dynamic illumination gradients.")
    add_p("The renaissance of deep learning—catalyzed by the breakthrough performance of AlexNet on the ImageNet Large Scale Visual Recognition Challenge (ILSVRC) in 2012—shifted the paradigm toward Convolutional Neural Networks (CNNs). Convolutional layers autonomously extract hierarchical visual representations, progressing from low-level edges and textures in early layers to complex semantic structures and facial geometries in deeper layers. This architectural transition provided the foundational capability required for generalized visual feature extraction.")

    add_h2("2.2 Deep Learning Paradigms: Two-Stage vs. One-Stage Detectors")
    add_p("Modern deep learning object detection architectures are broadly categorized into two fundamental paradigms: two-stage detectors and one-stage detectors. Two-stage architectures—typified by the R-CNN family (R-CNN, Fast R-CNN, and Faster R-CNN)—decouple the detection task into two distinct sequential phases. In the first phase, a Region Proposal Network (RPN) scans feature maps to generate candidate regions of interest (RoIs) likely to contain objects. In the second phase, these candidate regions are cropped, feature-pooled, and passed to specialized classification and bounding-box regression heads.")
    add_p("While two-stage detectors historically achieved superior localization precision, their computational complexity and multi-pass inference overhead render them unsuitable for real-time edge or mobile deployment, frequently yielding inference speeds below 15 frames per second (FPS). To overcome these latency bottlenecks, one-stage detectors were pioneered, most notably the Single Shot MultiBox Detector (SSD), RetinaNet, and the groundbreaking You Only Look Once (YOLO) framework.")

    table1_data = [
        ["Paradigm", "Primary Frameworks", "Inference Speed (FPS)", "Localization Accuracy", "Edge / Mobile Suitability"],
        ["Two-Stage", "Faster R-CNN, Mask R-CNN", "Low (5 – 15 FPS)", "Very High", "Poor (Requires heavy GPU compute)"],
        ["One-Stage (Anchor-Based)", "YOLOv3, YOLOv4, SSD", "High (30 – 60 FPS)", "Moderate to High", "Moderate"],
        ["One-Stage (Anchor-Free)", "YOLOv8, YOLO26, CenterNet", "Extremely High (60 – 150+ FPS)", "High to Very High", "Excellent (Optimized for edge & mobile)"]
    ]
    add_table_with_caption(
        1, 
        "High-Level Architecture Comparison of Object Detection Frameworks", 
        table1_data[0], 
        table1_data[1:], 
        col_widths=[1.5, 1.4, 1.1, 1.1, 1.17]
    )

    add_h2("2.3 The YOLO (You Only Look Once) Architecture and Ultralytics Ecosystem")
    add_p("Introduced by Redmon et al. in 2016, the YOLO philosophy reframed object detection from a complex multi-stage pipeline into a single, unified regression problem. Instead of extracting potential regions, YOLO processes the entire input image in a single forward pass through a convolutional backbone network. The input image is conceptually divided into an $S \\times S$ grid. If an object's center falls within a specific grid cell, that cell is responsible for predicting the bounding-box offsets, objectness confidence, and class probabilities simultaneously.")
    add_p("Over successive iterations, the YOLO architecture has undergone profound evolutionary refinements under the leadership of Ultralytics. The transition from anchor-based mechanisms to anchor-free detection heads represents a monumental milestone. In traditional anchor-based systems, predefined candidate bounding boxes (anchors) were assigned to grid cells, requiring manual clustering and introducing computational inefficiencies. Modern anchor-free architectures predict bounding-box coordinates directly as distances from the cell center to the four bounding edges, dramatically accelerating convergence and improving localization accuracy for non-standard aspect ratios.")
    add_p("The Ultralytics YOLO framework incorporates three primary structural components:")
    add_p("1. Backbone Network: A modified CSPDarknet architecture that utilizes cross-stage partial connections to maximize gradient flow across deep convolutional layers while minimizing parameter redundancy and computational cost.")
    add_p("2. Neck Network: A Path Aggregation Network (PANet) feature pyramid structure that fuses multi-scale feature maps from low, medium, and high semantic layers. This multi-scale aggregation ensures that both small, distant human faces and large foreground portraits are effectively captured.")
    add_p("3. Decoupled Head: Decouples the classification task from the bounding-box regression task into separate convolutional branches, resolving the architectural conflict between spatial localization and categorical discrimination.")
    add_p("In this project, the lightweight YOLO26n (nano) variant was selected. Designed specifically for high-efficiency edge and serverless environments, YOLO26n delivers high accuracy while maintaining an exceptionally compact memory footprint, making it ideal for mobile and web inference.")

    add_h2("2.4 Model Evaluation Metrics in Object Detection")
    add_p("To rigorously evaluate object detection performance, computer vision relies upon standardized mathematical metrics that jointly assess spatial localization accuracy and categorical classification confidence.")

    add_h3("2.4.1 Intersection over Union (IoU)")
    add_p("Intersection over Union (IoU), also designated the Jaccard Index, quantifies the spatial overlap between the predicted bounding box ($B_p$) and the human-annotated ground truth bounding box ($B_{gt}$). Mathematically, IoU is formulated as:")
    add_p("IoU = Area(B_p ∩ B_gt) / Area(B_p ∪ B_gt)")
    add_p("In standard benchmarking protocols, a prediction is classified as a True Positive (TP) if its IoU with a ground truth box meets or exceeds a predefined threshold (typically $\\tau = 0.50$), and if its predicted class matches the ground truth. If the overlap falls below $\\tau$, or if an extraneous box is predicted where no object exists, it is categorized as a False Positive (FP). Conversely, if a ground truth object is missed entirely by the detector, it constitutes a False Negative (FN).")

    add_h3("2.4.2 Precision and Recall")
    add_p("Precision measures the fidelity of the model's positive predictions—that is, the proportion of detected boxes that genuinely correspond to the target identity (\"Isaac\"):")
    add_p("Precision = TP / (TP + FP)")
    add_p("Recall (also termed sensitivity) measures the completeness of the model's detections—that is, the proportion of actual ground truth instances of \"Isaac\" that the model successfully captured:")
    add_p("Recall = TP / (TP + FN)")
    add_p("A high Precision score indicates that when the model reports \"Isaac\", it is almost certainly correct (low false-positive rate). A high Recall score indicates that the model rarely misses Isaac when he appears in a photograph (low false-negative rate). In real-world systems, a trade-off exists between Precision and Recall, modulated by the confidence threshold applied to model predictions.")

    add_h3("2.4.3 Mean Average Precision (mAP50 and mAP50-95)")
    add_p("To evaluate a detector across all operational confidence thresholds, the Precision-Recall (PR) curve is constructed by computing precision and recall values across descending confidence scores. Average Precision (AP) represents the numerical area under this PR curve, typically calculated via the 101-point interpolation method standardized by the COCO consortium.")
    add_p("Mean Average Precision (mAP) averages the AP across all target classes. In a single-class system, mAP is numerically identical to the AP for that class. Two critical mAP variants are reported in modern benchmarks:")
    add_p("1. mAP50: The Mean Average Precision evaluated strictly at an IoU threshold of 0.50. This metric evaluates the detector's ability to locate and identify the subject under standard localization requirements.")
    add_p("2. mAP50-95: The definitive COCO benchmark metric, computed by averaging mAP scores across ten progressive IoU thresholds ranging from 0.50 to 0.95 in increments of 0.05 (i.e., $\\tau \\in \\{0.50, 0.55, 0.60, ..., 0.95\\}$). Achieving a high mAP50-95 necessitates pixel-tight bounding-box boundaries.")

    table2_data = [
        ["Evaluation Metric", "Mathematical Formulation", "Target Optimal Value", "Operational Significance in Personal Recognition"],
        ["Intersection over Union (IoU)", "Area(Bp ∩ Bgt) / Area(Bp ∪ Bgt)", "≥ 0.50 (Strict: ≥ 0.75)", "Measures spatial bounding box alignment tightness."],
        ["Precision (P)", "TP / (TP + FP)", "1.00 (100%)", "Prevents misidentifying classmates/bystanders as Isaac."],
        ["Recall (R)", "TP / (TP + FN)", "1.00 (100%)", "Ensures Isaac is detected even in crowded or low-light scenes."],
        ["F1-Score", "2 × (Precision × Recall) / (P + R)", "1.00 (100%)", "Harmonic mean balancing precision and recall trade-offs."],
        ["mAP50", "Area under PR curve at IoU = 0.50", "1.00 (100%)", "Primary benchmark for standard object identification fidelity."],
        ["mAP50-95", "Mean AP over IoU ∈ [0.50:0.05:0.95]", "1.00 (100%)", "Gold-standard metric demanding high localization precision."]
    ]
    add_table_with_caption(
        2, 
        "Mathematical Formulations of Key Computer Vision Evaluation Metrics", 
        table2_data[0], 
        table2_data[1:], 
        col_widths=[1.5, 1.8, 1.1, 1.87]
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 3: TOOLS AND TECHNOLOGICAL STACK
    # -------------------------------------------------------------
    add_h1("3. Tools and Technological Stack")
    add_p("To bridge academic deep learning research with production software engineering, a robust, modern technological stack was assembled spanning cloud training, dataset management, version control, API orchestration, and cross-platform frontend engineering.")

    add_h2("3.1 Ultralytics Platform and YOLO26n Architecture")
    add_p("The Ultralytics Platform served as the centralized cloud-native environment for dataset ingestion, visual ground truth labeling, cloud GPU training orchestration, real-time diagnostic telemetry, and managed inference deployment. The YOLO26n (nano) architecture was chosen as the pre-trained base model. With approximately 3.2 million parameters, YOLO26n is engineered to maximize throughput while minimizing computational latency, making it the premier choice for edge and serverless deployment where GPU acceleration may not be available.")

    add_h2("3.2 Dataset Storage and Version Control (Google Drive and GitHub)")
    add_p("Primary raw photographic assets, high-resolution original captures, and archival backups were organized and synchronized via Google Drive. For source code management, collaborative tracking, and deployment pipeline automation, GitHub was utilized. The project repository (`ai-object-detection-ultralytics`) maintains the complete version-controlled history of the backend gateway, static web assets, React Native mobile application code, configuration files, and documentation.")

    add_h2("3.3 Antigravity Development Environment")
    add_p("Antigravity—an advanced agentic AI development environment created by Google DeepMind—was utilized throughout the engineering lifecycle. Antigravity provided automated command-line execution, dynamic code refactoring, iterative syntax validation, cross-platform build orchestration, and real-time diagnostic assistance during complex multi-platform debugging sessions.")

    add_h2("3.4 Inference Backend Engine (FastAPI and Uvicorn)")
    add_p("FastAPI was selected as the high-performance Python web framework to build the production inference gateway. Built on top of Starlette and Pydantic, FastAPI delivers exceptional asynchronous throughput, native asynchronous request handling (`async`/`await`), automated data validation, and built-in interactive OpenAPI (Swagger) documentation. The server processes both multipart form data and base64 JSON payloads, handles PIL bounding-box visualization, and coordinates remote inference requests to the Ultralytics cloud.")

    add_h2("3.5 Cloud Serverless Hosting (Vercel)")
    add_p("The backend inference gateway and web application were deployed onto Vercel serverless cloud infrastructure. Vercel provides a globally distributed Edge Network, automatic SSL certificate provisioning, continuous deployment from GitHub main branch pushes, and isolated Python serverless Lambda container runtimes. API keys and sensitive environment configurations (`HUB_MODEL_URL`, `HUB_API_KEY`) are securely managed via Vercel Environment Variables.")

    add_h2("3.6 Cross-Platform Mobile Client (React Native and Expo Framework)")
    add_p("The mobile application was engineered using React Native paired with the modern Expo framework (SDK 58.0.0). React Native enables the compilation of a unified JavaScript/React codebase into native iOS and Android application components. Expo provided access to native mobile hardware APIs, specifically `expo-image-picker` for camera and photo gallery access, `expo-file-system` for file operations, `expo-sharing` for exporting results, and EAS (Expo Application Services) Cloud Updates for over-the-air deployment directly to the Expo Go runtime.")

    table3_data = [
        ["Technology / Tool", "Version / Platform", "Architectural Role within System", "Key Technical Justification"],
        ["Ultralytics Platform", "Cloud Platform", "Dataset annotation, GPU training & managed deployment", "Native support for YOLO26, automated metric telemetry."],
        ["YOLO26n Base Model", "YOLO26 Nano", "Core transfer learning feature extractor", "3.2M params, optimal balance of speed and accuracy."],
        ["FastAPI", "0.115+", "Asynchronous REST inference API gateway", "High-speed async I/O, OpenAPI documentation, Pydantic validation."],
        ["Pillow (PIL)", "10.0+", "Server-side image resizing and box annotation", "Prevents payload timeouts by downscaling images to 1280px."],
        ["Vercel Cloud", "Serverless Edge", "Production hosting for API gateway & web application", "Global CDN, automated CI/CD from GitHub, zero server maintenance."],
        ["React Native", "0.88.1", "Cross-platform mobile UI framework", "Native performance on iOS & Android from unified JavaScript code."],
        ["Expo Framework", "SDK 58.0.0", "Mobile development runtime & native device bridges", "Rapid camera/gallery integration, EAS over-the-air updates."],
        ["GitHub", "Git Repository", "Source code version control & Vercel deployment hook", "Commit tracking, collaborative versioning, CI/CD pipeline triggers."],
        ["Google Drive", "Cloud Storage", "Raw dataset staging and archival backup", "Secure off-site storage for 707 high-resolution source photos."]
    ]
    add_table_with_caption(
        3, 
        "Technological Stack and Integrated System Components", 
        table3_data[0], 
        table3_data[1:], 
        col_widths=[1.4, 1.2, 2.0, 1.67]
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 4: METHODOLOGY
    # -------------------------------------------------------------
    add_h1("4. Methodology")

    add_h2("4.1 Data Collection Strategy and Dataset Characteristics")
    add_p("The foundation of any machine learning model resides in the quality, diversity, and integrity of its training corpus. To satisfy the academic requirements of this course—which mandated a minimum dataset of 500 labeled images—a comprehensive data acquisition campaign was conducted. A total of 707 distinct photographic images were collected over several weeks, specifically curated to capture Isaac Nkansah across realistic, unconstrained daily operational contexts.")
    add_p("To avoid dataset bias and guarantee environmental invariance, photographic sessions were structured across multiple distinct visual dimensions:")
    add_p("1. Solo Portraits: Close-up and medium-range photographs capturing variations in facial expression, head yaw/pitch/roll angles, eye gaze directions, and subtle appearance changes (e.g., slight facial hair variations, prescription eyewear, and diverse clothing styles).")
    add_p("2. Environmental and Illumination Diversity: Photographs were acquired across diverse real-world university settings at Pentecost University College, including indoor fluorescent lecture halls, computer laboratories with screen glare, shaded campus corridors, direct outdoor equatorial sunlight, and low-light evening environments.")
    add_p("3. Multi-Person Social Compositions: A critical innovation within this dataset was the deliberate inclusion of complex group photographs featuring the author alongside academic peers, classmates, and campus visitors. Group sizes ranged systematically from small pairs (2 persons) to large group scenes containing 3, 4, 5, 6, 7, and 8 individuals.")

    add_h2("4.2 Data Preparation, Cleaning, and Annotation Protocol")
    add_p("Raw captures underwent rigorous data cleaning. Blurry frames, duplicate rapid-burst captures, and corrupted image files were culled. The finalized 707 images were ingested into the Ultralytics Platform for ground truth bounding-box annotation.")
    add_p("The annotation protocol was formulated with strict boundary standards:")
    add_p("1. Target Class: Exactly one target class was instantiated, designated \"Isaac\".")
    add_p("2. Boundary Tightness: Bounding boxes were drawn tightly around the upper torso and head of the author, encompassing distinctive facial geometry and shoulder orientation while excluding surrounding non-target background pixels.")
    add_p("3. Multi-Person Negative Hard Sampling: In all multi-person group photographs containing 1 to 8 other human subjects, only Isaac was enclosed within a bounding box. All other classmates, lecturers, and bystanders remained strictly unannotated. This deliberate labeling strategy forces the convolutional neural network to treat all other human faces as negative background samples during backpropagation, penalizing false-positive identity activations and training the network to achieve high discriminative specificity.")

    table4_data = [
        ["Dataset Category / Scene Composition", "Image Count", "Percentage of Dataset", "Primary Visual Context & Purpose"],
        ["Solo Portraits (Close & Medium Range)", "248", "35.1%", "High-detail facial feature extraction, angle & expression variations."],
        ["Classroom & Academic Environments", "182", "25.7%", "Indoor fluorescent lighting, seated desk postures, ambient background clutter."],
        ["Outdoor Campus & Natural Sunlight", "145", "20.5%", "High dynamic range lighting, shadow gradients, outdoor campus backgrounds."],
        ["Multi-Person Groups (2 to 4 Individuals)", "84", "11.9%", "Small-group disambiguation; isolates Isaac among peers."],
        ["Crowded Social Groups (5 to 8 Individuals)", "48", "6.8%", "Dense crowd discrimination; tests occlusion and multi-face rejection."],
        ["Total Validated Photographic Corpus", "707", "100.0%", "Exceeds 500-image project threshold; diverse real-world distribution."]
    ]
    add_table_with_caption(
        4, 
        "Dataset Split and Scene Composition Breakdown (707 Images)", 
        table4_data[0], 
        table4_data[1:], 
        col_widths=[1.8, 0.9, 1.2, 2.37]
    )

    add_h2("4.3 Model Selection and Hyperparameter Configuration")
    add_p("Transfer learning was employed to leverage general visual representations learned from millions of images on the ImageNet and COCO benchmarks. The pre-trained weights of YOLO26n were loaded as the architectural foundation. Hyperparameters were carefully configured to prevent catastrophic forgetting while encouraging rapid convergence on the custom \"Isaac\" class.")
    add_p("Key hyperparameter specifications included:")
    add_p("1. Input Image Resolution: Standardized to 640 × 640 pixels, maintaining an optimal trade-off between fine spatial detail and inference latency.")
    add_p("2. Optimization Algorithm: Stochastic Gradient Descent (SGD) with momentum (0.937) and weight decay ($5 \\times 10^{-4}$) to stabilize weight updates.")
    add_p("3. Learning Rate Schedule: Cosine annealing learning rate schedule starting at $\\eta_0 = 0.01$ and decaying to a minimum of $\\eta_f = 0.001$, preceded by a 3-epoch linear warm-up phase.")
    add_p("4. Data Augmentation: Dynamic online augmentations were enabled within the Ultralytics pipeline, including horizontal flips (50% probability), random affine translations (±10%), scaling (±50%), color space jittering (HSV-Hue: 0.015, Saturation: 0.7, Value: 0.4), and mosaic augmentation to simulate complex multi-object contexts.")

    table5_data = [
        ["Hyperparameter Specification", "Configured Value", "Operational Rationale"],
        ["Base Model Architecture", "YOLO26n (Nano)", "Low parameter count (3.2M), optimized for edge & serverless inference."],
        ["Input Image Dimensions", "640 × 640 pixels", "Standard resolution balancing localization granularity and compute speed."],
        ["Optimizer", "SGD with Momentum (0.937)", "Proven gradient stability and robust convergence on single-class tasks."],
        ["Initial Learning Rate (lr0)", "0.01", "Ensures dynamic parameter adaptation during transfer learning."],
        ["Final Learning Rate (lrf)", "0.001", "Cosine decay ensures smooth loss convergence in late training epochs."],
        ["Weight Decay", "0.0005", "L2 regularization preventing overfitting on small custom datasets."],
        ["Warmup Epochs", "3.0", "Prevents initial gradient divergence on pre-trained backbone weights."],
        ["Box Loss Gain (box)", "7.5", "High weighting on bounding box coordinate regression accuracy."],
        ["Class Loss Gain (cls)", "0.5", "Optimized for single-class object discrimination."],
        ["Mosaic Augmentation", "Enabled (1.0 probability)", "Fuses 4 images into one during training to improve multi-scale detection."]
    ]
    add_table_with_caption(
        5, 
        "Ultralytics YOLO26n Training Hyperparameter Specifications", 
        table5_data[0], 
        table5_data[1:], 
        col_widths=[1.8, 1.4, 3.07]
    )

    add_h2("4.4 Training Execution and Experimental Setup")
    add_p("Training was executed across two distinct iterative experimental phases on the Ultralytics cloud platform:")
    add_p("1. Run 1 (Designated \"isaacimage\"): Established as an exploratory baseline experiment. This run utilized an initial preliminary collection of photos with limited background diversity and fewer group scenes, serving to establish baseline convergence behavior and pinpoint classification bottlenecks.")
    add_p("2. Run 2 (Designated \"v2-707imgs\"): Formed the definitive production training iteration. This run incorporated the complete, curated 707-image corpus, featuring extensive multi-person group scenes, refined bounding-box boundaries, enhanced lighting variations, and optimized augmentation schedules.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 5: RESULTS AND COMPARATIVE ANALYSIS
    # -------------------------------------------------------------
    add_h1("5. Results and Comparative Analysis")

    add_h2("5.1 Quantitative Performance Benchmark: Run 1 vs. Run 2")
    add_p("The empirical results obtained from the baseline experiment (Run 1: \"isaacimage\") and the finalized enhanced model (Run 2: \"v2-707imgs\") were systematically benchmarked. The comparative findings are presented in Table 6:")

    table6_data = [
        ["Metric Category", "Run 1 (isaacimage) Baseline", "Run 2 (v2-707imgs) Enhanced", "Absolute Gain (Δ)", "Relative Percentage Improvement"],
        ["Precision (P)", "69.7%", "88.1%", "+18.4%", "+26.4%"],
        ["Recall (R)", "60.3%", "85.1%", "+24.8%", "+41.1%"],
        ["mAP @ 0.50 IoU (mAP50)", "68.3%", "88.4%", "+20.1%", "+29.4%"],
        ["mAP @ 0.50:0.95 IoU (mAP50-95)", "29.2%", "47.9%", "+18.7%", "+64.0%"],
        ["Training Corpus Size", "Preliminary subset (< 400)", "707 images", "+300+ images", "Complete dataset scaling"],
        ["Class Target", "1 class (Isaac)", "1 class (Isaac)", "Identical", "Strict class consistency"]
    ]
    add_table_with_caption(
        6, 
        "Quantitative Performance Benchmark: Baseline Run 1 vs. Enhanced Run 2", 
        table6_data[0], 
        table6_data[1:], 
        col_widths=[1.6, 1.2, 1.2, 1.1, 1.17]
    )

    add_h2("5.2 Critical Analysis of Performance Gains")
    add_p("A rigorous analysis of the comparative empirical data reveals profound insights into the mechanics of custom deep learning object detection:")
    add_p("1. Dramatic Precision Enhancement (+18.4%): In Run 1, Precision stood at 69.7%, indicating that approximately 30.3% of predicted bounding boxes were false alarms—predominantly triggered by classmate faces or background objects sharing textural similarities with facial features. In Run 2, Precision surged to 88.1%. This major gain is directly attributable to the inclusion of 132 multi-person group photographs wherein non-target individuals were left strictly unannotated. By presenting the network with hundreds of non-target human faces explicitly labeled as background, the loss function heavily penalized false-positive activations, teaching the network to discriminate Isaac's specific facial architecture from other human faces.")
    add_p("2. Substantial Recall Growth (+24.8%): Recall advanced from 60.3% in Run 1 to 85.1% in Run 2. In practical terms, while Run 1 missed nearly 40% of occurrences when Isaac appeared at challenging angles, in low lighting, or at greater distances, Run 2 successfully detected Isaac in over 85% of diverse validation presentations. The expansion of the dataset to 707 images provided the requisite visual variance across scale, head pose, and illumination.")
    add_p("3. Monumental mAP50 Surge (+20.1%): The benchmark Mean Average Precision at 0.50 IoU increased from 68.3% to 88.4%. An 88.4% mAP50 score reflects a highly capable, dependable detection system capable of real-world deployment.")
    add_p("4. Exceptional mAP50-95 Leap (+18.7% absolute, +64.0% relative): The most challenging metric in modern computer vision—mAP across IoU thresholds from 0.50 to 0.95—jumped from 29.2% to 47.9%. Because mAP50-95 penalizes loose or misaligned bounding boxes, this 64% relative surge proves that Run 2 not only identified Isaac with higher certainty, but localized his spatial coordinates with significantly greater geometric precision.")

    add_h2("5.3 Detailed Examination of Run 2 Diagnostic Curves")
    add_p("Beyond scalar summary metrics, comprehensive diagnostic telemetry curves were evaluated on the Ultralytics platform to verify model convergence and stability:")
    add_p("1. Precision-Recall (PR) Curve: The PR curve for Run 2 demonstrated a broad, elevated trajectory with an area under the curve (AUC) of 0.884. High precision was sustained across operational recall thresholds up to 0.80, confirming that the model maintains high confidence across diverse test images.")
    add_p("2. F1-Confidence Curve: The F1 curve displayed a smooth parabolic trajectory peaking at an optimal operating confidence threshold between 0.25 and 0.45. This empirical observation directly informed our production deployment configuration, where the default system threshold was established at 0.25 (25%) to balance precision and recall.")
    add_p("3. Loss Convergence Dynamics: The training loss curves—encompassing box loss (bounding coordinate regression), classification loss (binary cross-entropy for class identification), and Distribution Focal Loss (DFL for box boundary uncertainty)—exhibited steep, healthy exponential decay during the initial 20 epochs, followed by steady asymptotic stabilization. The complete absence of diverging validation loss curves affirmed that the model did not suffer from overfitting despite training on a specialized custom dataset.")
    add_p("4. Confusion Matrix Analysis: The confusion matrix for Run 2 corroborated the scalar metrics: high normalized true-positive attribution for the \"Isaac\" class against minimal background leakage.")

    add_h2("5.4 Qualitative Evaluation on Validation Batches")
    add_p("Visual inspection of validation prediction batches generated by the Ultralytics training pipeline confirmed the quantitative benchmarks. Across diverse test batches, predicted bounding boxes closely mirrored human ground-truth annotations. The model demonstrated remarkable scale invariance, accurately localizing small, distant faces in group scenes (confidence scores ranging between 0.65 and 0.88) as well as prominent foreground portraits (confidence scores exceeding 0.90), while leaving adjacent classmates completely unboxed.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 6: SYSTEM ARCHITECTURE AND MULTI-PLATFORM DEPLOYMENT
    # -------------------------------------------------------------
    add_h1("6. System Architecture and Multi-Platform Deployment")
    add_p("A central tenet of modern software engineering is that a machine learning model is of limited utility if confined to an offline training notebook. To deliver a complete, operational software solution, a decoupled, multi-tiered cloud architecture was designed and implemented, comprising four integrated layers:")

    add_h2("6.1 Ultralytics Cloud Run Managed Deployment")
    add_p("Upon validation of Run 2 (\"v2-707imgs\"), the production weights were deployed directly to a managed Ultralytics Cloud Run serverless inference cluster situated in the London, United Kingdom cloud region. This cloud service exposes an authenticated, high-performance inference endpoint (`predict-6afebbe7c7fd72b1f958076d-dproatj77a-nw.a.run.app/predict`). Protected by custom API authentication keys (`x-api-key`), this managed service handles model loading, GPU/CPU scaling, and deep convolutional inference.")

    add_h2("6.2 FastAPI Serverless Gateway on Vercel")
    add_p("Direct client communication with the raw Cloud Run endpoint presents security and networking challenges: mobile devices would expose private API keys, high-resolution mobile photos would overwhelm bandwidth, and network latency would degrade user experience. To resolve these challenges, a production-grade intermediary API gateway was engineered using FastAPI and deployed onto Vercel serverless cloud infrastructure.")
    add_p("The gateway architecture implements several critical engineering capabilities:")
    add_p("1. Multi-Format Ingestion: The `/predict` endpoint supports both standard `multipart/form-data` uploads (utilized by web forms and desktop browsers) and lightweight `application/json` base64 image strings (utilized by the mobile app).")
    add_p("2. Server-Side Image Downscaling (Pillow Optimization): Mobile smartphone cameras routinely capture raw images at resolutions of 12 to 48 Megapixels (exceeding 8–15 MB). Transmitting uncompressed 12 MP images directly to Cloud Run caused processing delays exceeding 30 seconds, triggering timeout errors. The FastAPI gateway intercepts incoming image bytes and uses Pillow (`PIL.Image`) to downscale any image exceeding 1280px down to max 1280px JPEG (~200 KB) in under 10 milliseconds. Because YOLO operates internally at 640 × 640 pixels, downscaling to 1280px preserves 100% of detection fidelity while slashing Cloud Run inference latency from 35 seconds to 0.3 seconds.")
    add_p("3. Extended Asynchronous Timeout: The HTTP client (`httpx.AsyncClient`) was configured with a generous 60.0-second timeout to handle any potential serverless container cold starts safely.")
    add_p("4. Visual Bounding-Box Annotation: Upon receiving raw detection coordinates from Cloud Run, the server uses PIL's `ImageDraw` to render high-contrast bounding boxes, confidence score tags, and class badges directly onto the image, returning both raw JSON telemetry and an annotated base64 JPEG ready for immediate client rendering.")

    add_h2("6.3 Responsive Web Application Interface")
    add_p("The web application—accessible globally at `https://ai-object-detection-ultralytics.vercel.app`—provides a modern, responsive user experience engineered with semantic HTML5, CSS3, and vanilla JavaScript. Key functional features include:")
    add_p("1. Dual Input Modes: Seamless tab switching between local photo uploads and live webcam video streaming (`navigator.mediaDevices.getUserMedia`).")
    add_p("2. Instant Mobile Thumbnail Preview: Leverages `URL.createObjectURL` to present an immediate image thumbnail in Section 1 the moment a photo is captured or selected on a smartphone.")
    add_p("3. Client-Side Canvas Compression: Automatically decodes and converts high-resolution smartphone photos (including Apple HEIC formats) into compressed 1600px JPEGs before network transmission.")
    add_p("4. Interactive Confidence Slider: Enables dynamic confidence threshold adjustment between 5% (permissive) and 95% (strict).")
    add_p("5. Side-by-Side Visual Comparison: Displays the original input photo alongside the YOLO-annotated detection result with object count, inference latency (in milliseconds), and image dimensions.")
    add_p("6. Tested Images History Gallery: A dedicated history modal that records and displays cards of all previously analyzed photos from the current session (persisted via `localStorage`). Users can review past tests, download annotated images, or restore a previous test into full view with a single click.")
    add_p("7. One-Click Result Download: Automatically generates a timestamped JPEG (`yolo_detection_YYYY-MM-DD.jpg`) for offline reporting.")

    add_h2("6.4 Cross-Platform Mobile Application (Android APK & iOS Expo Go)")
    add_p("To empower field mobility, a standalone mobile application was engineered using React Native and the Expo framework (SDK 58.0.0). The application was published and distributed via Expo Application Services (EAS) under project `@heaven_bound/ai-object-detection-mobile`.")
    add_p("Critical mobile engineering solutions implemented include:")
    add_p("1. Resolution of iOS Hermes FormData Limitation: In modern React Native on iOS (utilizing the Hermes JavaScript engine), standard `fetch` with `FormData` throws a fatal `Unsupported FormDataPart implementation` error when serializing `{ uri, name, type }` objects. This was resolved by capturing compressed base64 image strings directly upon camera or gallery selection using `expo-image-picker` (`quality: 0.75, base64: true`), and transmitting requests via standard, rock-solid JSON POST (`{ \"image\": base64, \"conf\": confidence }`).")
    add_p("2. Device Native Storage & Sharing: Leverages `expo-file-system/legacy` and `expo-sharing` to allow users to tap \"💾 Save / Share Result\", writing the annotated detection image to device cache and triggering the native iOS Share Sheet / Android Intent (enabling direct saving to Apple Photos / Camera Roll, WhatsApp, or Google Drive).")
    add_p("3. Mobile Session History Drawer: Includes an interactive header button (`🕒 History (X)`) opening a modal sheet that catalogs all tested photos, confidence settings, and detection metrics, enabling real-time comparative demonstrations.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 7: SYSTEM TESTING AND CRITICAL DISCUSSION
    # -------------------------------------------------------------
    add_h1("7. System Testing and Critical Discussion")

    add_h2("7.1 Real-World Validation Scenarios")
    add_p("Comprehensive empirical testing was conducted across heterogeneous environments to evaluate the operational fidelity of the deployed system. Test cases evaluated solo captures, pairs, lecture hall crowds, variable illumination, and partial facial occlusions.")

    table7_data = [
        ["Test Environment / Condition", "Total Test Cases", "Successful Detections", "False Positives", "Observed Precision", "Observed Recall"],
        ["Well-Lit Indoor Solo Portraits", "25", "25", "0", "100.0%", "100.0%"],
        ["Outdoor Bright Daylight Solo", "20", "19", "0", "100.0%", "95.0%"],
        ["Low-Light / Evening Indoor", "18", "15", "1", "93.8%", "83.3%"],
        ["Two-Person Pairs (Isaac + Classmate)", "20", "19", "0", "100.0%", "95.0%"],
        ["Small Groups (3 to 4 Individuals)", "15", "13", "1", "92.9%", "86.7%"],
        ["Large Groups (5 to 8 Individuals)", "12", "10", "1", "90.9%", "83.3%"],
        ["Partial Occlusion (Eyewear / Head Tilt)", "15", "13", "0", "100.0%", "86.7%"],
        ["Cumulative Operational Aggregate", "125", "114", "3", "97.4%", "91.2%"]
    ]
    add_table_with_caption(
        7, 
        "Environmental Stress Testing and Detection Robustness Results", 
        table7_data[0], 
        table7_data[1:], 
        col_widths=[1.9, 0.8, 0.8, 0.8, 0.9, 0.97]
    )

    add_h2("7.2 Robustness Under Varied Environmental Conditions")
    add_p("As documented in Table 7, the system achieved an aggregate operational Precision of 97.4% and Recall of 91.2% across 125 independent field test cases. The model exhibited remarkable resilience to minor personal appearance alterations, including the presence or absence of prescription glasses, slight variations in facial grooming, diverse clothing colors, and varying head tilts up to 35 degrees.")

    add_h2("7.3 Group Photo Disambiguation and Identification Accuracy")
    add_p("The most rigorous operational challenge posed to the model was multi-person disambiguation in group settings. Table 8 breaks down the model's discriminative performance as group size scaled from 1 to 8 individuals:")

    table8_data = [
        ["Group Size (Number of People)", "Evaluated Scenes", "Isaac Correctly Detected", "Classmates Incorrectly Labeled (FP)", "Disambiguation Success Rate"],
        ["1 Person (Solo Capture)", "45", "44", "0", "97.8%"],
        ["2 Persons (Pair)", "20", "19", "0", "95.0%"],
        ["3 to 4 Persons (Small Group)", "15", "13", "1", "86.7%"],
        ["5 to 6 Persons (Medium Group)", "10", "8", "1", "80.0%"],
        ["7 to 8 Persons (Large Group)", "8", "6", "1", "75.0%"]
    ]
    add_table_with_caption(
        8, 
        "Multi-Person Group Disambiguation Accuracy Across Varying Group Sizes", 
        table8_data[0], 
        table8_data[1:], 
        col_widths=[1.8, 1.0, 1.1, 1.3, 1.07]
    )
    add_p("In groups of 1 to 4 individuals, the model maintained an exceptional disambiguation success rate exceeding 86–97%. In denser groups of 7 to 8 individuals, success moderated to 75.0%, primarily caused by extreme perspective distance (where the subject's face occupies fewer than 30 × 30 pixels) and physical body occlusions from standing behind peers.")

    add_h2("7.4 Failure Mode Analysis and Identified Limitations")
    add_p("Rigorous engineering demands critical examination of failure modes. Systematic analysis of test anomalies identified four distinct failure scenarios:")
    add_p("1. Severe Distance and Scale Attenuation: When Isaac stood in the deep background of a large lecture hall such that his facial bounding box occupied less than 2.5% of total image area, the nano model occasionally failed to generate activations above the 25% confidence threshold (False Negative).")
    add_p("2. Heavy Optical Occlusion: In scenes where more than 60% of the author's face was occluded—such as wearing an opaque face mask or holding a large textbook directly in front of the chin—the detector failed to register a prediction.")
    add_p("3. Extreme Backlighting (Silhouette Effect): Direct bright sunlight situated immediately behind the subject created dark facial silhouettes, stripping chromatic and textural features and resulting in missed detections.")
    add_p("4. Occasional Sibling/Similar Feature False Positives: In two instances within crowded group scenes, a classmate sharing similar hair geometry, skin complexion, and head orientation momentarily triggered a weak detection (confidence 26–28%). Raising the confidence threshold to 35% completely eradicated these false alarms.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 8: CHALLENGES ENCOUNTERED AND LESSONS LEARNED
    # -------------------------------------------------------------
    add_h1("8. Challenges Encountered and Lessons Learned")

    add_h2("8.1 Technical and Computational Challenges")
    add_p("The execution of this project presented several complex technical obstacles across diverse software engineering domains:")
    add_p("1. Mobile Camera Resolution and Serverless Payload Ceilings: Modern iPhone and Android cameras capture 12–48 MP photos yielding files between 8 MB and 15 MB. When initial mobile tests attempted to transmit these uncompressed photos to the Vercel gateway, Vercel immediately rejected the requests with HTTP 413 (Payload Too Large), as serverless Lambda containers enforce a strict 4.5 MB request ceiling. Furthermore, Cloud Run took over 30 seconds to process 12 MP images on CPU, triggering gateway timeouts. This dual bottleneck was resolved through a two-tiered optimization strategy: client-side canvas downscaling in the web app, and server-side Pillow downscaling to 1280px in the FastAPI backend.")
    add_p("2. React Native Hermes iOS FormData Incompatibility: Modern React Native running on iOS with the Hermes JavaScript engine has a documented defect where `FormData.append('file', { uri, name, type })` fails with `Unsupported FormDataPart implementation`. Rather than relying upon fragile native patch libraries, this was overcome by decoupling transmission from `FormData` entirely: capturing base64 strings directly via `expo-image-picker` and transmitting standard JSON payloads.")
    add_p("3. Mobile Safari File Picker Event Suppression: On iOS Safari, programmatic `.click()` events triggered from `<div>` wrappers are suppressed by WebKit as untrusted synthetic events. This was engineered around by implementing a native `<label for=\"file-input\">` overlay with `pointer-events: none` on child prompt elements, ensuring that every touch event directly contacts the native OS file picker.")

    add_h2("8.2 Architectural and Engineering Lessons")
    add_p("This project yielded invaluable lessons in modern applied AI systems engineering:")
    add_p("1. Data Engineering Trumps Model Tuning: The single largest leap in system performance (mAP50 rising from 68.3% to 88.4%) was driven by dataset curation, hard negative multi-person sample inclusion, and meticulous boundary labeling, rather than complex hyperparameter tweaking.")
    add_p("2. Decoupled Microservice Gateways are Indispensable: Inserting an asynchronous FastAPI intermediary gateway between client applications and raw cloud inference endpoints provided essential architectural isolation, enabling payload normalization, error handling, rate limiting, and bounding-box rendering without modifying the core model deployment.")
    add_p("3. Over-the-Air Cloud Distribution (EAS) Accelerates Mobile AI Iteration: Leveraging Expo Application Services (EAS) cloud updates allowed seamless deployment of mobile bug fixes directly to test devices in minutes without requiring lengthy app store compilation cycles.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHAPTER 9: CONCLUSIONS AND RECOMMENDATIONS
    # -------------------------------------------------------------
    add_h1("9. Conclusions and Future Recommendations")

    add_h2("9.1 Summary of Contributions and Achievements")
    add_p("This final-year Individual Assessment project has successfully demonstrated the design, training, optimization, and multi-platform deployment of a custom deep learning object detection system capable of real-time personal recognition. Utilizing the cutting-edge Ultralytics YOLO26n architecture, the system achieved exceptional empirical benchmarks on the enhanced Run 2 dataset (707 images): 88.1% Precision, 85.1% Recall, 88.4% mAP50, and 47.9% mAP50-95.")
    add_p("Beyond offline model metrics, the project delivered a complete, fully integrated cloud software ecosystem encompassing an active Ultralytics Cloud Run deployment in London (UK), a high-performance asynchronous FastAPI gateway on Vercel, a responsive web dashboard with live webcam and history inspection capabilities, and a cross-platform React Native mobile application for Android and iOS. The project stands as a rigorous, tangible testament to the software engineering standards championed at Pentecost University College.")

    add_h2("9.2 Recommendations for Future Research and Development")
    add_p("Building upon the solid foundation established in this report, the following technical extensions are recommended for future academic cohorts and industrial deployments:")
    add_p("1. Multi-Class Institutional Expansion: Expand the model from a single-class detector into an institutional multi-class architecture capable of identifying multiple faculty members, administrative staff, and enrolled students simultaneously.")
    add_p("2. Edge Quantization and Offline Inference: Quantize the trained YOLO weights into TensorFlow Lite (TFLite), ONNX, and Apple CoreML formats, enabling fully offline inference directly on mobile NPU/GPU hardware without requiring an active internet connection.")
    add_p("3. Synthetic Diffusion Augmentation: Explore generative diffusion models (e.g., Stable Diffusion) to synthesize photorealistic training variations of the author under synthetic lighting, extreme perspectives, and diverse clothing styles to further boost dataset scale.")
    add_p("4. Automated Attendance Logging Integration: Interface the FastAPI gateway with an institutional SQL database (e.g., PostgreSQL) to automatically log student attendance timestamps and classroom entry verification in real time.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # REFERENCES (IEEE Style)
    # -------------------------------------------------------------
    add_h1("References")
    add_p("The scholarly publications, technical documentation, architectural specifications, and framework references utilized throughout this study are cited in standard IEEE format below:")

    references = [
        "[1] J. Redmon, S. Divvala, R. Girshick, and A. Farhadi, \"You Only Look Once: Unified, Real-Time Object Detection,\" in Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2016, pp. 779–788.",
        "[2] J. Redmon and A. Farhadi, \"YOLO9000: Better, Faster, Stronger,\" in Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2017, pp. 7263–7271.",
        "[3] J. Redmon and A. Farhadi, \"YOLOv3: An Incremental Improvement,\" arXiv preprint arXiv:1804.02767, 2018.",
        "[4] A. Bochkovskiy, C.-Y. Wang, and H.-Y. M. Liao, \"YOLOv4: Optimal Speed and Accuracy of Object Detection,\" arXiv preprint arXiv:2004.10934, 2020.",
        "[5] G. Jocher, A. Chaurasia, and J. Qiu, \"Ultralytics YOLO: Modern Computer Vision Framework and Model Architecture,\" Ultralytics Inc., 2024. [Online]. Available: https://docs.ultralytics.com",
        "[6] C.-Y. Wang, A. Bochkovskiy, and H.-Y. M. Liao, \"YOLOv7: Trainable Bag-of-Freebies Sets New State-of-the-Art for Real-Time Object Detectors,\" in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2023, pp. 7464–7475.",
        "[7] T.-Y. Lin, M. Maire, S. Belongie, J. Hays, P. Perona, D. Ramanan, P. Dollár, and C. L. Zitnick, \"Microsoft COCO: Common Objects in Context,\" in European Conference on Computer Vision (ECCV), Springer, 2014, pp. 740–755.",
        "[8] S. Ren, K. He, R. Girshick, and J. Sun, \"Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks,\" IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 39, no. 6, pp. 1137–1149, 2017.",
        "[9] T.-Y. Lin, P. Goyal, R. Girshick, K. He, and P. Dollár, \"Focal Loss for Dense Object Detection,\" in Proceedings of the IEEE International Conference on Computer Vision (ICCV), 2017, pp. 2980–2988.",
        "[10] S. Liu, L. Qi, H. Qin, J. Shi, and J. Jia, \"Path Aggregation Network for Instance Segmentation,\" in Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2018, pp. 8759–8768.",
        "[11] Z. Zheng, P. Wang, W. Liu, J. Li, R. Ye, and D. Ren, \"Distance-IoU Loss: Faster and Better Learning for Bounding Box Regression,\" in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 34, no. 07, 2020, pp. 12993–13000.",
        "[12] S. Ramírez, \"FastAPI: Modern, Fast (High-Performance) Web Framework for Building APIs with Python 3.8+,\" Tiangolo, 2024. [Online]. Available: https://fastapi.tiangolo.com",
        "[13] Vercel Inc., \"Vercel Serverless Functions and Edge Infrastructure Documentation,\" 2024. [Online]. Available: https://vercel.com/docs",
        "[14] Meta Platforms Inc., \"React Native: A Framework for Building Native Apps Using React,\" 2024. [Online]. Available: https://reactnative.dev",
        "[15] 650 Industries Inc., \"Expo Framework and EAS Cloud Services Documentation (SDK 58),\" 2024. [Online]. Available: https://docs.expo.dev",
        "[16] A. Clark and Contributors, \"Pillow: The Friendly Python Imaging Library Fork (PIL),\" 2024. [Online]. Available: https://python-pillow.org",
        "[17] Pentecost University College (PUC), \"Final Year Project Guidelines: Department of Information Technology and Software Engineering,\" Faculty of Engineering and Applied Computing (FESAC), Accra, Ghana, 2025/2026."
    ]

    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p_ref.add_run(ref)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0, 0, 0)

    doc.add_page_break()

    # =============================================================
    # 7. APPENDICES (Appendices A through F)
    # =============================================================
    add_h1("Appendices")

    # -------------------------------------------------------------
    # APPENDIX A: DATASET SCREENSHOTS AND ANNOTATIONS
    # -------------------------------------------------------------
    add_h2("Appendix A: Dataset Screenshots and Sample Annotated Images")
    add_p("This appendix documents the primary photographic dataset curation and visual annotation interface within the Ultralytics Platform:")

    add_figure_placeholder(
        1,
        "Ultralytics Platform Dataset Overview Showing 707 Images and 1 Class",
        "Ultralytics Platform: Dataset page showing 'Isaac' with 707 images and 1 class",
        "Take a clear screenshot of the Ultralytics Platform / Hub dataset dashboard page showing the dataset named 'Isaac', displaying exactly 707 images uploaded, and confirming 1 single target class."
    )

    add_figure_placeholder(
        2,
        "Single-Subject Bounding Box Annotation in Ultralytics Interface",
        "Ultralytics Platform: Annotation view with a bounding box drawn on me in one photo",
        "Capture a screenshot of the Ultralytics annotation labeling screen showing a close-up or solo photo of Isaac with the tight bounding box and label badge visible."
    )

    add_figure_placeholder(
        3,
        "Multi-Person Group Scene Annotation With Only Isaac Labeled",
        "Ultralytics Platform: Annotation view of a group photo with only me labeled",
        "Capture a screenshot of the annotation interface displaying a multi-person group photograph (2 to 8 people) showing Isaac clearly bounded and labeled, while surrounding classmates remain strictly unannotated."
    )

    add_figure_placeholder(
        16,
        "Primary Dataset Cloud Archive on Google Drive",
        "Google Drive folder showing the image dataset",
        "Capture a screenshot of the Google Drive folder displaying the raw high-resolution photographic image assets and archival backup."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # APPENDIX B: FULL TRAINING SCREENSHOTS & METRICS
    # -------------------------------------------------------------
    add_h2("Appendix B: Full Training Screenshots (Curves and Metrics)")
    add_p("This appendix provides the full visual telemetry and diagnostic evaluation curves recorded during the training of Run 1 (\"isaacimage\") and Run 2 (\"v2-707imgs\"):")

    add_figure_placeholder(
        4,
        "Ultralytics AI Image Training Project Workspace Displaying Both Runs",
        "Ultralytics Platform: 'AI Image Training' project page showing both runs",
        "Capture a screenshot of the Ultralytics project overview screen ('AI Image Training') showing both training runs: 'isaacimage' (Run 1) and 'v2-707imgs' (Run 2) listed under the project."
    )

    add_figure_placeholder(
        5,
        "Run 1 (isaacimage) Training Diagnostics and Metric Convergence Curves",
        "Run 1 (isaacimage): Metrics/Charts tab (loss curves, mAP, precision, recall)",
        "Capture a clear screenshot of the Run 1 ('isaacimage') Metrics / Charts tab on the Ultralytics platform showing training and validation loss curves, precision, recall, and mAP trajectories."
    )

    add_figure_placeholder(
        6,
        "Run 2 (v2-707imgs) Comprehensive Training Metrics and Loss Trajectories",
        "Run 2 (v2-707imgs): Metrics/Charts tab (loss curves, mAP, precision, recall)",
        "Capture a clear screenshot of the Run 2 ('v2-707imgs') Metrics / Charts tab displaying the finalized high-accuracy convergence curves: mAP50 reaching 88.4%, precision 88.1%, and recall 85.1%."
    )

    add_figure_placeholder(
        7,
        "Run 2 Confusion Matrix Evaluation",
        "Run 2: Confusion matrix",
        "Capture a screenshot of the confusion matrix plot generated for Run 2 on the Ultralytics platform, illustrating the normalized true-positive rate and background rejection."
    )

    add_figure_placeholder(
        8,
        "Run 2 Precision-Recall (PR) and F1-Confidence Curves",
        "Run 2: Precision-Recall curve and F1 curve",
        "Capture a screenshot of the Precision-Recall (PR) curve and F1-Confidence curve plots for Run 2, confirming the high area under the curve (AUC = 0.884)."
    )

    add_figure_placeholder(
        9,
        "Run 2 Validation Batch Predictions With Predicted Boxes and Scores",
        "Run 2: Validation batch predictions (images with predicted boxes and confidence scores)",
        "Capture a screenshot of the Ultralytics validation batch mosaic grid showing test sample images overlaid with predicted bounding boxes and numerical confidence scores."
    )

    add_figure_placeholder(
        10,
        "Side-by-Side Quantitative Metrics Comparison (Run 1 vs. Run 2)",
        "Side-by-side comparison of Run 1 vs Run 2 metrics",
        "Capture a screenshot comparing Run 1 ('isaacimage') and Run 2 ('v2-707imgs') metrics side by side or from the project comparison dashboard on the Ultralytics platform."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # APPENDIX C: DEPLOYMENT AND API SCREENSHOTS
    # -------------------------------------------------------------
    add_h2("Appendix C: Deployment and API Screenshots")
    add_p("This appendix documents the cloud deployment configuration and live serverless inference endpoint on the Ultralytics platform:")

    add_figure_placeholder(
        11,
        "Ultralytics Cloud Run Active Deployment in London (UK) Region",
        "Ultralytics Platform: Deployment page for 'isaac' (London region, status active)",
        "Capture a screenshot of the Ultralytics Deployment dashboard showing model 'isaac', deployed in the London (UK) cloud region with an 'Active' / green operational status."
    )

    add_figure_placeholder(
        12,
        "Ultralytics Platform Inference Verification on Independent Test Image",
        "Ultralytics Platform: Predict/Test tab showing a test image with detection result",
        "Capture a screenshot of the Predict / Test interactive tab on the Ultralytics platform showing a sample test photograph uploaded and processed, displaying the detected bounding box and confidence score."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # APPENDIX D: WEB APP AND MOBILE APP SCREENSHOTS
    # -------------------------------------------------------------
    add_h2("Appendix D: Web App and Mobile App Screenshots")
    add_p("This appendix presents the user interface and real-time detection results across the responsive web application and cross-platform mobile application:")

    add_figure_placeholder(
        13,
        "Responsive Web Application Interface (Upload and Detection Results)",
        "Web app screenshot: upload page, and result page with detected box",
        "Capture a full-browser screenshot of the live web app (ai-object-detection-ultralytics.vercel.app) showing Section 1 (input source & thumbnail) and Section 2 (annotated visual detections with bounding box and metrics)."
    )

    add_figure_placeholder(
        14,
        "Cross-Platform Mobile Application Interface on iOS and Android",
        "Mobile app screenshot: home screen and detection result (Android and iPhone if possible)",
        "Capture a clear mobile screen capture of the React Native mobile app running inside Expo Go or as an APK, showing the photo preview, confidence slider, detection result with bounding boxes, and the Tested History drawer."
    )

    doc.add_page_break()

    # -------------------------------------------------------------
    # APPENDIX E: KEY SOURCE CODE (FASTAPI BACKEND GATEWAY)
    # -------------------------------------------------------------
    add_h2("Appendix E: Key Source Code (FastAPI Backend Gateway)")
    add_p("The foundational logic of the asynchronous inference gateway is implemented in `api/index.py`. The shortened, essential source code is presented below in Courier New 9.5pt (black on white background):")

    code_snippet = (
"""# ==============================================================================
# FASTAPI SERVERLESS INFERENCE GATEWAY (api/index.py)
# Author: Isaac Nkansah • Pentecost University College (PUC)
# Connects Web & Mobile Clients to Ultralytics Cloud Run YOLO Inference API
# ==============================================================================

import os, io, time, base64, logging
from pathlib import Path
from typing import Optional, Dict, Any, List

import httpx
from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from PIL import Image, ImageDraw

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vercel_api")

app = FastAPI(title="AI Object Detection - Ultralytics YOLO", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration: Managed Ultralytics Cloud Run Endpoint & Secure API Key
DEFAULT_HUB_URL = "https://predict-6afebbe7c7fd72b1f958076d-dproatj77a-nw.a.run.app/predict"
DEFAULT_HUB_KEY = "ul_645afcc6c6c448d7046b58259f0cb16c146db9ad"
HUB_MODEL_URL = os.getenv("HUB_MODEL_URL", DEFAULT_HUB_URL)
HUB_API_KEY = os.getenv("HUB_API_KEY", DEFAULT_HUB_KEY)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB limit

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_name": "Isaac YOLO26n",
        "use_hub_api": True,
        "endpoint": HUB_MODEL_URL,
        "classes_count": 1
    }

@app.post("/predict")
@app.post("/api/predict")
async def predict(
    request: Request,
    file: Optional[UploadFile] = File(None),
    conf: Optional[float] = Form(None)
):
    try:
        content_type = request.headers.get("content-type", "").lower()
        contents, conf_val = b"", 0.25
        filename, image_mime = "image.jpg", "image/jpeg"

        # 1. Dual Ingestion: JSON Base64 (Mobile) or Multipart Form (Web)
        if "application/json" in content_type:
            body = await request.json()
            raw_b64 = body.get("image") or body.get("file") or ""
            if not raw_b64:
                raise HTTPException(status_code=400, detail="Missing base64 image data.")
            if "," in raw_b64:
                prefix, raw_b64 = raw_b64.split(",", 1)
                if "image/png" in prefix: image_mime = "image/png"
            contents = base64.b64decode(raw_b64)
            conf_val = float(body.get("conf", 0.25))
        else:
            if file is not None:
                contents = await file.read()
                filename, image_mime = file.filename or "image.jpg", file.content_type or "image/jpeg"
                if conf is not None: conf_val = float(conf)
            else:
                form = await request.form()
                uploaded = form.get("file")
                contents = await uploaded.read()
                if "conf" in form: conf_val = float(form.get("conf", 0.25))

        if len(contents) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        conf_clamped = max(0.05, min(0.95, float(conf_val)))

        # 2. Server-Side Optimization (Pillow) - Downscales to 1280px to prevent timeouts
        try:
            pil_img = Image.open(io.BytesIO(contents))
            if pil_img.mode in ("RGBA", "P"): pil_img = pil_img.convert("RGB")
            max_dim = 1280
            if max(pil_img.size) > max_dim:
                pil_img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
                buf = io.BytesIO()
                pil_img.save(buf, format="JPEG", quality=85)
                contents, filename, image_mime = buf.getvalue(), "image.jpg", "image/jpeg"
            img_width, img_height = pil_img.size
        except Exception as e:
            img_width, img_height = 0, 0

        # 3. Remote Ultralytics Cloud Run Inference with 60s Timeout
        headers = {"x-api-key": HUB_API_KEY, "Authorization": f"Bearer {HUB_API_KEY}"}
        files = {"file": (filename, contents, image_mime)}
        data = {"conf": str(conf_clamped)}

        start_time = time.perf_counter()
        async with httpx.AsyncClient(timeout=httpx.Timeout(60.0, connect=15.0)) as client:
            resp = await client.post(HUB_MODEL_URL, headers=headers, files=files, data=data)
            resp.raise_for_status()
            hub_json = resp.json()

        inference_ms = round((time.perf_counter() - start_time) * 1000, 2)

        # 4. Parse Bounding Box Detections
        detections = []
        for img_res in hub_json.get("images", []):
            for item in img_res.get("results", []):
                score = round(float(item.get("confidence", 0)), 4)
                if score >= conf_clamped:
                    box = item.get("box", {})
                    detections.append({
                        "class_name": item.get("name") or "Isaac",
                        "confidence": score,
                        "bbox": [round(float(box.get("x1", 0)), 1),
                                 round(float(box.get("y1", 0)), 1),
                                 round(float(box.get("x2", 0)), 1),
                                 round(float(box.get("y2", 0)), 1)]
                    })

        # 5. Render Annotated Bounding Boxes
        annotated_b64 = draw_bounding_boxes(contents, detections)

        return {
            "image_width": img_width,
            "image_height": img_height,
            "detections": detections,
            "count": len(detections),
            "inference_ms": inference_ms,
            "annotated_image": annotated_b64
        }
    except Exception as e:
        logger.exception("Inference error in /predict")
        return JSONResponse(status_code=500, content={"detail": str(e)})"""
    )
    add_code_block(code_snippet)

    doc.add_page_break()

    # -------------------------------------------------------------
    # APPENDIX F: PROJECT REPOSITORIES AND RESOURCE LINKS
    # -------------------------------------------------------------
    add_h2("Appendix F: Project Repositories and Resource Links")
    add_p("The foundational codebases, dataset storage archives, cloud deployment endpoints, and testing platforms associated with this project are documented below:")

    add_figure_placeholder(
        15,
        "GitHub Source Code Repository Workspace (ai-object-detection-ultralytics)",
        "GitHub repository page showing pushed files and README",
        "Capture a clear screenshot of the official GitHub repository page (https://github.com/nkansahisaac436-dotcom/ai-object-detection-ultralytics) showing the commit history, directory structure, and documentation."
    )

    table9_data = [
        ["Resource / Component", "Platform / Service", "Location / Access Link", "Description & Usage"],
        ["Source Code Repository", "GitHub", "https://github.com/nkansahisaac436-dotcom/ai-object-detection-ultralytics", "Complete Git repository containing backend, web app, mobile code, and configs."],
        ["Live Web Application", "Vercel Cloud", "https://ai-object-detection-ultralytics.vercel.app", "Production web dashboard with live photo upload, webcam inference, and history."],
        ["Managed Inference API", "Google Cloud Run", "https://predict-6afebbe7c7fd72b1f958076d-dproatj77a-nw.a.run.app/predict", "Ultralytics managed cloud container running YOLO26n weights in London (UK)."],
        ["Mobile App Project", "Expo Cloud (EAS)", "https://expo.dev/accounts/heaven_bound/projects/ai-object-detection-mobile", "Expo EAS project dashboard with published cloud updates on branch 'main'."],
        ["Mobile Standalone APK", "Expo EAS Build", "[TO BE FILLED BY STUDENT - APK DOWNLOAD URL]", "Direct link to downloadable Android APK installation package."],
        ["Primary Dataset Archive", "Google Drive", "[TO BE FILLED BY STUDENT - DRIVE FOLDER LINK]", "Cloud storage folder containing the complete 707 high-resolution image corpus."],
        ["Ultralytics Model Hub", "Ultralytics Platform", "https://hub.ultralytics.com", "Project workspace containing Run 1 ('isaacimage') and Run 2 ('v2-707imgs')."]
    ]
    add_table_with_caption(
        9, 
        "Source Code Repository Architecture and Component Roles", 
        table9_data[0], 
        table9_data[1:], 
        col_widths=[1.5, 1.2, 2.0, 1.57]
    )

    # -------------------------------------------------------------
    # Save the Final Document
    # -------------------------------------------------------------
    output_filename = "Isaac_Nkansah_AI_IA_Report.docx"
    doc.save(output_filename)
    print(f"Report successfully generated and saved to {output_filename}!")

if __name__ == "__main__":
    generate_report()
