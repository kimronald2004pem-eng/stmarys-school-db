import os
from fpdf import FPDF

class SchoolReportPDF(FPDF):
    def header(self):
        # Maroon Header Banner
        self.set_fill_color(128, 0, 0)
        self.rect(0, 0, 210, 28, 'F')
        
        # School Title
        self.set_text_color(255, 255, 255)
        self.set_font("helvetica", "B", 15)
        self.set_xy(10, 5)
        self.cell(190, 6, "ST. MARY'S HIGH SCHOOL KISAASI", 0, 1, "C")
        
        # Motto / Details
        self.set_font("helvetica", "I", 9)
        self.set_text_color(240, 220, 130) # Gold accent
        self.set_xy(10, 12)
        self.cell(190, 5, "P.O. Box 7000, Kampala | 'Excellence & Discipline'", 0, 1, "C")
        
        if os.path.exists("assets/school_badge.png"):
            self.image("assets/school_badge.png", x=12, y=3, w=20)
            
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Page {self.page_no()} | St. Mary's High School Official Management System", 0, 0, "C")

def generate_report_card(student_info, marks_list, exam_type):
    pdf = SchoolReportPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Report Title
    pdf.set_font("helvetica", "B", 11)
    pdf.set_text_color(128, 0, 0)
    pdf.cell(0, 8, f"OFFICIAL {exam_type.upper()} ACADEMIC REPORT - {student_info['term']} {student_info['year']}", 0, 1, "C")
    pdf.ln(2)

    # Student Bio Box
    pdf.set_draw_color(128, 0, 0)
    pdf.set_fill_color(248, 246, 240)
    pdf.rect(10, 38, 190, 28, 'FD')

    # Student Photo Frame Placeholder
    photo_x, photo_y = 168, 40
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(photo_x, photo_y, 28, 24, 'FD')
    
    if student_info.get('photo_path') and os.path.exists(student_info['photo_path']):
        pdf.image(student_info['photo_path'], x=photo_x+1, y=photo_y+1, w=26, h=22)
    else:
        pdf.set_font("helvetica", "I", 7)
        pdf.set_text_color(120, 120, 120)
        pdf.set_xy(photo_x, photo_y + 10)
        pdf.cell(28, 4, "PASSPORT", 0, 0, "C")
        pdf.set_xy(photo_x, photo_y + 14)
        pdf.cell(28, 4, "PHOTO", 0, 0, "C")

    # Bio Details
    pdf.set_text_color(40, 40, 40)
    pdf.set_font("helvetica", "B", 10)
    pdf.set_xy(14, 40)
    pdf.cell(80, 6, f"Name: {student_info['full_name']}", 0, 1, "L")
    
    pdf.set_font("helvetica", "", 9)
    pdf.set_x(14)
    pdf.cell(80, 5, f"Student ID: {student_info['student_id']}", 0, 1, "L")
    pdf.set_x(14)
    pdf.cell(80, 5, f"Class: {student_info['class_name']} ({student_info['level']})  |  Stream: {student_info.get('stream', 'N/A')}", 0, 1, "L")
    pdf.set_x(14)
    pdf.cell(80, 5, f"Boarding Status: {student_info['boarding_status']}", 0, 1, "L")

    pdf.ln(12)

    # Table Header (Maroon)
    pdf.set_fill_color(128, 0, 0)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("helvetica", "B", 9)
    
    pdf.cell(65, 7, "Subject Description", 1, 0, "L", True)
    pdf.cell(30, 7, "Score / Total", 1, 0, "C", True)
    pdf.cell(35, 7, "Grade / Level", 1, 0, "C", True)
    pdf.cell(60, 7, "Teacher's Evaluation Remark", 1, 1, "L", True)

    # Table Body
    pdf.set_text_color(40, 40, 40)
    pdf.set_font("helvetica", "", 9)
    fill = False
    
    for m in marks_list:
        pdf.set_fill_color(245, 242, 238) if fill else pdf.set_fill_color(255, 255, 255)
        pdf.cell(65, 6, str(m['subject_name']), 1, 0, "L", True)
        pdf.cell(30, 6, str(m['score']), 1, 0, "C", True)
        pdf.cell(35, 6, str(m['grade']), 1, 0, "C", True)
        pdf.cell(60, 6, str(m['comment']), 1, 1, "L", True)
        fill = not fill

    pdf.ln(15)

    # Signatures
    pdf.set_font("helvetica", "B", 9)
    pdf.cell(95, 6, "Class Teacher Signature: ___________________________", 0, 0)
    pdf.cell(95, 6, "Head Teacher Signature: ___________________________", 0, 1)

    return pdf.output()