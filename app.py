import streamlit as st
import pandas as pd
import cv2
import dlib
import numpy as np
import pygame
import sqlite3
import hashlib
import numpy as np
import imutils
import time
from PIL import Image
import base64
from streamlit_option_menu import option_menu

# Hide Streamlit's default menu and footer
hide_st_style = """
               <style>
               #mainMenu {visibility:hidden;}
               footer {visibility:hidden;}
               </style>
               """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Function to encode an image file as a base64 string
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Set background image function
def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f'''
    <style>
    [data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpeg;base64,{bin_str}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Set the background image globally
set_background(r'C:\Users\nsgma\OneDrive\Desktop\D3\home1_img.webp')

# Initialize Pygame mixer for sound
pygame.mixer.init()

# Function to create the database and user table if they don't exist
def create_db():
    conn = sqlite3.connect('users.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            name TEXT,
            age INTEGER,
            email TEXT,
            mobile TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to hash passwords using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to create a new user in the database
def create_user(username, password, name, age, email, mobile):
    conn = sqlite3.connect('users.db')
    try:
        conn.execute("INSERT INTO users (username, password, name, age, email, mobile) VALUES (?, ?, ?, ?, ?, ?)", 
                     (username, hash_password(password), name, age, email, mobile))
        conn.commit()
        st.success("Account created successfully!")
    except sqlite3.IntegrityError:
        st.error("Username already exists. Please choose another.")
    finally:
        conn.close()

# Function to authenticate a user by checking credentials
def authenticate(username, password):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
        user = cursor.fetchone()
        return user is not None
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return False
    finally:
        conn.close()

# Create the user database if it doesn't exist
create_db()

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# User login/signup interface
if not st.session_state.logged_in:
    st.title("Driver Drowsiness Detection System")
    menu = ["Login", "Signup"]
    choice = st.selectbox("Select the option", menu)

    if choice == "Signup":
        st.subheader("Create a New Account")

    # Additional fields for user information
        username = st.text_input("Username")
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=1, max_value=100, step=1)
        email = st.text_input("Email")
        mobile = st.text_input("Mobile Number")
        password = st.text_input("Password", type='password')
        confirm_password = st.text_input("Confirm Password", type='password')

        if st.button("Signup"):  # Only one button for signing up
            # Check for empty fields and validate inputs
            if not username or not name or age <= 0 or not email or not mobile or not password or not confirm_password:
                st.error("Please fill in all fields.")
            elif password != confirm_password:
                st.error("Passwords do not match. Please try again.")
            else:
                # Create the user if all validations pass
                create_user(username, password, name, age, email, mobile)

    elif choice == "Login":
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            if authenticate(username, password):
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.session_state.username = username  # Store the username in session state
                st.experimental_rerun()  # Refresh after login
            else:
                st.error("Invalid credentials. Please try again.")

# After login, display a sidebar for navigation and main content

# Function to set the sidebar background with a gradient
def set_sidebar_background():
    sidebar_bg = '''
    <style>
    .css-1y4k8a2 {  /* Sidebar container class */
        background: linear-gradient(to bottom, #00698f, #00bfff); /* Example gradient */
        color: white; /* Set text color to white for better contrast */
    }
    </style>
    '''
    st.markdown(sidebar_bg, unsafe_allow_html=True)

set_sidebar_background()

if st.session_state.logged_in:
    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=["Home", "Profile", "About", "Contact us"],
            icons=["house-door-fill", "person-circle", "person-down", "telephone-fill"],
        )

        st.write("---")
        st.write("Guide Name: Mr. Abdul Aziz md")
        st.write("Team Members:")
        st.write("- BHARGAV SUNKARI")
        st.write("- SANTHOSH GEMBALI")
        st.write("- PAVAN KUMAR SIGNSETTI")
        st.write("- ARAVIND KUMAR RAYPUDI")

    # Handle sidebar selection


    if selected == "Home":
        def background(png_file):
            bin_str = get_base64_of_bin_file(png_file)
            page_bg_img = f'''
            <style>
            [data-testid="stAppViewContainer"] {{
                background-image: url("data:image/jpeg;base64,{bin_str}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            '''
            st.markdown(page_bg_img, unsafe_allow_html=True)

        background(r'C:\Users\nsgma\OneDrive\Desktop\D3\background_home.jpg')

        # Add the custom heading for "Driver Drowsiness Detection"
        st.markdown("""
        <h1 style='text-align: center; color: #00698f; font-size: 50px; font-family: "Arial", sans-serif; text-shadow: 2px 2px 5px rgba(0,0,0,0.5);'>
            Driver Drowsiness Detection
        </h1>
        """, unsafe_allow_html=True)
        description = """
            <p style='font-size: 15px; color: white; text-align: justify; font-family: Arial, sans-serif;'>
            The Driver Drowsiness Detection System is an innovative safety technology designed to prevent accidents caused by driver fatigue, a major cause of road accidents globally. 
            This system continuously monitors the driver's face, particularly focusing on the eyes, and detects early signs of drowsiness. 
            When the system detects symptoms of fatigue, such as slow blinking or eye closure, it triggers an alert to wake the driver, potentially preventing dangerous situations.
            </p>
            """

            # Display the description
        st.markdown(description, unsafe_allow_html=True)
        st.markdown("""
            <style>
            div.stButton > button:first-child {
                background-color: blue;
                color: white;
                width: 50%;
                margin: 0 auto;
                display: block;
            }
            </style>
            """, unsafe_allow_html=True)

        # Start ride detection button
        if st.button("Start Ride"):
            # Load the alarm sound
            alarm_sound = pygame.mixer.Sound('alarm-car-or-home-62554.mp3')

            # Function to calculate the Eye Aspect Ratio (EAR)
            def eye_aspect_ratio(eye):
                A = np.linalg.norm(eye[1] - eye[5])
                B = np.linalg.norm(eye[2] - eye[4])
                C = np.linalg.norm(eye[0] - eye[3])
                ear = (A + B) / (2.0 * C)
                return ear

            # Load face and eye detection models
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            detector = dlib.get_frontal_face_detector()
            predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

            # EAR threshold for detecting closed eyes
            EYE_AR_THRESH = 0.2

            # Start video capture
            cap = cv2.VideoCapture(0)

            alarm_played = False
            alarm_start_time = 0

            video_frame = st.empty()  # Streamlit component to display video

            # Stop detection button
            stop_detection = st.button("Stop Detection")

            while True:
                ret, frame = cap.read()
                frame = imutils.resize(frame, width=640)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    dlib_faces = detector(gray)

                    for face in dlib_faces:
                        landmarks = predictor(gray, face)
                        landmarks_array = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(68)])

                        left_eye = landmarks_array[36:42]
                        right_eye = landmarks_array[42:48]
                        left_ear = eye_aspect_ratio(left_eye)
                        right_ear = eye_aspect_ratio(right_eye)
                        ear = (left_ear + right_ear) / 2.0

                        # Detect drowsiness based on EAR
                        if ear < EYE_AR_THRESH:
                            cv2.putText(frame, "DROWSY", (frame.shape[1] // 2 - 50, frame.shape[0] // 2), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
                            if not alarm_played:
                                alarm_sound.play()
                                alarm_played = True
                                alarm_start_time = time.time()
                        else:
                            cv2.putText(frame, "AWAKE", (frame.shape[1] // 2 - 50, frame.shape[0] // 2), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
                            if alarm_played:
                                alarm_sound.stop()
                                alarm_played = False

                        if alarm_played and time.time() - alarm_start_time > 10:
                            alarm_sound.stop()
                            alarm_played = False

                        # Draw facial landmarks
                        for n in range(0, 68):
                            cv2.circle(frame, (landmarks_array[n, 0], landmarks_array[n, 1]), 1, (255, 0, 0), -1)

                # Display video in Streamlit
                video_frame.image(frame, channels="BGR")

                if stop_detection:
                    break

            # Release camera and destroy windows
            cap.release()
            cv2.destroyAllWindows()

            # "About" section content
    elif selected == "About":
        # Function to set a custom background and enhance the page
        def about_background():
            page_bg_style = '''
            <style>
            [data-testid="stAppViewContainer"] {
                background: linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%);
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }
            [data-testid="stHeader"], [data-testid="stToolbar"] {
                background: rgba(0,0,0,0); /* Hide header */
            }
            h2 {
                color: #003366; /* Dark blue for headings */
                font-size: 28px;
                font-weight: bold;
                font-family: 'Helvetica', sans-serif;
                text-align: center;
                text-transform: uppercase;
                padding: 15px 0;
                text-shadow: 2px 2px 5px rgba(0,0,0,0.3); /* Subtle shadow for the text */
            }
            h3 {
                color: #006400; /* Dark green for subheadings */
                font-size: 22px;
                font-weight: bold;
                font-family: 'Helvetica', sans-serif;
                padding: 10px 0;
                text-transform: capitalize;
            }
            p {
                color: #ffffff; /* White text */
                font-size: 18px;
                font-family: 'Arial', sans-serif;
                line-height: 1.6;
                text-align: justify;
                background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent background for contrast */
                padding: 10px 15px;
                border-radius: 5px;
            }
            .stImage {
                border-radius: 10px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5); /* Shadow for the image */
            }
            </style>
            '''
            st.markdown(page_bg_style, unsafe_allow_html=True)

        about_background()

        # About the System Section
        st.title("About the System")
        st.write("---")
        
        # Display image with custom styling
        img = Image.open("car_img.jpeg")
        st.image(
            img,
            caption="Driver Drowsiness Detection",
            width=400,
            channels="RGB",
            use_column_width=False
        )

        # Introduction Section
        st.markdown("<h2>Introduction</h2>", unsafe_allow_html=True)
        st.write("<p>The <b>Driver Drowsiness Detection System</b> is an innovative solution designed to combat one of the leading causes of road accidents: <b>driver fatigue</b>.</p>", unsafe_allow_html=True)
        st.write("<p>According to global road safety reports, drowsy driving is responsible for thousands of crashes, injuries, and fatalities every year.</p>", unsafe_allow_html=True)
        st.write("<p>Drivers experiencing fatigue often have slower reaction times, impaired judgment, and a higher likelihood of falling asleep behind the wheel, which can lead to catastrophic accidents.</p>", unsafe_allow_html=True)

        # How it Works Section
        st.markdown("<h2>How it Works</h2>", unsafe_allow_html=True)
        st.write("<p>Our system leverages <b>advanced computer vision</b> and <b>machine learning techniques</b> to continuously monitor the driver's facial expressions, focusing on eye movements and blinking patterns.</p>", unsafe_allow_html=True)
        st.write("<p>By analyzing the <b>Eye Aspect Ratio (EAR)</b> through real-time video feeds, the system detects signs of drowsiness, such as prolonged eye closure or frequent blinking, and alerts the driver with an <b>auditory alarm</b>.</p>", unsafe_allow_html=True)

        # Why is this Important Section
        st.markdown("<h2>Why is this Important?</h2>", unsafe_allow_html=True)

        st.markdown("<h3>Road Safety</h3>", unsafe_allow_html=True)
        st.write("<p>Fatigue-related accidents often occur without any warning, especially on long or monotonous journeys. Early detection provides critical time for drivers to take necessary actions like pulling over or resting.</p>", unsafe_allow_html=True)

        st.markdown("<h3>Prevent Fatalities</h3>", unsafe_allow_html=True)
        st.write("<p>Drowsy driving is just as dangerous as drunk driving. Research shows that driving after being awake for 18+ hours is equivalent to having a <b>blood alcohol content (BAC) of 0.05%</b>. Our system aims to reduce this risk and save lives.</p>", unsafe_allow_html=True)

        st.markdown("<h3>Cost Reduction</h3>", unsafe_allow_html=True)
        st.write("<p>Fatigue-related accidents can lead to significant financial losses due to vehicle damage, legal costs, and medical expenses.</p>", unsafe_allow_html=True)



    elif selected == "Profile":
        # Function to set a custom background with a gradient or attractive color
        def profile_background():
            page_bg_style = '''
            <style>
            [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, #74ebd5, #ACB6E5); /* Soft blue gradient */
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }
            [data-testid="stHeader"], [data-testid="stToolbar"] {
                background: rgba(0,0,0,0); /* Hide header */
            }
            h1 {
                color: #ffffff; /* White for the profile heading */
                font-size: 36px;
                font-family: 'Segoe UI', sans-serif;
                text-align: center;
                margin-bottom: 30px;
                text-shadow: 2px 2px 5px rgba(0,0,0,0.5); /* Slight shadow for the heading */
                display: flex;
                justify-content: center;
                align-items: center;
            }
            h1 i {
                margin-right: 10px; /* Space between icon and text */
                font-size: 40px; /* Icon size */
            }
            h2 {
                color: #00698f; /* Blue for profile labels */
                font-size: 24px;
                font-family: 'Arial', sans-serif;
                margin-bottom: 5px;
                font-weight: bold;
                text-shadow: 1px 1px 3px rgba(0,0,0,0.3); /* Shadow for headings */
            }
            p {
                color: #ffffff; /* White for the profile details */
                font-size: 18px;
                font-family: 'Arial', sans-serif;
                background-color: rgba(0, 0, 0, 0.3); /* Slightly transparent black background */
                padding: 10px;
                border-radius: 8px;
                margin-bottom: 20px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); /* Add box shadow for text sections */
            }
            .value {
                color: #FFD700; /* Gold color for values (e.g., "Mani Sunkari") */
                font-size: 20px; /* Slightly larger font size for values */
                font-weight: normal; /* Regular weight for values */
            }
            </style>
            '''
            st.markdown(page_bg_style, unsafe_allow_html=True)

        # Include Font Awesome
        st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
        """, unsafe_allow_html=True)

        # Profile Heading with Font Awesome icon
        st.markdown("""
        <h1><i class="fas fa-user-circle"></i>Your Profile</h1>
        """, unsafe_allow_html=True)

        # Connect to database and fetch user data
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (st.session_state.username,))
        user_data = cursor.fetchone()
        conn.close()

        # Function to format text for profile fields
        def formatted_text(label, value):
            return f"<h2>{label}:</h2><p class='value'>{value}</p>"

        if user_data:
            # Display user profile details with styled headings and text
            st.markdown(formatted_text("Name", user_data[3]), unsafe_allow_html=True)
            st.markdown(formatted_text("Age", user_data[4]), unsafe_allow_html=True)
            st.markdown(formatted_text("Email", user_data[5]), unsafe_allow_html=True)
            st.markdown(formatted_text("Mobile", user_data[6]), unsafe_allow_html=True)
        else:
            st.error("Unable to fetch user data.")

        # Logout button
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.experimental_rerun()



    elif selected == "Contact us":
        # Function to add a custom background with a vibrant blue theme
        def background():
            page_bg_style = '''
            <style>
            [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, #007BFF 0%, #00C6FF 100%);
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }
            [data-testid="stHeader"], [data-testid="stToolbar"] {
                background: rgba(0,0,0,0); /* Hides header */
            }
            h1 {
                color: #FFFFFF; /* White color for the heading */
                font-size: 40px;
            }
            h2, h3, h4, h5, h6 {
                color: #FFDD00; /* Distinct gold color for subheadings */
            }
            .highlight-email {
                font-size: 20px;
                font-weight: bold;
                color: #FF5733; /* Bright orange for the email */
                background-color: #FFF3CD; /* Light yellow background */
                padding: 5px 10px;
                border-radius: 5px;
                display: inline-block;
            }
            .stTable {
                background-color: rgba(255, 255, 255, 0.8); /* Light background for the table to improve readability */
            }
            </style>
            '''
            st.markdown(page_bg_style, unsafe_allow_html=True)

        background()
        
        # Contact Us Section with white heading color
        st.title("Contact Us")
        
        st.write("If you have any questions or need support, please feel free to reach out:")

        # Highlighted email
        st.markdown('<p class="highlight-email">bhargavsunkari13@gmail.com</p>', unsafe_allow_html=True)
        
        st.write("---")

        # Contact details in a table
        data = [
            ["Leader", "BHARGAV SUNKARI ", "8106012509","bhargavsunkari13@gmail.com"],
            ["Team #1", "SANTHOSH GEMBALI", "7569926814","gembalisantoshkumar14@gmail.com"],
            ["Team #2", "PAVAN KUMAR SIGNISETTI","9398207933","pavansingisetti@gmail.com"],
            ["Team #3", "ARAVIND KUMAR RAYPUDI", "9100543554","aravindravipudi@gmail.com"]
        ]
        
        df = pd.DataFrame(data, columns=["Position","Name", "Phone Number","E-Mail"])
        st.table(df)
