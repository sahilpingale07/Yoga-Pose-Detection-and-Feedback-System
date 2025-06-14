import tkinter as tk
from tkinter import PhotoImage, Toplevel
from PIL import Image, ImageTk
import threading
from threading import Thread
import cv2
from movenet import Movenet  # Import the MoveNet class
from movenet import draw_pose
import tensorflow as tf
import pyttsx3
import time  # Add this import at the top of the file
from preprocess import preprocess_for_prediction
from tkinter import messagebox
import requests
import json
import os
from datetime import date, timedelta
import subprocess
from angle_calculator import extract_angles_from_person
tts_engine = pyttsx3.init()

from feedback import get_feedback
# Load the model in an older compatible version


angle_keys = [
    'left_elbow', 'right_elbow',
    'left_shoulder', 'right_shoulder',
    'left_hip', 'right_hip',
    'left_knee', 'right_knee',
    'neck'
]

def convert_to_angle_dict(raw_angles, angle_keys):
    """
    Convert a NumPy array of angles to a dictionary with specified keys.
    raw_angles: NumPy array of angles.
    angle_keys: List of keys for the angles.
    """
    if len(raw_angles) != len(angle_keys):
        raise ValueError("Length of raw_angles and angle_keys must match.")
    return {key: angle for key, angle in zip(angle_keys, raw_angles)}


def load_pose_model(pose_name):
    """Load the appropriate model for the given pose"""
    print(tf.__version__)
    model_path = f"./pose_models/{pose_name.lower()}/model.h5"
    try:
        model = tf.keras.models.load_model(model_path)
        
        print(f"Successfully loaded model for {pose_name}")
        return model
    except Exception as e:
        print(f"Error loading model for {pose_name}: {e}")
        return None
# Path to your local model folder (contains saved_model.pb and variables folder)
model_path = ".\movenet_thunder.tflite"  # Update this to the path of your saved model
movenet = Movenet(model_path)

# Splash Screen
def splash_screen():
    splash = tk.Tk()
    splash.title("Yoga Pose Detection")
    splash.geometry("600x400")
    splash.configure(bg="white")

    # Center the splash screen
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (600 / 2))
    y_cordinate = int((screen_height / 2) - (400 / 2))
    splash.geometry(f"600x400+{x_cordinate}+{y_cordinate}")

    # Load GIF
    gif_label = tk.Label(splash, bg="white")
    gif_label.pack(expand=True, fill="both")

    gif_image = Image.open(".\yoga_welcome.gif")  # Replace with your path
    frames = []
    try:
        while True:
            frame = gif_image.copy()
            frame = frame.resize((600, 400), Image.LANCZOS)
            frames.append(ImageTk.PhotoImage(frame))
            gif_image.seek(len(frames))
    except EOFError:
        pass

    def animate(index):
        gif_label.configure(image=frames[index])
        splash.after(50, animate, (index + 1) % len(frames))  # Reduced delay to 50ms

    total_duration = len(frames) * 50  # Adjusted to match the new frame interval

    animate(0)
    splash.after(total_duration, lambda: [splash.destroy(), login_window()])
    splash.mainloop()

SERVER_URL = "http://127.0.0.1:5001"

# ** Start the Flask Backend Automatically **
def start_backend():
    process = subprocess.Popen(["python", "backend.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3)  # Give some time for the server to start
    return process
# ** Start Backend Before Launching GUI **
backend_process = start_backend()


# Main Login Window
def login_window():
    root = tk.Tk()
    root.title("Login Window")
    root.geometry("600x400")
    root.configure(bg="#2e2e3e")
    root.resizable(False, False)

    # Center the splash screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (600 / 2))
    y_cordinate = int((screen_height / 2) - (400 / 2))
    root.geometry(f"600x400+{x_cordinate}+{y_cordinate}")

    # Load Image
    image_path = ".\yoga_logo.jpg"  # Replace with the actual image path
    bg_image = Image.open(image_path)
    bg_image = bg_image.resize((250, 250), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Place Image on Left Side
    image_label = tk.Label(root, image=bg_photo)
    image_label.place(x=30, y=80)

    # Login Form UI
    tk.Label(root, text="Login", font=("Arial", 16, "bold"), fg="white", bg="#2e2e3e").place(x=400, y=50)

    tk.Label(root, text="User Name:", font=("Arial", 12), fg="white", bg="#2e2e3e").place(x=310, y=120)
    entry_username = tk.Entry(root, width=25, font=("Arial", 12))
    entry_username.place(x=310, y=150)

    tk.Label(root, text="Password:", font=("Arial", 12), fg="white", bg="#2e2e3e").place(x=310, y=185)
    entry_password = tk.Entry(root, width=25, font=("Arial", 12), show="*")
    entry_password.place(x=310, y=215)

    # Function to handle login
    def login(username, password):
        if not username or not password:
            messagebox.showerror("Error", "All fields are required")
            return

        response = requests.post("http://127.0.0.1:5001/login", json={"username": username, "password": password})
        data = response.json()

        if data["status"] == "success":
            messagebox.showinfo("Success", "Login Successful")

            with open("current_user.json", "w") as f:
               json.dump({"username": username}, f)

            root.destroy()
            pose_selection_window()
        else:
            messagebox.showerror("Error", data["message"])

    # Login Button
    login_button = tk.Button(root, text="Log in", font=("Arial", 12), bg="blue", fg="white",
                         width=15, command=lambda: [login(entry_username.get(), entry_password.get())])
    login_button.place(x=350, y=255)

    # Signup Option
    tk.Label(root, text="Don't have an account?", font=("Arial", 10), fg="white", bg="#2e2e3e").place(x=340, y=295)
    signup_button = tk.Button(root, text="Sign up", font=("Arial", 10, "underline"), fg="blue", bg="#2e2e3e",
                          cursor="hand2", bd=0, command=lambda: [root.destroy(),open_register_window()])
    signup_button.place(x=480, y=292)

    root.mainloop()


# ** Stop Backend When GUI Closes **
backend_process.terminate() 

# Function to open registration window
def open_register_window():
    register_window = tk.Tk()
    register_window.title("Registration Form")  
    register_window.configure(bg="#2e2e3e")  

    # Make window fullscreen
    register_window.state('zoomed')  # For Windows
    register_window.attributes('-fullscreen', True)  # Alternative for Linux/Mac

    # Create a main frame with padding and centered alignment
    frame = tk.Frame(register_window, bg="#D3D3D3", padx=50, pady=50, bd=5, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=800, height=500)  

    # Title Label
    tk.Label(register_window, text="Registration Form", font=("Arial", 20, "bold"), fg="white", bg="#2e2e3e").pack(pady=20)

    # Styling for labels
    label_style = {"font": ("Arial", 14, "bold"), "bg": "#D3D3D3"}

    # Input fields with labels
    tk.Label(frame, text="Enter Name", **label_style).grid(row=0, column=0, sticky="w", pady=10, padx=20)
    entry_name = tk.Entry(frame, width=40, font=("Arial", 12))
    entry_name.grid(row=0, column=1, pady=10, padx=20)

    tk.Label(frame, text="Age", **label_style).grid(row=1, column=0, sticky="w", pady=10, padx=20)
    entry_age = tk.Entry(frame, width=40, font=("Arial", 12))
    entry_age.grid(row=1, column=1, pady=10, padx=20)

    tk.Label(frame, text="Gender", **label_style).grid(row=2, column=0, sticky="w", pady=10, padx=20)
    gender_var = tk.StringVar(value="Male")
    gender_frame = tk.Frame(frame, bg="#D3D3D3")
    gender_frame.grid(row=2, column=1, pady=10, padx=20, sticky="w")
    tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male", bg="#D3D3D3", font=("Arial", 12)).pack(side="left", padx=10)
    tk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female", bg="#D3D3D3", font=("Arial", 12)).pack(side="left", padx=10)
    tk.Radiobutton(gender_frame, text="Others", variable=gender_var, value="Others", bg="#D3D3D3", font=("Arial", 12)).pack(side="left", padx=10)

    tk.Label(frame, text="Username", **label_style).grid(row=3, column=0, sticky="w", pady=10, padx=20)
    entry_username_reg = tk.Entry(frame, width=40, font=("Arial", 12))
    entry_username_reg.grid(row=3, column=1, pady=10, padx=20)

    tk.Label(frame, text="Password", **label_style).grid(row=4, column=0, sticky="w", pady=10, padx=20)
    entry_password_reg = tk.Entry(frame, width=40, show="*", font=("Arial", 12))
    entry_password_reg.grid(row=4, column=1, pady=10, padx=20)

    tk.Label(frame, text="Injuries", **label_style).grid(row=5, column=0, sticky="w", pady=10, padx=20)
    entry_injuries = tk.Entry(frame, width=40, font=("Arial", 12))
    entry_injuries.grid(row=5, column=1, pady=10, padx=20)

    tk.Label(frame, text="Disabilities", **label_style).grid(row=6, column=0, sticky="w", pady=10, padx=20)
    entry_disabilities = tk.Entry(frame, width=40, font=("Arial", 12))
    entry_disabilities.grid(row=6, column=1, pady=10, padx=20)

    # Function to handle registration
    def register_user():
        user_data = {
            "name": entry_name.get(),
            "age": entry_age.get(),
            "gender": gender_var.get(),
            "username": entry_username_reg.get(),
            "password": entry_password_reg.get(),
            "injuries": entry_injuries.get(),
            "disabilities": entry_disabilities.get(),
        }
        
        response = requests.post(f"{SERVER_URL}/register", json=user_data)
        data = response.json()

        if data["status"] == "success":
            username = user_data["username"]

        # ✅ Save session info
            with open("current_user.json", "w") as f:
                json.dump({"username": username}, f)

        # ✅ Save user profile locally in users/<username>.json
            os.makedirs("users", exist_ok=True)
            try:
            # Fetch user data from backend (ensure complete DB-consistent record)
                user_response = requests.get(f"{SERVER_URL}/user/{username}")
                if user_response.status_code == 200:
                    full_user_data = user_response.json()
                    with open(f"users/{username}.json", "w") as f:
                         json.dump(full_user_data, f, indent=4)
                else:
                # fallback: store form data if API fails
                    with open(f"users/{username}.json", "w") as f:
                        json.dump(user_data, f, indent=4)
            except:
                with open(f"users/{username}.json", "w") as f:
                    json.dump(user_data, f, indent=4)

            messagebox.showinfo("Success", "Registration successful! Proceeding to pose selection.")
            register_window.destroy()
            pose_selection_window()
        else:
            messagebox.showerror("Error", "Registration failed!")

    # Register Button
    tk.Button(frame, text="Register", command=register_user, font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", width=15).grid(row=7, column=0, pady=20, padx=10)

    # Exit Button
    tk.Button(frame, text="Exit", command=register_window.destroy, font=("Arial", 14, "bold"), bg="#FF3B3B", fg="white", width=15).grid(row=7, column=1, pady=20, padx=10)

    register_window.mainloop()


def update_streak():
    today = str(date.today())

    try:
        with open("current_user.json", "r") as f:
            username = json.load(f)["username"]
    except FileNotFoundError:
        print("User not logged in.")
        return

    # Load or initialize streak data
    if os.path.exists("streak_data.json"):
        with open("streak_data.json", "r") as f:
            data = json.load(f)
    else:
        data = {}

    if username not in data:
        data[username] = {}

    # Mark today as completed
    data[username][today] = True

    # Save it back
    with open("streak_data.json", "w") as f:
        json.dump(data, f, indent=4)


def get_user_streak(username):
    try:
        with open("streak_data.json", "r") as f:
            all_data = json.load(f)
            user_data = all_data.get(username, {})
    except FileNotFoundError:
        user_data = {}

    # Generate past 30 days with streak flag
    today = date.today()
    streak_days = {}
    for i in range(30):
        day = today - timedelta(days=29 - i)
        day_str = day.isoformat()
        streak_days[day_str] = user_data.get(day_str, False)

    return streak_days

def draw_streak_heatmap(parent_frame):
    try:
        with open("current_user.json", "r") as f:
            username = json.load(f)["username"]
    except:
        username = None

    if not username:
        return

    streak_data = get_user_streak(username)

    canvas = tk.Canvas(parent_frame, width=480, height=120, bg="#2e2e3e", highlightthickness=0)
    canvas.pack(pady=20)
    canvas.create_text(200, 90, text="Your 30-Day Yoga Streak", fill="white", font=("Arial", 16))

    box_size = 24
    gap = 7
    today = date.today()

    for i, (day_str, did_yoga) in enumerate(streak_data.items()):
        x = (box_size + gap) * (i % 15)
        y = (box_size + gap) * (i // 15)
        color = "#4CAF50" if did_yoga else "#888484"
        canvas.create_rectangle(x, y, x + box_size, y + box_size, fill=color, outline="")


def pose_selection_window():
    global yoga_image  # Prevent garbage collection issues

    root = tk.Tk()
    root.title("Yoga Pose Selection")
    root.configure(bg="#2e2e3e")
    root.state('zoomed')

    def logout():
        root.destroy()
        login_window()  # Call your login function here

    def open_profile():
        try:
            with open("current_user.json", "r") as f:
                username = json.load(f)["username"]
            with open(f"users/{username}.json", "r") as f:
                user = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "User data not found!")
            return

        # Profile Window Setup
        profile_win = tk.Toplevel()
        profile_win.title("User Profile")
        window_width = 700
        window_height = 500
        screen_width = profile_win.winfo_screenwidth()
        screen_height = profile_win.winfo_screenheight()
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        profile_win.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        profile_win.configure(bg="#2e2e3e")

        # Main frame to divide left (info) and right (image)
        main_frame = tk.Frame(profile_win, bg="#2e2e3e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Left frame for user information
        left_frame = tk.Frame(main_frame, bg="#2e2e3e")
        left_frame.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(left_frame, text="🧘‍♂️ User Profile", font=("Arial", 20, "bold"), bg="#2e2e3e", fg="white").pack(pady=10, anchor="w")

        info_fields = [
            f"Name: {user.get('name', 'N/A')}",
            f"Username: {user.get('username', 'N/A')}",
            f"Age: {user.get('age', 'N/A')}",
            f"Gender: {user.get('gender', 'N/A')}",
            f"Injuries: {user.get('injuries', 'None')}",
            f"Disabilities: {user.get('disabilities', 'None')}",
        ]

        for info in info_fields:
            tk.Label(left_frame, text=info, font=("Arial", 14), bg="#2e2e3e", fg="white", anchor="w").pack(pady=5, anchor="w")

       # Right frame for user image
        right_frame = tk.Frame(main_frame, bg="#2e2e3e")
        right_frame.pack(side="right", fill="y", padx=10)

        try:
            # Choose image based on gender
            gender = user.get("gender", "Male").lower()
            if gender == "female":
                image_path = "./images/female-face-icon.png"
            else:
                image_path = "./images/male-face-icon.jpg"

            user_img = Image.open(image_path)   
            user_img = user_img.resize((240, 230))
            user_photo = ImageTk.PhotoImage(user_img)
            img_label = tk.Label(right_frame, image=user_photo, bg="#2e2e3e")
            img_label.image = user_photo  # keep reference
            img_label.pack(pady=10)
        except Exception as e:
            tk.Label(right_frame, text="No Image", font=("Arial", 12), bg="#2e2e3e", fg="white").pack(pady=10)

        draw_streak_heatmap(left_frame)    
            
    hamburger_btn = tk.Menubutton(
    root,
    text="☰",
    font=("Arial", 20, "bold"),
    bg="#2e2e3e",
    fg="white",
    activebackground="#3e3e4e",
    relief="flat",
    direction="below"
    )
    hamburger_btn.place(relx=0.97, rely=0.03, anchor="ne")

   # Custom font for menu items
    menu_font = ("Arial", 14, "bold")

   # Create the dropdown menu
    dropdown_menu = tk.Menu(hamburger_btn, tearoff=0, 
                        bg="#f0f0f0", 
                        fg="black", 
                        activebackground="#dcdcdc", 
                        activeforeground="black",
                        font=menu_font,
                        bd=2)

    # Add commands with extra spacing for a larger feel
    dropdown_menu.add_command(label="Profile", command=open_profile)
    dropdown_menu.add_command(label="Logout", command=logout)

    7# Attach menu to Menubutton
    hamburger_btn.config(menu=dropdown_menu)

    # Title Label
    title_label = tk.Label(
        root,
        text="Select a Yoga Pose",
        font=("Arial", 24, "bold"),
        bg="#2e2e3e",
        fg="#ffffff"
    )
    title_label.pack(pady=20)

    # Main Frame (Splits 60-40)
    main_frame = tk.Frame(root, bg="#2e2e3e")
    main_frame.pack(fill="both", expand=True)

    # Left Frame (60% width)
    left_frame = tk.Frame(main_frame, bg="#2e2e3e", width=int(root.winfo_screenwidth() * 0.6))
    left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    # Right Frame (40% width)
    right_frame = tk.Frame(main_frame, bg="#2e2e3e", width=int(root.winfo_screenwidth() * 0.4))
    right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
    
    # Load and display the yoga image
    yoga_image_path = ".\yoga_image.png"  # Ensure correct file path
    img = Image.open(yoga_image_path)  
    img = img.resize((400, 500))  
    yoga_image = ImageTk.PhotoImage(img)  # Keep reference global


    image_label = tk.Label(right_frame, image=yoga_image, bg="#2e2e3e")
    image_label.image = yoga_image  # Keep a reference to prevent garbage collection
    image_label.pack(expand=True)

    # Yoga Poses List
    poses= [
            'Adhomukhasvanasana', 'Kumbhakasana', 'Bhujangasana',
            'Natarajasana', 'Trikonasana', 'Utkatakonasana',
            'Utkatasana', 'Virabhadrasana', 'Vrksasana'
    ] 

    button_style = {
        "font": ("Arial", 14, "bold"),
        "bg": "#d3d3d3",
        "fg": "#000000",
        "activebackground": "#a9a9a9",
        "activeforeground": "#000000",
        "relief": "solid",
        "borderwidth": 2,
        "width": 20,
        "height": 2,
    }

    # Grid Layout for Buttons (2 columns)
    rows = (len(poses) + 1) // 2  # Distribute buttons evenly
    for i, pose in enumerate(poses):
        row, col = divmod(i, 2)
        btn = tk.Button(
            left_frame,
            text=pose,
            command=lambda pose=pose: [root.destroy(), show_disclaimer(pose)],
            **button_style
        )
        btn.grid(row=row, column=col, padx=10, pady=5, sticky="ew")

    # Exit Button at the bottom
    exit_btn = tk.Button(
        left_frame,
        text="Exit",
        command=root.destroy,
        font=("Arial", 14, "bold"),
        bg="#ff4d4d",
        fg="#ffffff",
        activebackground="#ff6666",
        activeforeground="#ffffff",
        relief="solid",
        borderwidth=2,
        width=6,
        height=1,
    )
    exit_btn.grid(row=rows, column=0, pady=20, sticky="")

    # Adjust row weights so buttons align properly
    for i in range(rows + 1):
        left_frame.grid_rowconfigure(i, weight=1)
    for i in range(2):  # 2 columns
        left_frame.grid_columnconfigure(i, weight=1)

    root.mainloop()
# Disclaimer/instructions window
pose_disclaimers = {
    "Utkatasana": "Instructions: (Chair Pose)\n\n"
             "1. Bend your knees as if sitting on an imaginary chair, ensuring they don’t go past your toes.\n"
             "2. Avoid straining your neck and shoulders; keep them relaxed.\n"
             "3. If you feel any pain, stop immediately.\n\n"
             "Disclaimer\n"
             "Avoid this pose if you have:- Knee injuries, Lower back pain, Ankle injuries",
    "Bhujangasana": "Instructions: (Cobra Pose)\n\n"
             "1. Do not overarch your back.\n"
             "2. Keep your shoulders relaxed.\n"
             "3. Avoid this pose if you have a back injury.\n\n"
             "Disclaimer\n"
             "Avoid this pose if you have:- Neck injuries, Back injuries",
    "Adhomukhasvanasana": "Instructions: (Downward Dog Pose)\n\n"
           "1. Keep your hands shoulder-width apart.\n"
           "2. Distribute your weight evenly between hands and feet.\n"
           "3. Avoid this pose if you have wrist or shoulder issues.\n\n"
           "Disclaimer\n"
           "Avoid this pose if you have:- Wrist injuries, Shoulder injuries",
    "Virabhadrasana": "Instructions: (Warrior Pose)\n\n"
               "1. Keep your front knee aligned with your ankle.\n"
               "2. Engage your core for balance.\n"
               "3. Avoid this pose if you have knee problems.\n\n"
               "Disclaimer\n"
               "Avoid this pose if you have:- Knee injuries, Ankle injuries",
    "Vrksasana": "Instructions: (Tree Pose)\n\n"
            "1. Focus on a fixed point to maintain balance.\n"
            "2. Avoid locking your standing knee.\n"
            "3. If you feel unstable, use a wall for support.\n\n"
            "Disclaimer\n"
            "Avoid this pose if you have:- Knee injuries, Ankle injuries",
    "Trikonasana": "Instructions: (Triangle Pose)\n\n"
                "1. Keep your legs straight but not locked.\n"
                "2. Avoid overstretching your side.\n"
                "3. If you feel dizzy, come out of the pose slowly.\n\n"
                "Disclaimer\n"
                "Avoid this pose if you have:- Neck injuries, Back injuries",
    "Kumbhakasana": "Instructions: (Half Lord of Fishes Pose)\n\n"
                "1. Sit with your back straight and twist your torso while keeping your spine elongated.\n"
                "2. Place one hand behind you for support and the other on the knee of your opposite leg.\n\n"
                "3. Breathe deeply and avoid straining your back or neck."
                "Disclaimer\n"
                "Avoid this pose if you have:- Spinal injuries, Herniated discs, Severe hip pain\n",
    "Natarajasana": "Instructions: (Dancer pose)\n\n"
                "1. Stand tall and shift your weight onto one leg while lifting the opposite leg behind you.\n"
                "2. Hold your lifted foot with the same-side hand and extend the opposite arm forward for balance.\n"
                "3. Engage your core and avoid excessive strain on your lower back."
                "Disclaimer\n"
                "Avoid this pose if you have:- Knee injuries, Ankle instability, Lower back pain\n" ,
    "Utkatakonasana": "Instructions: (Goddess Pose)\n\n"
                "1. Stand with feet wide apart and turn toes slightly outward.\n"
                "2. Lower into a squat position while keeping your back straight and knees aligned with your toes.\n"
                "3. Engage your core and avoid excessive arching in your lower back.\n\n"
                "Disclaimer\n"
                "Avoid this pose if you have:- Knee pain, Hip injuries, Lower back discomfort."                               
}

def show_disclaimer(pose):
    # Create a new Toplevel window
    disclaimer_window = tk.Tk()
    disclaimer_window.title("Disclaimer")
    disclaimer_window.geometry("600x300")
    disclaimer_window.configure(bg="#f0f0f0")  # Light grey background

    # Center the disclaimer window
    screen_width = disclaimer_window.winfo_screenwidth()
    screen_height = disclaimer_window.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (600 / 2))
    y_cordinate = int((screen_height / 2) - (300 / 2))
    disclaimer_window.geometry(f"600x300+{x_cordinate}+{y_cordinate}")

    # Add instructions and disclaimer text
    disclaimer_text = pose_disclaimers.get(pose, "No disclaimer available for this pose.")
    instructions, disclaimer = disclaimer_text.split("Disclaimer")

    # Frame for instructions
    instructions_frame = tk.Frame(disclaimer_window, bg="#f0f0f0")
    instructions_frame.pack(pady=10, padx=20, fill="x")

    instructions_label = tk.Label(
        instructions_frame,
        text=instructions.strip(),
        font=("Helvetica", 12),
        fg="black",
        bg="#f0f0f0",
        wraplength=550,
        justify="left"
    )
    instructions_label.pack(anchor="w")

    # Frame for disclaimer
    disclaimer_frame = tk.Frame(disclaimer_window, bg="#f0f0f0")
    disclaimer_frame.pack(pady=10, padx=20, fill="x")

    disclaimer_label = tk.Label(
        disclaimer_frame,
        text="Disclaimer:\n" + disclaimer.strip(),
        font=("Helvetica", 12),
        fg="red",
        bg="#f0f0f0",
        wraplength=550,
        justify="left"
    )
    disclaimer_label.pack(anchor="w")

    # Frame for buttons
    button_frame = tk.Frame(disclaimer_window, bg="#f0f0f0")
    button_frame.pack(pady=20)

    # Add "Continue" button
    continue_button = tk.Button(
        button_frame,
        text="Continue",
        font=("Helvetica", 12, "bold"),
        bg="#2196F3",  # Dark Sky Blue Color
        fg="white",
        command=lambda: [disclaimer_window.destroy(), pose_execution_window(pose)]  # Proceed to pose execution
    )
    continue_button.pack(side="left", padx=10)

    # Add "Cancel" button
    cancel_button = tk.Button(
        button_frame,
        text="Cancel",
        font=("Helvetica", 12, "bold"),
        bg="#f44336",  # Dark Red Color
        fg="white",
        command=lambda: [disclaimer_window.destroy(), pose_selection_window()]  # Close the disclaimer window
    )
    cancel_button.pack(side="left", padx=10)

# Declare global variables at the top
camera_running = False  # Initialize as False
cap = None  # Initialize the video capture object


# Initialize the camera
# Pose Execution Window with integrated MoveNet

is_speaking = False
import numpy as np 
def pose_execution_window(pose_name):
    global camera_running, cap
    camera_running = False
    cap = None
    
    model=load_pose_model(pose_name)
    if model is None:
        print(f"Failed to load model for {pose_name}. Exiting.")
        return
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    # Function to speak feedback in a separate thread
    def speak_feedback(feedback):
        global is_speaking
        is_speaking = True
        tts_engine.say(feedback)
        tts_engine.runAndWait()
        is_speaking = False

    engine.setProperty('rate', 150)  # Speed of speech (words per minute)
    engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)
    
    # Variable to store the last spoken feedback
    last_spoken_feedback = None
    last_spoken_time = 0  # Track the last time feedback was spoken

    def start_camera():
        global camera_running, cap
        camera_running = True
        update_streak()

        def update_frame():
            global camera_running
            nonlocal last_spoken_feedback, last_spoken_time
            while camera_running:
                ret, frame = cap.read()
                if not ret:
                    break

                try:
                    # Detect keypoints using movenet
                    detected_pose = movenet.detect(frame)

                    # Check if a pose is detected
                    if detected_pose and hasattr(detected_pose, 'keypoints'):
                        # Preprocess keypoints
                        # Get the preprocessed inputs correctly
                        threshold=0.4
                        keypoints_input,angles_input,raw_angles=preprocess_for_prediction(detected_pose)
                        if pose_name == "Bhujangasana":
                            threshold=0.75
                        elif pose_name =="Kumbhakasana":
                            threshold=0.46
                        elif pose_name=="Virabhadrasana":
                            threshold=0.3
                        elif pose_name=="Natarajasana":
                            threshold=0.092
                        elif pose_name=="Vrksasana":
                            threshold=0.83
                        elif pose_name=="Adhomukhasvanasana":
                            threshold=0.93
                        elif pose_name=="Trikonasana":
                            threshold=0.98
                        elif pose_name=="UtkataKonasana":
                            threshold=0.85
                    # Predict the pose
                   
                        predictions = model.predict([keypoints_input, angles_input])
                        print(f"Raw predictions: {predictions}, Shape: {predictions.shape}")
                        print(f"no. of Raw angles : {raw_angles.shape}")
                        pose_correct = predictions[0][0] > threshold

                        raw_angles = raw_angles.flatten()
                        angle_dict = convert_to_angle_dict(raw_angles, angle_keys)
                        feedback_messages, highlighted_keypoints = get_feedback(pose_name, angle_dict)


                    # Use after method to update UI from thread
                        window.after(0, lambda p=pose_correct: 
                        feedback_label.config(text="Correct Pose!" if p else feedback_messages, 
                                             fg="green" if p else "red"))

                    # Draw keypoints based on whether the pose is correct
                        frame_with_pose = draw_pose(frame, detected_pose, detected=pose_correct, highlighted_keypoints=highlighted_keypoints)

                        # Provide audio feedback every 10 seconds or when feedback changes
                        current_time = time.time()

                        # Prioritize 'Correct Pose!' and interrupt with short message
                        if pose_correct and not is_speaking:
                            Thread(target=speak_feedback, args=("Correct Pose!",)).start()
                            last_spoken_feedback = "Correct Pose!"
                            last_spoken_time = current_time

                        # Otherwise, speak feedback if it's different or enough time has passed
                        elif not pose_correct and (feedback_messages != last_spoken_feedback or (current_time - last_spoken_time) >= 10):
                            Thread(target=speak_feedback, args=(feedback_messages,)).start()
                            last_spoken_feedback = feedback_messages
                            last_spoken_time = current_time

                        
                    else:
                        frame_with_pose = draw_pose(frame, detected_pose, detected=False)
                        feedback_label.config(text="No Pose Detected", fg="white")

                    # Convert frame to RGB for Tkinter
                    frame_rgb = cv2.cvtColor(frame_with_pose, cv2.COLOR_BGR2RGB)

                    # Resize and display
                    resized_frame = cv2.resize(frame_rgb, 
                                               (int(window.winfo_screenwidth() * 0.7), 
                                                int(window.winfo_screenheight() * 0.7)))
                    img = ImageTk.PhotoImage(Image.fromarray(resized_frame))
                    camera_label.configure(image=img)
                    camera_label.image = img

                except Exception as e:
                    print(f"Error in pose detection: {e}")

                # Small delay for smoother performance
                window.update()
                window.after(10)

        # Open camera
        cap = cv2.VideoCapture(0)

        # Rest of the code...
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return

        # Start frame update in a separate thread
        threading.Thread(target=update_frame, daemon=True).start()

    def stop_camera():
        global camera_running
        camera_running = False
        if cap is not None:
            cap.release()
        camera_label.configure(image='')

    def resize_with_aspect_ratio(image, target_width, target_height):
        """Resize image maintaining aspect ratio to fit within target dimensions"""
        original_width, original_height = image.size
        aspect_ratio = original_width / original_height
        target_ratio = target_width / target_height

        if target_ratio > aspect_ratio:
            new_height = target_height
            new_width = int(aspect_ratio * new_height)
        else:
            new_width = target_width
            new_height = int(new_width / aspect_ratio)

        return image.resize((new_width, new_height), Image.LANCZOS)

    window = tk.Tk()
    window.title(f"Perform {pose_name}")
    window.configure(bg="#f0f0f0")
    window.attributes('-fullscreen', True)

    screen_height = window.winfo_screenheight()
    screen_width = window.winfo_screenwidth()

    # Header Frame
    header_frame = tk.Frame(window, bg="#2c3e50", height=int(screen_height * 0.1))
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)

    title_label = tk.Label(
        header_frame,
        text=f"Pose: {pose_name}",
        font=("Helvetica", 24, "bold"),
        bg="#2c3e50",
        fg="white"
    )
    title_label.pack(expand=True)

    # Main content frame
    content_frame = tk.Frame(window, bg="#f0f0f0")
    content_frame.pack(fill="both", expand=True, pady=15)

    # Video Feed and Reference Image Frame
    video_ref_frame = tk.Frame(content_frame, bg="#f0f0f0", height=int(screen_height * 0.7))
    video_ref_frame.pack(fill="both", expand=True)
    video_ref_frame.pack_propagate(False)

    # Video Feed
    camera_frame = tk.Frame(video_ref_frame, bg="black", width=int(screen_width * 0.7), height=int(screen_height * 0.7))
    camera_frame.pack(side="left", padx=5)
    camera_frame.pack_propagate(False)

    camera_label = tk.Label(camera_frame, bg="black")
    camera_label.pack(fill="both", expand=True)

    # Reference Image
    reference_frame = tk.Frame(video_ref_frame, bg="#f0f0f0", width=int(screen_width * 0.3), height=int(screen_height * 0.7))
    reference_frame.pack(side="right", padx=5)
    reference_frame.pack_propagate(False)

    # Load the reference image
    reference_image = Image.open(f"./images/{pose_name.lower()}.jpg")
    target_width = int(screen_width * 0.3)
    target_height = int(screen_height * 0.7)

    resized_image = resize_with_aspect_ratio(reference_image, target_width, target_height)
    photo_image = ImageTk.PhotoImage(resized_image)

    # Create the label and store a reference to the image
    reference_label = tk.Label(reference_frame, image=photo_image, bg="#f0f0f0")
    reference_label.image = photo_image  # Keep a reference to avoid garbage collection
    reference_label.pack(expand=True)

    # Feedback Frame with enhanced visibility
    feedback_frame = tk.Frame(window, bg="#2c3e50", height=int(screen_height * 0.1))
    feedback_frame.pack(fill="x")
    feedback_frame.pack_propagate(False)

    feedback_label = tk.Label(
    feedback_frame,
    text="Feedback will appear here",
    font=("Helvetica", 18, "bold"),  # Smaller font size
    fg="black",
    bg="SystemButtonFace",  # Default background (like transparent)
    wraplength=int(screen_width * 0.8)
    )
    feedback_label.pack(expand=True)

    # Button Frame
    button_frame = tk.Frame(window, bg="#f0f0f0", height=int(screen_height * 0.1))
    button_frame.pack(fill="x")
    button_frame.pack_propagate(False)

    button_container = tk.Frame(button_frame, bg="#f0f0f0")
    button_container.pack(expand=True)

    button_style = {
        "font": ("Helvetica", 12, "bold"),
        "relief": "raised",
        "padx": 20,
        "pady": 8,
        "borderwidth": 2
    }

    start_btn = tk.Button(
        button_container,
        text="Start",
        command=start_camera,
        bg="#4CAF50",
        fg="white",
        **button_style
    )
    start_btn.pack(side="left", padx=10)

    stop_btn = tk.Button(
        button_container,
        text="Stop",
        command=stop_camera,
        bg="#f44336",
        fg="white",
        **button_style
    )
    stop_btn.pack(side="left", padx=10)

    back_btn = tk.Button(
        button_container,
        text="Back",
        command=lambda: [stop_camera(), window.destroy(), pose_selection_window()],
        bg="#2196F3",
        fg="white",
        **button_style
    )
    back_btn.pack(side="left", padx=10)

    def quit_application():
        stop_camera()
        window.destroy()

    quit_btn = tk.Button(
        button_container,
        text="Quit",
        command=quit_application,
        bg="#FF5722",
        fg="white",
        **button_style
    )
    quit_btn.pack(side="left", padx=10)

    window.mainloop()

splash_screen()