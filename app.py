import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Apna Bank", page_icon="🏦", layout="centered")

USER_FILE = "user.csv"

# Initialize user.csv if it doesn't exist
if not os.path.exists(USER_FILE):
    df = pd.DataFrame(columns=["username", "password", "balance"])
    df.to_csv(USER_FILE, index=False)

def load_users():
    try:
        return pd.read_csv(USER_FILE)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=["username", "password", "balance"])

def save_users(df):
    df.to_csv(USER_FILE, index=False)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'is_admin' not in st.session_state:
    st.session_state['is_admin'] = False

def login(username, password):
    users = load_users()
    user_row = users[users['username'] == username]
    if not user_row.empty:
        actual_password = str(user_row['password'].values[0])
        if str(password) == actual_password:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['is_admin'] = False
            return True
    return False

def admin_login(secret_key):
    # Hardcoded admin key for demonstration instead of face unlock
    if secret_key == "admin123":
        st.session_state['logged_in'] = True
        st.session_state['username'] = "Admin"
        st.session_state['is_admin'] = True
        return True
    return False

def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.session_state['is_admin'] = False

def create_account(username, password):
    users = load_users()
    if username in users['username'].values:
        return False, "Username already exists."
    
    new_user = pd.DataFrame({"username": [username], "password": [password], "balance": [0]})
    users = pd.concat([users, new_user], ignore_index=True)
    save_users(users)
    return True, "Account created successfully."

# --- UI ---

st.title("🏦 Apna Bank Management System")

if not st.session_state['logged_in']:
    tab1, tab2, tab3 = st.tabs(["User Login", "Admin Login", "Create Account"])
    
    with tab1:
        st.subheader("Login to your account")
        l_user = st.text_input("Username", key="l_user")
        l_pass = st.text_input("Password", type="password", key="l_pass")
        if st.button("Login"):
            if login(l_user, l_pass):
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
else:
    # Logged in UI
    st.sidebar.title(f"Welcome, {st.session_state['username']}!")
    if st.sidebar.button("Logout"):
        logout()
        st.rerun()
        
    if st.session_state['is_admin']:
        st.header("Admin Dashboard")
        st.subheader("All Users")
        users = load_users()
        st.dataframe(users)
    else:
        st.header("User Dashboard")
        users = load_users()
        current_username = st.session_state['username']
        user_balance = users.loc[users['username'] == current_username, 'balance'].values[0]
        st.metric("Current Balance", f"₹{user_balance}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Deposit")
            dep_amount = st.number_input("Amount to deposit", min_value=1, step=100)
            dep_pin = st.text_input("Enter PIN to confirm", type="password", key="dep_pin")
            if st.button("Deposit"):
                actual_pass = str(users.loc[users['username'] == current_username, 'password'].values[0])
                if dep_pin == actual_pass:
                    users.loc[users['username'] == current_username, 'balance'] += dep_amount
                    save_users(users)
                    st.success(f"Deposited ₹{dep_amount} successfully.")
                    st.rerun()
                else:
                    st.error("Incorrect PIN.")
                    
        with col2:
            st.subheader("Withdraw")
            with_amount = st.number_input("Amount to withdraw", min_value=1, step=100)
            with_pin = st.text_input("Enter PIN to confirm", type="password", key="with_pin")
            if st.button("Withdraw"):
                actual_pass = str(users.loc[users['username'] == current_username, 'password'].values[0])
                if with_pin == actual_pass:
                    if user_balance >= with_amount:
                        users.loc[users['username'] == current_username, 'balance'] -= with_amount
                        save_users(users)
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
                users.loc[users['username'] == current_username, 'password'] = new_pass
                save_users(users)
                st.success("Password changed successfully.")
            else:
                st.warning("Password cannot be empty.")
