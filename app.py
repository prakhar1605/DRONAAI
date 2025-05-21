import streamlit as st
from utils import save_user_data, translate_to_hindi
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="🧠 Drona AI",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "user_authenticated" not in st.session_state:
    st.session_state["user_authenticated"] = False

def inject_css():
    st.markdown(
        """
        <style>
            body {
                background-color: #f5f7fa;
                color: #333333;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .plan-card {
                background: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                color: black;
            }
            .plan-title {
                color: #4b6cb7;
                font-weight: bold;
            }
            .plan-content {
                font-size: 1rem;
            }
        </style>
        """, 
        unsafe_allow_html=True
    )

def animated_header():
    st.markdown(
        """
        <div style="text-align: center;">
            <h1 style="color: #4b6cb7;">🧠 Drona AI</h1>
            <p>Your AI-Powered Educational Companion for Clarity and Learning</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

def signup_or_signin_page():
    st.markdown("## 🔑 Sign Up / Sign In")
    
    phone_number = st.text_input("📱 Enter your phone number", key="phone")
    user_name = st.text_input("📝 Enter your name (for signup)", key="username")
    exam_preparation = st.selectbox("🎯 Exam Preparation", ["JEE", "NEET", "UPSC", "Other"], index=0, key="exam")
    
    if st.button("✅ Continue"):
        if phone_number.strip():
            st.session_state["user_authenticated"] = True
            st.session_state["user_name"] = user_name
            st.session_state["phone_number"] = phone_number
            st.session_state["exam_preparation"] = exam_preparation
            save_user_data(phone_number, user_name, exam_preparation)
            st.experimental_rerun()
        else:
            st.error("Please enter your phone number to proceed.")

def detailed_study_plan(subjects, total_hours, exam):
    subject_list = [s.strip() for s in subjects.split(",") if s.strip() != ""]
    if not subject_list:
        return "No subjects provided. Please input at least one subject."
    
    num_subjects = len(subject_list)
    allocated_hours = total_hours // num_subjects
    remainder = total_hours % num_subjects
    
    plan_lines = []
    plan_lines.append(f"Study Plan for {exam}:")
    for i, subject in enumerate(subject_list):
        hours_for_subject = allocated_hours + (1 if i < remainder else 0)
        plan_lines.append(f"- {subject}: {hours_for_subject} hour(s)")
    plan_lines.append("✅ Stay consistent and revise thoroughly!")
    return "\n".join(plan_lines)

def study_plan_generator():
    st.markdown(f"## 📚 Study Plan for {st.session_state.get('exam_preparation', 'Your Exam')}")
    
    subjects = st.text_input(
        "**Enter subjects to focus on** (comma separated)", 
        placeholder="e.g. Physics, Organic Chemistry", 
        key="subjects"
    )
    hours = st.slider("**How many hours can you study today?** ⏳", 1, 12, 5, key="hours")
    lang = st.radio("**Choose your language**", ["English 🇬🇧", "Hindi 🇮🇳"], horizontal=True, key="language")
    
    if st.button("✨ Generate Study Plan", key="generate_plan"):
        with st.spinner("🧠 Creating your personalized plan..."):
            plan = detailed_study_plan(subjects, hours, st.session_state.get("exam_preparation", "Other"))
            if lang == "Hindi 🇮🇳":
                plan = translate_to_hindi(plan)
            
            st.markdown(f"""
            <div class="plan-card">
                <h3 class="plan-title">📅 Your Study Plan</h3>
                <div class="plan-content">
                    {plan.replace('\n', '<br>')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.download_button(
                label="📥 Download Plan",
                data=plan,
                file_name=f"{st.session_state.get('exam_preparation')}_study_plan.txt",
                mime="text/plain"
            )

def app_footer():
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center;">
            <p>Made with ❤️ by Drona AI</p>
            <p>Stay consistent. You're doing great! 💪</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

def main():
    inject_css()
    animated_header()
    
    if not st.session_state.user_authenticated:
        signup_or_signin_page()
    else:
        st.title(f"Welcome, {st.session_state.get('user_name', 'Student')}! 🎓")
        st.write("Your personalized study plan starts here.")
        study_plan_generator()
    
    app_footer()

if __name__ == "__main__":
    main()