from fpdf import FPDF

def generate_report_card(student_name, student_id, class_name, stream, term, marks_data):
    pdf = FPDF()
    pdf.add_page()

    # School Header (Maroon theme)
    pdf.set_fill_value = (128, 0, 0)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="ST. MARY'S HIGH SCHOOL ZIROOBWE", ln=True, align="C")

    pdf.set_font("Arial", "I", 10)
    pdf.cell(200, 6, txt="P.O. Box 123, Ziroobwe | Excellence & Discipline", ln=True, align="C")
    pdf.ln(10)

    # Student Information Box
    pdf.set_font("Arial", "B", 11)
    pdf.cell(100, 8, txt=f"Student Name: {student_name}", ln=0)
    pdf.cell(90, 8, txt=f"Student ID: {student_id}", ln=1)
    pdf.cell(100, 8, txt=f"Class & Stream: {class_name} ({stream})", ln=0)
    pdf.cell(90, 8, txt=f"Term: {term}", ln=1)
    pdf.ln(5)

    # Marks Table Header
    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(80, 8, "Subject", 1, 0, "L", True)
    pdf.cell(30, 8, "Score", 1, 0, "C", True)
    pdf.cell(35, 8, "Grade", 1, 0, "C", True)
    pdf.cell(45, 8, "Remarks", 1, 1, "C", True)

    # Marks Rows
    pdf.set_font("Arial", "", 10)
    for subject, score, grade, remarks in marks_data:
        pdf.cell(80, 7, subject, 1)
        pdf.cell(30, 7, str(score), 1, 0, "C")
        pdf.cell(35, 7, grade, 1, 0, "C")
        pdf.cell(45, 7, remarks, 1, 1, "C")

    pdf.ln(15)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(200, 6, txt="Head Teacher's Signature: ______________________", ln=True)

    return pdf.output(dest='S').encode('latin1')
