import pandas as pd
import os

# Updated to reflect new relative path from where app.py will run (Bank_Management root)
USER_FILE = "data/user.csv"

def init_db():
    if not os.path.exists(USER_FILE):
        # Ensure data dir exists
        os.makedirs(os.path.dirname(USER_FILE), exist_ok=True)
        df = pd.DataFrame(columns=["username", "password", "balance"])
        df.to_csv(USER_FILE, index=False)

def load_users():
    init_db()
    try:
        return pd.read_csv(USER_FILE)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=["username", "password", "balance"])

def save_users(df):
    df.to_csv(USER_FILE, index=False)

def get_user_balance(username):
    users = load_users()
    return users.loc[users['username'] == username, 'balance'].values[0]

def update_balance(username, new_balance):
    users = load_users()
    users.loc[users['username'] == username, 'balance'] = new_balance
    save_users(users)

def update_password(username, new_password):
    users = load_users()
    users.loc[users['username'] == username, 'password'] = new_password
    save_users(users)
