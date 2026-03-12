import os
import pandas as pd
import numpy as np
import cv2
from PIL import Image

def get_users_df():
    """Retrieve users from CSV."""
    if not os.path.exists("user.csv"):
        return None
    return pd.read_csv("user.csv")

def save_user_df(df):
    """Save users dataframe to CSV."""
    df.to_csv("user.csv", index=False)

def append_to_training(images):
    """
    Takes a list of images (NumPy arrays), extracts faces, 
    saves them to a dataset directory, and retrains trainer.yml
    """
    if not os.path.exists("dataset"):
        os.makedirs("dataset")
        
    face_id = 1 # Simplified ID management for Admin
    count = 0
    while os.path.exists(f"dataset/User.{face_id}.{count}.jpg"):
        count += 1
        
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    saved_count = 0
    for img_data in images:
        gray = img_data
        if len(gray.shape) == 3:
             gray = cv2.cvtColor(gray, cv2.COLOR_RGB2GRAY)
             
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.imwrite(f"dataset/User.{face_id}.{count}.jpg", gray[y:y+h,x:x+w])
            count += 1
            saved_count += 1
            
    # Retrain model
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    imagePaths = [os.path.join("dataset", f) for f in os.listdir("dataset")]
    faceSamples = []
    ids = []

    for imagePath in imagePaths:
        try:
            PIL_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img,'uint8')
            
            id_str = os.path.split(imagePath)[-1].split(".")[1]
            id = int(id_str)
            
            faces = face_cascade.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)
        except Exception:
            continue
            
    if faceSamples:
        recognizer.train(faceSamples, np.array(ids))
        recognizer.write('trainer.yml') 
    
    return saved_count
