import streamlit as st
import sqlite3
from database import init_db, seed_demo_data, get_connection
from pdf_generator import generate_report_card

# Page Configuration
st.set_page_config(page_title="St. Mary's High School Ziroobwe MIS", layout="wide")

# Custom Styling (Maroon/Institutional Colors)
st.markdown("""
    <style>
        .main-header {color: #800000; font-weight: bold;}
        .stButton>button {background-color: #800000; color: white; border-radius: 5px;}
    </style>
""", unsafe_allow_html=True)

# Initialize database & demo records
init_db()
seed_demo_data()

st.markdown("# 🎓 St. Mary's High School Ziroobwe")
st.caption("100% Offline Local Management Information System")

# Sidebar Navigation Role Selector
role = st.sidebar.selectbox("Select Portal", ["Director of Studies (DOS)", "Bursar", "Head Teacher"])

conn = get_connection()

if role == "Director of Studies (DOS)":
    st.markdown("<h2 class='main-header'>📊 Director of Studies: Academic & Registration Portal</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📝 Register New Student", "📋 Student Directory", "🎓 Generate Report Card"])
    
    with tab1:
        st.subheader("New Student Registration")
        with st.form("reg_form"):
            col1, col2 = st.columns(2)
            with col1:
                s_id = st.text_input("Unique Student ID (e.g., SMHS-002)")
                fullname = st.text_input("Full Name")
                level = st.selectbox("Level", ["O-Level", "A-Level"])
            with col2:
                class_name = st.selectbox("Class", ["S.1", "S.2", "S.3", "S.4", "S.5", "S.6"])
                stream = st.selectbox("Stream", ["East", "West", "North", "South"])
                boarding = st.selectbox("Boarding Status", ["Boarding", "Day"])
            
            submitted = st.form_submit_button("Register Student")
            if submitted:
                if s_id and fullname:
                    try:
                        conn.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?);", 
                                     (s_id, fullname, level, class_name, stream, boarding))
                        conn.commit()
                        st.success(f"Successfully registered {fullname} ({s_id})!")
                    except sqlite3.IntegrityError:
                        st.error("Error: Student ID already exists. Please use a unique ID.")
                else:
                    st.warning("Please fill in both Student ID and Full Name.")

    with tab2:
        st.subheader("Enrolled Students Directory")
        cursor = conn.execute("SELECT * FROM students;")
        students = cursor.fetchall()
        if students:
            for s in students:
                st.write(f"🆔 **{s[0]}** | 👤 **{s[1]}** | 📚 {s[3]} ({s[2]} - {s[4]}) | 🏫 {s[5]}")
        else:
            st.info("No students registered yet.")

    with tab3:
        st.subheader("Official PDF Report Card Studio")
        cursor = conn.execute("SELECT student_id, full_name, class_name, stream FROM students;")
        students_list = cursor.fetchall()
        
        if students_list:
            student_dict = {f"{s[1]} ({s[0]})": s for s in students_list}
            selected_label = st.selectbox("Select Student", list(student_dict.keys()))
            selected_s = student_dict[selected_label]
            
            term = st.selectbox("Select Term", ["Term I", "Term II", "Term III"])
            
            st.write("Enter Marks & Grades:")
            col1, col2, col3 = st.columns(3)
            with col1:
                sub1 = st.text_input("Subject 1", "Mathematics")
                mark1 = st.number_input("Mark 1", 0, 100, 75)
                grade1 = st.text_input("Grade 1", "D1")
                rem1 = st.text_input("Remark 1", "Excellent")
            with col2:
                sub2 = st.text_input("Subject 2", "English")
                mark2 = st.number_input("Mark 2", 0, 100, 80)
                grade2 = st.text_input("Grade 2", "D2")
                rem2 = st.text_input("Remark 2", "Very Good")
            with col3:
                sub3 = st.text_input("Subject 3", "Physics")
                mark3 = st.number_input("Mark 3", 0, 100, 68)
                grade3 = st.text_input("Grade 3", "C3")
                rem3 = st.text_input("Remark 3", "Good")

            marks_data = [
                (sub1, mark1, grade1, rem1),
                (sub2, mark2, grade2, rem2),
                (sub3, mark3, grade3, rem3)
            ]

            if st.button("Generate & Download PDF Report Card"):
                pdf_bytes = generate_report_card(selected_s[1], selected_s[0], selected_s[2], selected_s[3], term, marks_data)
                st.download_button(
                    label="📥 Click to Download Report Card PDF",
                    data=pdf_bytes,
                    file_name=f"{selected_s[1]}_Report_Card.pdf",
                    mime="application/pdf"
                )
        else:
            st.warning("Please register at least one student first.")

elif role == "Bursar":
    st.markdown("<h2 class='main-header'>💼 Bursar: Staff Payroll Portal</h2>", unsafe_allow_html=True)
    cursor = conn.execute("SELECT staff_id, full_name, role, base_salary FROM staff;")
    staff_list = cursor.fetchall()
    
    if staff_list:
        staff_dict = {f"{s[1]} ({s[2]})": s for s in staff_list}
        selected_staff_label = st.selectbox("Select Staff Member", list(staff_dict.keys()))
        s_data = staff_dict[selected_staff_label]
        
        st.write(f"**Staff ID:** {s_data[0]}")
        st.write(f"**Full Name:** {s_data[1]}")
        st.write(f"**Role:** {s_data[2]}")
        st.write(f"**Base Salary:** UGX {s_data[3]:,.0f}")
    else:
        st.info("No staff records found.")

else:
    st.markdown("<h2 class='main-header'>🏫 Head Teacher Executive Dashboard</h2>", unsafe_allow_html=True)
    st_count = conn.execute("SELECT COUNT(*) FROM students;").fetchone()[0]
    staff_count = conn.execute("SELECT COUNT(*) FROM staff;").fetchone()[0]
    col1, col2 = st.columns(2)
    col1.metric("Total Enrolled Students", st_count)
    col2.metric("Total Active Staff", staff_count)
