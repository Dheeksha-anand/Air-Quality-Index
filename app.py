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
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }

    body {
        background: linear-gradient(to bottom, #1d2b64, #f8cdda);
        animation: fadeIn 2s;
        font-family: 'Arial', sans-serif;
        color: white;
    }

    .title {
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        animation: fadeIn 1.5s ease-in-out;
    }

    .description {
        font-size: 20px;
        text-align: center;
        margin-bottom: 30px;
        animation: fadeIn 1.8s ease-in-out;
    }

    .input-section {
        background-color: rgba(0, 0, 0, 0.6); 
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
        text-align: center;
        margin: auto;
        width: 50%;
        animation: fadeIn 2s ease-in-out;
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
        animation: fadeIn 2.5s ease-in-out;
    }

    .button:hover {
        background-color: #ff9478;
        box-shadow: 0px 4px 15px rgba(255, 111, 97, 0.5);
        transform: scale(1.05);
    }

    .output {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
        color: #ffd700;
        animation: fadeIn 3s ease-in-out;
    }

    footer {
        text-align: center;
        padding: 15px;
        margin-top: 50px;
        background-color: #1d2b64;
        color: white;
        animation: fadeIn 3.5s ease-in-out;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
if st.button("Predict AQI Category", key="predict_button", help="Click to predict AQI"):
    predicted_category = predict_aqi_category(co_value, ozone_value, no2_value, pm25_value)
    st.markdown(f'<p class="output">Predicted AQI Category: {predicted_category}</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <footer>
        &#169; 2024 Air Quality Prediction | Powered by AI
    </footer>
    """,
    unsafe_allow_html=True
)
