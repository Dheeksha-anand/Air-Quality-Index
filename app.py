import pickle
import streamlit as st
import numpy as np

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

# Set up the page layout and title
st.set_page_config(page_title="Air Quality Prediction", layout="centered")

# Add custom CSS for animations and styling
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to bottom, #1d2b64, #f8cdda);
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

# Login Section
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<p class="title">Login</p>', unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        st.session_state.authenticated = True
        st.success(f"Successfully logged in as {username}!")
else:
    # Sidebar Navigation
    page = st.sidebar.radio("Navigate", ["Home", "About"])

    if page == "Home":
        # Header of the app
        st.markdown('<p class="title">Air Quality Prediction</p>', unsafe_allow_html=True)
        st.markdown('<p class="description">Enter AQI values to predict the air quality category.</p>', unsafe_allow_html=True)

        # User input section
        st.markdown('<div class="input-section">', unsafe_allow_html=True)

        co_value = st.number_input('CO AQI Value:', min_value=0, value=50, step=1, format="%d")
        ozone_value = st.number_input('Ozone AQI Value:', min_value=0, value=30, step=1, format="%d")
        no2_value = st.number_input('NO2 AQI Value:', min_value=0, value=20, step=1, format="%d")
        pm25_value = st.number_input('PM2.5 AQI Value:', min_value=0, value=10, step=1, format="%d")

        # Predict button
        if st.button("Predict AQI Category"):
            predicted_category = predict_aqi_category(co_value, ozone_value, no2_value, pm25_value)

            # Color-coded output
            if predicted_category == "Good":
                color = "#4CAF50"  # Green for good air quality
            elif predicted_category == "Moderate":
                color = "#FFEB3B"  # Yellow for moderate air quality
            elif predicted_category == "Unhealthy":
                color = "#FF5722"  # Orange for unhealthy air quality
            else:
                color = "#FF0000"  # Red for very unhealthy or hazardous

            st.markdown(
                f'<p class="output" style="color:{color};">Predicted AQI Category: {predicted_category}</p>',
                unsafe_allow_html=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

    elif page == "About":
        st.markdown('<p class="title">About</p>', unsafe_allow_html=True)
        st.markdown(
            """
            <p class="description">
"Breathe smart, live better – the air you inhale shapes the life you exhale." 

Welcome to **Air Quality Prediction**, your smart companion for staying informed about the air you breathe. Using AI-powered insights, our app analyzes AQI factors like CO, Ozone, NO₂, and PM2.5 to provide accurate and instant predictions.  

With an intuitive design and vibrant, color-coded results, tracking air quality has never been easier. Stay informed, stay protected, and embrace a healthier future!
            </p>
            """,
            unsafe_allow_html=True
        )

    # Footer
    st.markdown(
        """
        <footer>
            &#169; 2024 Air Quality Prediction | Powered by AI
        </footer>
        """,
        unsafe_allow_html=True
    )
