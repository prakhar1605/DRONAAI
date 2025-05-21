import streamlit as st
import pandas as pd
import requests

# Google Sheets API details (adjust accordingly)
SHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"

# Function to store user signup info
def save_user_info(name, phone, exam):
    user_data = {"Name": name, "Phone": phone, "Exam": exam}
    # Store in Google Sheets (adjust API setup)
    df = pd.DataFrame([user_data])
    df.to_csv("users.csv", mode="a", header=False, index=False)  # Temporary storage
    return True

# Signup Page UI
st.title("Sign Up for Drona AI")

name = st.text_input("Enter Your Name")
phone = st.text_input("Enter Your Phone Number")
exam = st.selectbox("Select Your Exam", ["JEE", "NEET", "Other"])

if st.button("Sign Up"):
    if name and phone:
        save_user_info(name, phone, exam)
        st.success("Signup Successful! Redirecting...")
        st.experimental_set_query_params(page="dashboard")  # Redirects to the MVP
    else:
        st.error("Please fill all required fields.")
