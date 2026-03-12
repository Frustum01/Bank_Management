import streamlit as st
from src.auth import login, admin_login, create_account, verify_pin
from src.database import load_users, get_user_balance, update_balance, update_password

st.set_page_config(page_title="Apna Bank", page_icon="🏦", layout="centered")

def init_session():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    if 'is_admin' not in st.session_state:
        st.session_state['is_admin'] = False

def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.session_state['is_admin'] = False

# --- UI Methods ---
def show_login_page():
    st.title("🏦 Apna Bank Management System")
    tab1, tab2, tab3 = st.tabs(["User Login", "Admin Login", "Create Account"])
    
    with tab1:
        st.subheader("Login to your account")
        l_user = st.text_input("Username", key="l_user")
        l_pass = st.text_input("Password", type="password", key="l_pass")
        if st.button("Login"):
            if login(l_user, l_pass):
                st.session_state['logged_in'] = True
                st.session_state['username'] = l_user
                st.session_state['is_admin'] = False
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password.")
                
    with tab2:
        st.subheader("Admin Access")
        st.info("Face unlock replaced with secret key ('admin123') for web version.")
        a_key = st.text_input("Admin Secret Key", type="password")
        if st.button("Admin Login"):
            if admin_login(a_key):
                st.session_state['logged_in'] = True
                st.session_state['username'] = "Admin"
                st.session_state['is_admin'] = True
                st.success("Admin login successful!")
                st.rerun()
            else:
                st.error("Invalid Admin Key.")
                
    with tab3:
        st.subheader("Open a new account")
        c_user = st.text_input("Choose Username", key="c_user")
        c_pass = st.text_input("Choose Password", type="password", key="c_pass")
        if st.button("Create Account"):
            if c_user and c_pass:
                success, msg = create_account(c_user, c_pass)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                st.warning("Please fill all fields.")

def show_admin_dashboard():
    st.header("Admin Dashboard")
    st.subheader("All Users")
    users = load_users()
    st.dataframe(users)

def show_user_dashboard():
    current_username = st.session_state['username']
    user_balance = get_user_balance(current_username)
    
    st.header("User Dashboard")
    st.metric("Current Balance", f"₹{user_balance}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Deposit")
        dep_amount = st.number_input("Amount to deposit", min_value=1, step=100)
        dep_pin = st.text_input("Enter PIN to confirm", type="password", key="dep_pin")
        if st.button("Deposit"):
            if verify_pin(current_username, dep_pin):
                update_balance(current_username, user_balance + dep_amount)
                st.success(f"Deposited ₹{dep_amount} successfully.")
                st.rerun()
            else:
                st.error("Incorrect PIN.")
                
    with col2:
        st.subheader("Withdraw")
        with_amount = st.number_input("Amount to withdraw", min_value=1, step=100)
        with_pin = st.text_input("Enter PIN to confirm", type="password", key="with_pin")
        if st.button("Withdraw"):
            if verify_pin(current_username, with_pin):
                if user_balance >= with_amount:
                    update_balance(current_username, user_balance - with_amount)
                    st.success(f"Withdrawn ₹{with_amount} successfully.")
                    st.rerun()
                else:
                    st.error("Insufficient balance.")
            else:
                st.error("Incorrect PIN.")
                
    st.divider()
    st.subheader("Change Password")
    new_pass = st.text_input("New Password", type="password")
    if st.button("Change Password"):
        if new_pass:
            update_password(current_username, new_pass)
            st.success("Password changed successfully.")
        else:
            st.warning("Password cannot be empty.")

# --- Main App Execution ---
init_session()

if not st.session_state['logged_in']:
    show_login_page()
else:
    st.sidebar.title(f"Welcome, {st.session_state['username']}!")
    if st.sidebar.button("Logout"):
        logout()
        st.rerun()
        
    if st.session_state['is_admin']:
        show_admin_dashboard()
    else:
        show_user_dashboard()
