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
role = st.sidebar.selectbox("Select Portal", ["Director of Studies (DOS)", "Bursar", "Head Teacher"], key="sidebar_role_select")

conn = get_connection()

if role == "Director of Studies (DOS)":
    st.markdown("<h2 class='main-header'>📊 Director of Studies: Academic & Registration Portal</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📝 Register New Student", "📋 Student Directory", "🎓 Class Bulk Report Cards"])
    
    with tab1:
        st.subheader("New Student Registration")
        with st.form("reg_form"):
            col1, col2 = st.columns(2)
            with col1:
                s_id = st.text_input("Unique Student ID (e.g., SMHS-002)")
                fullname = st.text_input("Full Name")
                level = st.selectbox("Level", ["O-Level", "A-Level"], key="reg_level")
            with col2:
                class_name = st.selectbox("Class", ["S.1", "S.2", "S.3", "S.4", "S.5", "S.6"], key="reg_class")
                stream = st.selectbox("Stream", ["East", "West", "North", "South"], key="reg_stream")
                boarding = st.selectbox("Boarding Status", ["Boarding", "Day"], key="reg_boarding")
            
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
        st.subheader("Class-Wide Bulk Report Card Printing (O-Level)")
        
        # Locked-in working class selection with unique keys
        selected_class = st.selectbox("Select Working Class", ["S.1", "S.2", "S.3", "S.4"], key="bulk_class_select")
        term = st.selectbox("Select Term", ["Term I", "Term II", "Term III"], key="bulk_term_select")
        
        # Fetch students belonging to the selected class
        cursor = conn.execute("SELECT student_id, full_name, class_name, stream FROM students WHERE class_name = ?;", (selected_class,))
        class_students = cursor.fetchall()
        
        if class_students:
            st.info(f"Found {len(class_students)} student(s) in {selected_class}. Ready for bulk generation.")
            
            if st.button(f"Generate All Report Cards for {selected_class}", key="gen_bulk_btn"):
                # Official O-Level Subjects structure (with multi-papers for sciences/arts)
                sample_subjects = [
                    ("Mathematics", "P1"), ("English", "P1"), 
                    ("Biology", "P1"), ("Biology", "P2"),
                    ("Chemistry", "P1"), ("Chemistry", "P2"),
                    ("Physics", "P1"), ("Physics", "P2"),
                    ("History", "P1"), ("Geography", "P1"),
                    ("Agriculture", "P1"), ("Agriculture", "P2"),
                    ("Literature", "P1"), ("Luganda", "P1"),
                    ("Entrepreneurship", "P1"), ("Music", "P1"),
                    ("Art and Design", "P1"), ("Art and Design", "P2"),
                    ("Kiswahili", "P1")
                ]
                
                marks_data = [(sub, paper, 75, "D1", "Excellent") for sub, paper in sample_subjects]
                
                st.success(f"Successfully generated report cards for all {len(class_students)} students in {selected_class}!")
                
                # Unique key prefix for each loop download button
                for s in class_students:
                    pdf_bytes = generate_report_card(s[1], s[0], s[2], s[3], term, marks_data)
                    st.download_button(
                        label=f"Download Report: {s[1]} ({s[0]})",
                        data=pdf_bytes,
                        file_name=f"{s[1]}_{selected_class}_Report.pdf",
                        mime="application/pdf",
                        key=f"dl_btn_{s[0]}"
                    )
        else:
            st.warning(f"No students found registered under class {selected_class}. Register students in this class first.")

elif role == "Bursar":
    st.markdown("<h2 class='main-header'>💼 Bursar: Staff Payroll Portal</h2>", unsafe_allow_html=True)
    cursor = conn.execute("SELECT staff_id, full_name, role, base_salary FROM staff;")
    staff_list = cursor.fetchall()
    
    if staff_list:
        staff_dict = {f"{s[1]} ({s[2]})": s for s in staff_list}
        selected_staff_label = st.selectbox("Select Staff Member", list(staff_dict.keys()), key="bursar_staff_select")
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
