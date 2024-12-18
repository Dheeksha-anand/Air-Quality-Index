import pickle
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load the saved model, scaler, and encoders from pickle
with open('air_quality_model.pkl', 'rb') as model_file:
    loaded_objects = pickle.load(model_file)
    model = loaded_objects["model"]
    scaler = loaded_objects["scaler"]
    saved_encoders = loaded_objects["encoders"]

# Function to predict AQI category
def predict_aqi_category(co_value, ozone_value, no2_value, pm25_value):
    input_data = np.array([co_value, ozone_value, no2_value, pm25_value]).reshape(1, -1)
    input_data_scaled = scaler.transform(input_data)
    predicted_category_encoded = model.predict(input_data_scaled)
    predicted_category_decoded = saved_encoders['AQI Category'].inverse_transform([predicted_category_encoded[0]])
    return predicted_category_decoded[0]

# Function to log user activity
def log_activity(username, activity):
    with open('user_activity.log', 'a') as log_file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_file.write(f"{timestamp} | {username} | {activity}\n")

# Set up the page layout and title
st.set_page_config(page_title="Air Quality Prediction", layout="centered")

# Add custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background: url('avenue-815297_1280.jpg') no-repeat center center fixed;
        background-size: cover;
        font-family: 'Arial', sans-serif;
        color: white;
    }
    .title {
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
    }
    .description {
        font-size: 20px;
        text-align: center;
        margin-bottom: 30px;
    }
    .input-section {
        background-color: rgba(0, 0, 0, 0.6); 
        padding: 30px;
        border-radius: 15px;
        margin: auto;
        width: 50%;
        text-align: center;
    }
    .button {
        background-color: #ff6f61; 
        color: white;
        padding: 15px 30px;
        border: none;
        border-radius: 8px;
        font-size: 18px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .button:hover {
        background-color: #ff9478;
        transform: scale(1.05);
    }
    .output {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
    }
    footer {
        text-align: center;
        padding: 10px;
        margin-top: 50px;
        background-color: #1d2b64;
        color: white;
    }
    .center-button {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Login validation functions
def is_valid_username(username):
    # Check that username is not empty and does not contain numbers
    if not username:
        return False
    return not any(char.isdigit() for char in username)

if not st.session_state.authenticated:
    st.markdown('<p class="title">Login</p>', unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    # Login logic with username and password validation
    if st.button("Login"):
        if is_valid_username(username) and password:
            st.session_state.authenticated = True
            st.session_state.username = username
            log_activity(username, "Logged in")
            st.success(f"Successfully logged in as {username}!")
            st.rerun()  # Rerun to show the main app page
        else:
            if not is_valid_username(username):
                st.error("Username must not contain numbers.")
            elif not password:
                st.error("Please enter a password.")
else:
    # Sidebar Navigation
    page = st.sidebar.radio("Navigate", ["Home", "Visualize Air Quality", "About", "Logout"])

    if page == "Home":
        st.markdown('<p class="title">Air Quality Prediction</p>', unsafe_allow_html=True)
        st.markdown('<p class="description">Enter AQI values to predict the air quality category.</p>', unsafe_allow_html=True)

        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        co_value = st.number_input('CO AQI Value:', min_value=0, value=50, step=1, format="%d")
        ozone_value = st.number_input('Ozone AQI Value:', min_value=0, value=30, step=1, format="%d")
        no2_value = st.number_input('NO2 AQI Value:', min_value=0, value=20, step=1, format="%d")
        pm25_value = st.number_input('PM2.5 AQI Value:', min_value=0, value=10, step=1, format="%d")

        if st.button("Predict AQI Category"):
            predicted_category = predict_aqi_category(co_value, ozone_value, no2_value, pm25_value)
            color = {
                "Good": "#4CAF50",
                "Moderate": "#FFEB3B",
                "Unhealthy": "#FF5722",
                "Hazardous": "#FF0000"
            }.get(predicted_category, "#FFFFFF")

            st.markdown(
                f'<p class="output" style="color:{color};">Predicted AQI Category: {predicted_category}</p>',
                unsafe_allow_html=True
            )
            log_activity(st.session_state.username, f"Predicted AQI: {predicted_category}")
        st.markdown('</div>', unsafe_allow_html=True)

    elif page == "Visualize Air Quality":
        st.markdown('<p class="title">Visualize Air Quality</p>', unsafe_allow_html=True)
        co_value = st.number_input('CO AQI Value:', min_value=0, value=50, step=1, format="%d")
        ozone_value = st.number_input('Ozone AQI Value:', min_value=0, value=30, step=1, format="%d")
        no2_value = st.number_input('NO2 AQI Value:', min_value=0, value=20, step=1, format="%d")
        pm25_value = st.number_input('PM2.5 AQI Value:', min_value=0, value=10, step=1, format="%d")

        # Additional data table columns
        data = {
            "AQI Parameter": ["CO", "Ozone", "NO2", "PM2.5"],
            "Input Value": [co_value, ozone_value, no2_value, pm25_value],
            "Good Range": ["0-50", "0-54", "0-53", "0-12"],
            "Moderate Range": ["51-100", "55-70", "54-100", "13-35"],
            "Unhealthy Range": ["101-150", "71-85", "101-360", "36-55"],
            "Very Unhealthy Range": [">150", ">85", ">360", ">55"]
        }
        df = pd.DataFrame(data)

        # Display the data table
        st.markdown('<p class="description">AQI Parameter Ranges</p>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)

        # Pie chart visualization
        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor("#121212")
        ax.set_facecolor("#121212")
        wedges, texts, autotexts = ax.pie(
            df["Input Value"], 
            labels=df["AQI Parameter"], 
            autopct='%1.1f%%', 
            colors=['#4CAF50', '#FFEB3B', '#FF5722', '#FF0000']
        )
        
        # Set label and percentage text colors to white
        plt.setp(texts, color='white')
        plt.setp(autotexts, color='white')
        
        plt.title("AQI Distribution", color="white")
        st.pyplot(fig)

    elif page == "About":
        st.markdown('<p class="title">About Air Quality Prediction</p>', unsafe_allow_html=True)
        
        # Attractive About section with quote and description
        st.markdown("""
        <div style="background-color: rgba(0, 0, 0, 0.6); padding: 30px; border-radius: 15px; margin: 20px 0;">
        <blockquote style="font-style: italic; font-size: 24px; color: #ff6f61; text-align: center; margin-bottom: 20px;">
        "The air we breathe is the very essence of life. Understanding it is our first step towards protecting it."
        </blockquote>
        
        <p style="color: white; font-size: 18px; line-height: 1.6; text-align: justify;">
        Our Air Quality Prediction app is more than just a tool—it's a mission to empower individuals with critical environmental insights. 
        In an era of increasing environmental challenges, knowledge is our most powerful weapon in the fight for cleaner, healthier air.
        </p>
        
        <h2 style="color: #4CAF50; text-align: center; margin-top: 20px;">Our Vision</h2>
        
        <p style="color: white; font-size: 16px; line-height: 1.6; text-align: justify;">
        We believe that by providing real-time, accurate air quality information, we can:
        • Raise awareness about environmental health
        • Help individuals make informed decisions
        • Contribute to a global movement of environmental consciousness
        </p>
        
        <div style="text-align: center; margin-top: 20px;">
        <img src="/api/placeholder/400/200" alt="Environmental Awareness" style="max-width: 100%; border-radius: 10px;">
        </div>
        
        <p style="color: #FFEB3B; text-align: center; margin-top: 20px; font-size: 16px;">
        Together, we can breathe easier. Together, we can make a difference.
        </p>
        </div>
        """, unsafe_allow_html=True)

    elif page == "Logout":
        st.markdown('<p class="title">Logout</p>', unsafe_allow_html=True)
        
        # Create a centered container for the logout button
        col1, col2, col3 = st.columns([3, 2, 3])
        
        with col2:
            if st.button("Confirm Logout", key="logout_button"):
                log_activity(st.session_state.username, "Logged out")
                st.session_state.authenticated = False
                st.success("You have been logged out. Refresh the page to log back in.")
