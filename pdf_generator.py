from fpdf import FPDF

def generate_report_card(student_name, student_id, class_name, stream, term, marks_data):
    pdf = FPDF()
    pdf.add_page()
    
    # School Header (Maroon theme)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 8, txt="ST. MARY'S HIGH SCHOOL ZIROOBWE", ln=True, align="C")
    
    pdf.set_font("Arial", "I", 9)
    pdf.cell(200, 5, txt="P.O. Box 123, Ziroobwe | O-Level Academic Report", ln=True, align="C")
    pdf.ln(5)
    
    # Student Information Box
    pdf.set_font("Arial", "B", 10)
    pdf.cell(100, 6, txt=f"Student Name: {student_name}", ln=0)
    pdf.cell(90, 6, txt=f"Student ID: {student_id}", ln=1)
    pdf.cell(100, 6, txt=f"Class & Stream: {class_name} ({stream})", ln=0)
    pdf.cell(90, 6, txt=f"Term: {term}", ln=1)
    pdf.ln(4)
    
    # Marks Table Header
    pdf.set_font("Arial", "B", 9)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(70, 7, "Subject", 1, 0, "L", True)
    pdf.cell(25, 7, "Paper", 1, 0, "C", True)
    pdf.cell(25, 7, "Score", 1, 0, "C", True)
    pdf.cell(25, 7, "Grade", 1, 0, "C", True)
    pdf.cell(45, 7, "Remarks", 1, 1, "C", True)
    
    # Marks Rows
    pdf.set_font("Arial", "", 9)
    for subject, paper, score, grade, remarks in marks_data:
        pdf.cell(70, 6, subject, 1)
        pdf.cell(25, 6, paper, 1, 0, "C")
        pdf.cell(25, 6, str(score), 1, 0, "C")
        pdf.cell(25, 6, grade, 1, 0, "C")
        pdf.cell(45, 6, remarks, 1, 1, "C")
        
    pdf.ln(10)
    pdf.set_font("Arial", "B", 9)
    pdf.cell(200, 5, txt="Head Teacher's Signature: ______________________", ln=True)
    
    return pdf.output()
