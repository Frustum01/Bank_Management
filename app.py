import streamlit as st
import os
from src.theme import apply_corporate_theme
from src.components.admin_views import render_admin_login, render_admin_panel
from src.components.user_views import render_create_account, render_user_login, render_user_panel

# Setup page (No emojis, corporate title)
st.set_page_config(page_title="Apna Bank Portal", layout="centered")

# Apply clean custom styling
apply_corporate_theme()

# --- State Management ---
if 'page' not in st.session_state:
    st.session_state.page = "MainMenu"
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'training_images' not in st.session_state:
    st.session_state.training_images = []

def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# --- Main App Logic / Router ---
def main():
    if st.session_state.page == "MainMenu":
        st.markdown("<h1 style='text-align: center; font-size: 3rem;'>Apna Bank</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #4B5563; margin-bottom: 3rem;'>Secure, Fast, and Reliable Banking Solutions.</p>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Admin Portal", use_container_width=True):
                navigate_to("AdminLogin")
        with col2:
            if st.button("User Login", use_container_width=True):
                navigate_to("UserLogin")
        with col3:
            if st.button("Open Account", use_container_width=True):
                navigate_to("CreateAccount")
                
    elif st.session_state.page == "AdminLogin":
        render_admin_login()
    elif st.session_state.page == "AdminPanel":
        render_admin_panel()
    elif st.session_state.page == "UserLogin":
        render_user_login()
    elif st.session_state.page == "CreateAccount":
        render_create_account()
    elif st.session_state.page == "UserPanel":
        render_user_panel()

if __name__ == "__main__":
    main()
