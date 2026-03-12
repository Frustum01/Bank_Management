import streamlit as st
import pandas as pd
import os
from src.utils.data_handler import get_users_df, save_user_df

def navigate_to(page):
    st.session_state.page = page
    st.rerun()

def render_create_account():
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Back"):
            navigate_to("MainMenu")
            
    st.title("Open New Account")
    st.markdown("Welcome to Apna Bank. Fill in the details below to join.")
    
    with st.container():
        with st.form("create_account_form", clear_on_submit=True):
            username = st.text_input("Username", placeholder="e.g. john_doe")
            password = st.text_input("Secure PIN (numeric only)", type="password", placeholder="e.g. 1234")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("Submit Application")
            
            if submit:
                if not username:
                    st.error("Username cannot be empty.")
                elif not password.isdigit():
                    st.error("PIN must consist of numbers only.")
                else:
                    password = int(password)
                    user = get_users_df()
                    if user is not None and username in user['username'].values:
                        st.error("Username already exists. Please choose a different one.")
                    else:
                        balance = 0
                        new_user = pd.DataFrame({
                            "username": [username],
                            "password": [password],
                            "balance": [balance]
                        })

                        if os.path.exists("user.csv"):
                            new_user.to_csv("user.csv", mode='a', index=False, header=False)
                        else:
                            new_user.to_csv("user.csv", index=False)
                        st.success("Account created successfully. Returning to Main Menu...")

def render_user_login():
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Back"):
            navigate_to("MainMenu")
            
    st.title("User Portal")
    st.markdown("Please enter your credentials to access your account.")
    
    user = get_users_df()
    if user is None:
        st.warning("Our records show no accounts currently exist. Please create an account first.")
        return

    with st.container():
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("PIN (numeric)", type="password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("Secure Login")
            
            if submit:
                if not password.isdigit():
                    st.error("Invalid credentials format.")
                else:
                    password = int(password)
                    if username in user['username'].values:
                        user_row = user[user['username'] == username]
                        actual_password = int(user_row['password'].values[0])
                        if password == actual_password:
                            st.session_state.logged_in_user = username
                            navigate_to("UserPanel")
                        else:
                            st.error("Incorrect PIN.")
                    else:
                        st.error("Account not found.")

def render_user_panel():
    username = st.session_state.logged_in_user
    if not username:
        st.error("Active session not found.")
        navigate_to("MainMenu")
        return
        
    st.title(f"Welcome back, {username}")
    st.markdown("Manage your finances securely below.")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Balance", "Deposit", "Withdraw", "Security"])
    
    user = get_users_df()
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        if user is not None:
            balance = user.loc[user['username'] == username, 'balance'].values[0]
            st.metric(label="Available Balance", value=f"₹{balance:,.2f}")
            st.caption("Your funds are protected by Apna Bank security standards.")
            
    with tab2:
        st.subheader("Add Funds")
        with st.form("deposit_form", clear_on_submit=True):
            deposit_amount = st.number_input("Amount to deposit (₹)", min_value=1, step=100)
            dep_pin = st.text_input("Enter PIN to confirm", type="password")
            submit_dep = st.form_submit_button("Process Deposit")
            
            if submit_dep:
                if not dep_pin.isdigit():
                     st.error("PIN must be numeric.")
                else:
                    dep_pin = int(dep_pin)
                    actual_password = int(user.loc[user['username'] == username, 'password'].values[0])
                    if dep_pin == actual_password:
                        user.loc[user['username'] == username, 'balance'] += deposit_amount
                        save_user_df(user)
                        st.success(f"Successfully deposited ₹{deposit_amount:,.2f}.")
                        st.rerun() 
                    else:
                        st.error("Authentication failed. Incorrect PIN.")

    with tab3:
        st.subheader("Withdraw Funds")
        with st.form("withdraw_form", clear_on_submit=True):
            withdraw_amount = st.number_input("Amount to withdraw (₹)", min_value=1, step=100)
            with_pin = st.text_input("Enter PIN to confirm", type="password")
            submit_with = st.form_submit_button("Process Withdrawal")
            
            if submit_with:
                if not with_pin.isdigit():
                    st.error("PIN must be numeric.")
                else:
                    with_pin = int(with_pin)
                    actual_password = int(user.loc[user['username'] == username, 'password'].values[0])
                    if with_pin == actual_password:
                        current_balance = user.loc[user['username'] == username, 'balance'].values[0]
                        if current_balance >= withdraw_amount:
                            user.loc[user['username'] == username, 'balance'] -= withdraw_amount
                            save_user_df(user)
                            st.success(f"Successfully withdrew ₹{withdraw_amount:,.2f}.")
                            st.rerun()
                        else:
                            st.error(f"Insufficient funds. Available balance: ₹{current_balance:,.2f}")
                    else:
                        st.error("Authentication failed. Incorrect PIN.")

    with tab4:
        st.subheader("Update Credentials")
        with st.form("change_pass_form", clear_on_submit=True):
            new_password = st.text_input("Enter New PIN (numeric only)", type="password")
            confirm_password = st.text_input("Confirm New PIN", type="password")
            submit_pass = st.form_submit_button("Update PIN")
            
            if submit_pass:
                if not new_password.isdigit() or not confirm_password.isdigit():
                    st.error("PINs must be numeric.")
                elif new_password != confirm_password:
                    st.error("PINs do not match.")
                else:
                    new_password = int(new_password)
                    user.loc[user['username'] == username, 'password'] = new_password
                    save_user_df(user)
                    st.success("Security credentials updated successfully.")

    st.markdown("---")
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("Logout"):
            st.session_state.logged_in_user = None
            navigate_to("MainMenu")
