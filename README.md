# 🌾 Farmer App: Smart Agriculture Assistant

A professional, AI-powered Streamlit web application designed to help farmers optimize their crop yields and get expert agricultural advice.

## 🚀 Features
- **🌱 Crop Recommendation**: Get personalized crop suggestions based on Nitrogen (N), Phosphorus (P), Potassium (K), soil pH, and local weather patterns (Temperature, Humidity, Rainfall).
- **🤖 AI Agronomist**: A virtual agriculture expert powered by Google Gemini AI, capable of answering complex farming questions, diagnosing pests, and providing soil health tips.
- **☁️ Weather Dashboard**: Real-time weather monitoring for better planning.
- **💎 Premium UI**: A clean, responsive, and easy-to-use interface designed for practicality.

## 🛠️ Installation

1. **Clone or Download** this folder.
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up API Keys**:
   - Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/).
   - Add it to the `.env` file or enter it directly in the app's sidebar.

## 🏃 How to Run
```bash
streamlit run app.py
```

## 📁 Project Structure
- `app.py`: The main user interface and navigation.
- `logic.py`: Contains the logic for crop prediction and AI communication.
- `requirements.txt`: List of Python libraries needed.
- `.env`: Template for securing your API keys.
