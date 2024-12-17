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
    </style>
    """,
    unsafe_allow_html=True
)

# Authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<p class="title">Login</p>', unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        st.session_state.authenticated = True
        st.session_state.username = username
        log_activity(username, "Logged in")
        st.success(f"Successfully logged in as {username}!")
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
        
        # Input data to generate visualization details
        co_value = st.number_input('CO AQI Value:', min_value=0, value=50, step=1, format="%d")
        ozone_value = st.number_input('Ozone AQI Value:', min_value=0, value=30, step=1, format="%d")
        no2_value = st.number_input('NO2 AQI Value:', min_value=0, value=20, step=1, format="%d")
        pm25_value = st.number_input('PM2.5 AQI Value:', min_value=0, value=10, step=1, format="%d")

        # Basic descriptions to show good vs bad air quality
        good_air = "The air quality is considered <b>Good</b> when AQI values are low and have minimal health impact. <br>"
        bad_air = "The air quality becomes <b>Hazardous</b> when AQI values reach higher levels, and it may trigger significant health problems.<br>"
        
        st.markdown(f'<p class="description">{good_air}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="description">{bad_air}</p>', unsafe_allow_html=True)

        # Calculate general air quality threshold from user input
        data = {
            "AQI Parameter": ["CO", "Ozone", "NO2", "PM2.5"],
            "Input Value": [co_value, ozone_value, no2_value, pm25_value],
            "Good Threshold": [50, 50, 50, 50],  # You can adjust these threshold values based on your model or actual guidelines
            "Moderate Threshold": [100, 100, 100, 100],
            "Unhealthy Threshold": [150, 150, 150, 150]
        }
        df = pd.DataFrame(data)
        st.write(df)
        
        fig, ax = plt.subplots(figsize=(8, 5))

        # Plot for AQI categories
        ax.pie(df["Input Value"], labels=df["AQI Parameter"], autopct='%1.1f%%', colors=['#4CAF50', '#FFEB3B', '#FF5722', '#FF0000'])
        st.pyplot(fig)

        st.markdown("""
        
        """, unsafe_allow_html=True)

    elif page == "About":
        st.markdown('<p class="title">About</p>', unsafe_allow_html=True)
        st.markdown(
            """
            <p class="description">
            
            "Breathe Better, Live Smarter!" 🌿
            </p>
            <p class="description">
            Welcome to Air Quality Prediction, your smart AI-powered companion for monitoring and understanding air quality. By analyzing AQI factors like CO, Ozone, NO₂, and PM2.5, we deliver instant  reports.

Stay aware, stay healthy—because every breath shapes your life. Breathe smart, live brighter! 
            </p>
            """,
            unsafe_allow_html=True
        )

    elif page == "Logout":
        log_activity(st.session_state.username, "Logged out")
        st.session_state.authenticated = False
        st.success("You have been logged out.")
