# How to Deploy Farmer Super App to Streamlit Cloud

Your application is ready for deployment! Follow these steps to put it online.

## 1. Prepare GitHub Repository
1. Create a **New Repository** on [GitHub](https://github.com/new).
2. Upload all your project files to this repository. You can do this via command line or by uploading files directly in the browser (if the project is small).
   - **Important**: Do NOT upload `.env` or `user_db.json` if it contains real user data. 
   - Ensure `requirements.txt` is included.

## 2. Deploy on Streamlit Cloud
1. Go to [Streamlit Community Cloud](https://share.streamlit.io/) and Sign Up/Login.
2. Click **"New app"**.
3. Select your GitHub repository, branch (usually `main`), and the main file path: `app.py`.
4. Click **"Advanced Settings"** before deploying.

## 3. Configure Secrets (Crucial Step)
Streamlit Cloud doesn't read your `.env` file. You must add your API keys manually in the **Secrets** section.

Copy and paste the following into the **Secrets** text area (replace with your actual keys):

```toml
GOOGLE_API_KEY = "your_actual_google_api_key_here"
WEATHER_API_KEY = "your_actual_openweathermap_key_here"
```

## 4. Click "Deploy"!
- Streamlit will install the libraries from `requirements.txt`.
- It will start your app.
- Once finished, you will get a public URL (e.g., `https://farmer-app.streamlit.app`) to share with everyone!

### Troubleshooting
- **Background Images**: If background images don't load, ensure they are in the `assets/` folder and that folder is uploaded to GitHub.
- **API Errors**: If you see "API Key Error", double-check the **Secrets** usage in Step 3.
