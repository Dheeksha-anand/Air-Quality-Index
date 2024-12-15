# 🌟 **Air Quality Prediction Application**


## Welcome to the Air Quality Prediction Application

A user-friendly tool that leverages machine learning to predict air quality categories based on AQI (Air Quality Index) values of major pollutants such as CO, Ozone, NO2, and PM2.5.



## 🚀 **Features**


✨ Real-Time PredictionsQuickly predicts the air quality category using pre-trained machine learning models.

✨ Interactive DesignSmooth transitions, user-friendly layout, and clean styling enhanced with dynamic animations.

✨ Custom StylingA visually appealing design with a gradient background and modern UI elements for a premium experience.

## 🛠️ **Technology Stack**

Frontend: Streamlit

Machine Learning: Scikit-learn

Preprocessing: Data scaler and encoders (Pickle files)

Programming: Python

## 💻 **Installation Guide**

Clone the repository:

    git clone https://github.com/your-repository/air-quality-prediction.git
    cd air-quality-prediction

Install dependencies:

    pip install -r requirements.txt

Run the application:

    streamlit run app.py

## 🧪 **How It Works**

Input AQI Values: Enter AQI values for pollutants like CO, Ozone, NO2, and PM2.5.

Scaled Data: Inputs are preprocessed using a preloaded scaler for accuracy.

Prediction: A trained ML model predicts the air quality category instantly.

Result: The predicted AQI category is displayed on the screen in a visually prominent format.

## 💂️‍♀️ **Project Structure**

    📁 air-quality-prediction/
    ├── app.py                  # Main application code
    ├── air_quality_model.pkl   # Pre-trained ML model & preprocessors
    ├── requirements.txt        # Python dependencies
    ├── README.md                # Project overview

## 🌈 **Application Layout**

### 📊 Prediction Section

Input Fields: Specify pollutant AQI values.

Predict Button: Get an instant AQI category prediction.

Responsive Design: Works across different screen sizes.



## ✨ **Workflow**
Data Preprocessing

Input features are scaled using StandardScaler.
Labels are encoded using LabelEncoder.
Model Training

The Random Forest Classifier is used for training the model.
Data is split into training and testing sets (80/20).
Model Saving

The trained model is saved as a .pkl file using pickle.
Deployment

Web UI is built using Streamlit to take user AQI inputs.
The trained model is loaded to predict and display the AQI category.

## 🚀 **Execution**
Train the Model
Run the model training script:

    python train_model.py
This script:<br>
Loads and preprocesses the data.<br>
Trains the Random Forest model.<br>
Saves the model as air_quality_model.pkl.

Start the Streamlit Web App

    streamlit run app.py
    
Interact with the Web App

The Streamlit interface allows you to input CO, Ozone, NO2, PM2.5 values.
Click on "Predict AQI Category" to see the prediction result.


## 🚧 **Future Enhancements**

✅ Add real-time AQI updates via APIs.<br>
✅ Incorporate trend visualizations for air quality over time.<br>
✅ Include a comparison chart for AQI standards.


## 📜 **License**

This project is licensed under the MIT License. See the LICENSE file for more information.

## 🌟 **Acknowledgments**

Special thanks to Streamlit and Scikit-learn for their powerful tools, and to all those who contributed to the development of this application.

# 🚀 Get started today and make a positive impact with air quality insights!
