🧘‍♂️ Project Title:
Yoga Pose Detection and Feedback System

Project Demo Video:
https://drive.google.com/drive/folders/1OvVnNsf80hoaLNS3UW6JZ21vl7OZ8Hfg?usp=drive_link

📌 Project Summary:
The Yoga Pose App is a real-time posture analysis tool designed for yoga practitioners to improve pose accuracy, prevent injuries, and track personal progress. By integrating machine learning with computer vision, the app detects body keypoints using a webcam, evaluates user poses, and provides visual, audio, and text-based feedback. Built with a desktop-friendly GUI using Tkinter, it ensures accessibility even without an internet connection.

This tool empowers users to perform yoga safely and effectively at home by simulating expert guidance through AI-based feedback.

🌟 Key Features:
1. 👤 User Authentication & Personalization
Login/Signup system using Flask with password hashing (Flask-Bcrypt).

User dashboard with profile info and personalized streak tracking.

2. 📸 Real-Time Pose Detection
Live video capture from webcam using OpenCV.

Pose keypoint extraction using TensorFlow MoveNet model.

3. 🧠 Pose Evaluation & Feedback
Pose classification model to detect correct/incorrect poses.

Calculates joint angles using trigonometric functions (math module).

Highlights joints with:

✅ Green lines for correct posture

❌ Red lines for incorrect posture

4. 🔊 Multi-Modal Feedback System
Text Feedback: Instant corrections displayed on screen.

Voice Feedback: Audio instructions via pyttsx3.

Visual Feedback: Real-time overlay of joint keypoints and lines.

5. 📅 Progress Tracking
Tracks daily yoga activity using streak logic (datetime module).

Session logs maintained via backend (Flask_SQLAlchemy).

6. 🚨 Guidelines & Safety
Splash screen shows instructions and disclaimers.

Alerts users to avoid certain poses if they have specific injuries.

🛠️ Technologies & Libraries Used:
🖥️ Frontend (GUI & Camera)
Library	Purpose
tkinter	GUI framework for the desktop app
Pillow	Displays images inside the GUI
OpenCV	Captures webcam feed and processes frames
pyttsx3	Converts feedback text into speech
threading	Ensures GUI remains responsive during processing
math	Calculates angles between body joints
time, datetime	Delay handling & streak tracking
os, json, subprocess	File handling, config management

🧠 Machine Learning / Pose Estimation
Library	Role
TensorFlow	Loads MoveNet model for keypoint extraction
movenet	Extracts 17 body keypoints per frame
NumPy	Handles numerical & vector calculations
angle_calculator	Module to compute joint angles
preprocess.py	Normalizes pose data before classification
feedback.py	Generates appropriate feedback messages

🌐 Backend (User & Session Data)
Technology	Purpose
Flask	Web framework for APIs
Flask_SQLAlchemy	ORM to manage user data
Flask_Bcrypt	Hashes passwords securely
Flask_CORS	Enables frontend-backend communication
requests	Interacts with backend from frontend logic

🏫 Developed At:
Sinhgad College of Engineering
Department of Information Technology
Academic Year: 2024–25
