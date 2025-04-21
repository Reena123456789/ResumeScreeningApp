import streamlit as st
import register  
import login
import resume

# Initialize session state variables if they do not exist
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Sidebar Navigation with Styled Text and Icons
st.sidebar.markdown("## 🌟 Want a **Good Resume?**")
st.sidebar.markdown("### ✅ It's a Correct Application")
st.sidebar.markdown("### 🚀 Let's Get Started!")


if st.session_state.authenticated:
    # Show user details and logout option when logged in
    st.sidebar.success(f"👤 **Logged in as {st.session_state.username}**")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()
    page = "Home"  # Redirect to Home automatically after login
else:
    # Show login and register options when not logged in
    st.sidebar.markdown("---")  # Divider
    page = st.sidebar.radio("📌 **Navigation**", ["🔑 Login", "📝 Register"])

# Page Routing Logic
if page == "🔑 Login":
    login.login()

elif page == "📝 Register":
    register.register()  
    

elif page == "Home":
    if st.session_state.authenticated:
        resume.main()
    else:
        st.warning("⚠️ Please login first!")
