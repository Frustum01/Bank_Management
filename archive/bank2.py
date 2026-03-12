import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import os

def exit():
    quit()

def withdraw(username, password):
     amount = int(input("Enter the amount to withdraw: "))
     pin = int(input("Enter the pin: "))
     if pin == password:
        user = pd.read_csv("user.csv")
        current_balance = user.loc[user['username'] == username, 'balance'].values[0]
        if current_balance >= amount:
            user.loc[user['username'] == username, 'balance'] -= amount
            user.to_csv("user.csv", index=False)
            print("Withdrawal successful.")
        else:
            print("Insufficient balance.")
     else:
        print("Incorrect PIN.")

def admin_face_unlock():
    import cv2
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer.yml")

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print(" Error: Could not open webcam.")
        return

    print(" Starting face recognition... Press 'q' to quit.")
    unlocked = False

    while True:
        ret, img = cam.read()
        if not ret:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            if confidence < 50:
                print(" Admin recognized! Access granted.")
                unlocked = True
                break
            else:
                print(f" Unknown face (confidence: {round(confidence, 2)})")

        if unlocked:
            break

        cv2.imshow('Face Unlock', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

    if unlocked:
        admin_section()  


def admin_section():
    print("\n--- Admin Panel ---")
    print("1. View All Users")
    print("2. Log Out")

    choice = input("Enter choice: ")
    if choice == "1":
        user = pd.read_csv("user.csv")
        print(user)
        menu()
    elif choice == "2":
        print("Loging Out.....")
        return


def deposite(username, password):
    amount = int(input("Enter the amount you want to deposit: "))
    pin = int(input("Enter the pin: "))
    
    if pin == password:
        user = pd.read_csv("user.csv")
        user.loc[user['username'] == username, 'balance'] += amount
        user.to_csv("user.csv", index=False)
        print("Amount deposited successfully.")
    else:
        print("Incorrect password.")

def createaccount():
    username = input("Enter Username: ")
    password = int(input("Enter Password: "))
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
    print("Account created successfully.")

def userlogin():  
    username = input("Enter the username: ")
    password = int(input("Enter the password: "))

    user = pd.read_csv("user.csv")
    if username in user['username'].values:
        user_row = user[user['username'] == username]
        actual_password = int(user_row['password'].values[0])
        if password == actual_password:
            index = user.index[user['username'] == username][0]
            print("Login successful.\n")
            usermenu(username, password)
        else:
            print("Incorrect password.")
    else:
        print("Incorrect username.")

def menu():
    while True:
        print("\n----- Welcome to the Apna Bank  ------")
        print("1. Admin Login (Face Unlock)")
        print("2. User Login")
        print("3. Create Account")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            admin_face_unlock()
        elif choice == "2":
            userlogin()
        elif choice == "3":
            createaccount()
        elif choice == "4":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


def checkbalance(username):
    user = pd.read_csv("user.csv")
    balance = user.loc[user['username'] == username, 'balance'].values[0]
    print(f"{username}, your balance is: ₹{balance}")

def changepassword(username):
    new_pass=int(input("Enter New Password"))
    user = pd.read_csv("user.csv")
    user.loc[user['username'] == username, 'password'] = new_pass
    user.to_csv("user.csv", index=False)
    print("Password changed successfully.")
     


def transfertoother(username):
    print(f"{username}, transfer feature coming soon.")

def usermenu(username,password):
    while True:
        print(f"\n--- Welcome, {username}! ---")
        print("1] Check Balance")
        print("2] Deposit")
        print("3] Withdraw")
        print("4] Change Password")
        print("5] Logout")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            checkbalance(username)
        elif choice == "2":
            deposite(username, password)
        elif choice == "3":
            withdraw(username,password)
        elif choice == "4":
            changepassword(username)
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")

menu()