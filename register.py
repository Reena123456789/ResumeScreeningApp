import streamlit as st
import database
def register():
    st.title("📝 Register Here !! ")

    name = st.text_input("Full Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if not name or not username or not password or not confirm_password:
            st.error("⚠️ All fields are required!")
            return
        
        if password != confirm_password:
            st.error("Passwords do not match!")
            return

        if database.registerUser(name, username, password):
            st.toast("✅ Registration Successful! Please login.")
            st.balloons()
        else:
            st.error("❌ Username already exists!")