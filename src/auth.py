import pandas as pd
from src.database import load_users, save_users

def login(username, password):
    users = load_users()
    user_row = users[users['username'] == username]
    if not user_row.empty:
        actual_password = str(user_row['password'].values[0])
        if str(password) == actual_password:
            return True
    return False

def admin_login(secret_key):
    # Hardcoded admin key for demonstration
    if secret_key == "admin123":
        return True
    return False

def create_account(username, password):
    users = load_users()
    if username in users['username'].values:
        return False, "Username already exists."
    
    new_user = pd.DataFrame({"username": [username], "password": [password], "balance": [0]})
    users = pd.concat([users, new_user], ignore_index=True)
    save_users(users)
    return True, "Account created successfully."

def verify_pin(username, pin):
    users = load_users()
    user_row = users[users['username'] == username]
    if not user_row.empty:
        actual_password = str(user_row['password'].values[0])
        return str(pin) == actual_password
    return False
