import streamlit as st
import database

def login():
    st.title("🔐 Login to Resume Screening App")

    username = st.text_input("Username ")
    password = st.text_input("Password ", type="password")

    if st.button("Login"):
        if database.loginUser(username, password):
            st.toast("✅ Login Successfull !!!")
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success(f" Welcome, {username}!")
            
            st.rerun()  # 🔥 Refresh UI after login
        else:
            st.error("❌ Invalid username or password!")
