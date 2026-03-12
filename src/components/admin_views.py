import streamlit as st
import os
import cv2
import numpy as np
from PIL import Image
from src.utils.data_handler import get_users_df, append_to_training

def navigate_to(page):
    st.session_state.page = page
    st.rerun()

def render_admin_login():
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Back"):
            navigate_to("MainMenu")
            
    st.title("Admin Face Verification")
    st.markdown("Please position your face clearly in the camera view to authenticate.")
    
    if not os.path.exists("trainer.yml"):
        st.error("Trainer file ('trainer.yml') not found. Admin login requires a pre-trained face model.")
        return

    camera_image = st.camera_input("Scan Face")
    
    if camera_image is not None:
        try:
            image = Image.open(camera_image)
            img_array = np.array(image)
            
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array

            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.read("trainer.yml")
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            faces = face_cascade.detectMultiScale(gray, 1.2, 5)
            
            if len(faces) == 0:
                st.warning("No face detected. Please try again.")
            else:
                unlocked = False
                for (x, y, w, h) in faces:
                    id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])
                    if confidence < 50:
                        unlocked = True
                        break
                
                if unlocked:
                    st.success("Identity Verified. Redirecting...")
                    st.session_state.is_admin = True
                    navigate_to("AdminPanel")
                else:
                    st.error("Unknown face. Access denied.")
        except Exception as e:
            st.error(f"Error processing image: {e}")

def render_admin_panel():
    st.title("Admin Dashboard")
    
    if not st.session_state.is_admin:
        st.error("Unauthorized access.")
        return
        
    tab1, tab2 = st.tabs(["Manage Users", "Train New Admin"])
    
    with tab1:
        st.subheader("Registered Users Directory")
        user = get_users_df()
        if user is None:
            st.info("No users found in the system.")
        else:
            display_df = user.copy()
            if 'password' in display_df.columns:
                display_df['password'] = '********'
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
    with tab2:
        st.subheader("Register a New Admin Face")
        st.info("To add a new authorized face, capture at least 5 photos of the person from different angles.")
        
        col_cam, col_info = st.columns([2, 1])
        
        with col_cam:
            new_face_img = st.camera_input("Take Training Photo", key="train_cam")
            if new_face_img is not None:
                img = Image.open(new_face_img)
                st.session_state.training_images.append(np.array(img))
                st.success(f"Captured photo #{len(st.session_state.training_images)}")
                
        with col_info:
            st.metric("Photos Captured", len(st.session_state.training_images))
            if len(st.session_state.training_images) > 0:
                if st.button("Clear Photos"):
                    st.session_state.training_images = []
                    st.rerun()
                    
            if len(st.session_state.training_images) >= 5:
                st.markdown("---")
                if st.button("Train Face Model Now", type="primary"):
                    with st.spinner("Processing images and updating model..."):
                        extracted_faces = append_to_training(st.session_state.training_images)
                        if extracted_faces > 0:
                            st.success(f"Successfully trained the model with {extracted_faces} detected faces.")
                            st.session_state.training_images = []
                        else:
                            st.error("No clear faces could be detected in the captured photos. Please try again.")

    st.markdown("---")
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("Secure Logout"):
            st.session_state.is_admin = False
            st.session_state.training_images = []
            navigate_to("MainMenu")
