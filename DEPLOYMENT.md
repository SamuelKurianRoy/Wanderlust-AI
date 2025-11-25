# 🚀 Deployment Guide

## Deploying to Streamlit Cloud

### Prerequisites
- GitHub account
- Google Gemini API key
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io/))

### Step-by-Step Deployment

#### 1. Prepare Your Repository
```bash
# Make sure all changes are committed
git add .
git commit -m "Ready for deployment"
git push origin main
```

#### 2. Deploy on Streamlit Cloud

1. Go to [https://share.streamlit.io/](https://share.streamlit.io/)
2. Click "New app"
3. Select your repository: `Wanderlust-AI`
4. Set the main file path: `app.py`
5. Click "Deploy"

#### 3. Add Secrets

1. In your deployed app's dashboard, click the "⚙️ Settings" button
2. Navigate to the "Secrets" section
3. Add your secrets in TOML format:

```toml
GEMINI_API_KEY = "your_actual_gemini_api_key_here"
```

4. Click "Save"
5. Your app will automatically restart with the new secrets

### ✅ That's it!

Your AI Travel Planner is now live and accessible via the Streamlit Cloud URL!

## 🔒 Security Best Practices

- ✅ Secrets are stored securely in Streamlit Cloud
- ✅ Never commit `.streamlit/secrets.toml` or `.env` to Git
- ✅ Both files are already in `.gitignore`
- ✅ API keys are never exposed in the frontend

## 🐛 Troubleshooting

**App won't start:**
- Check that `requirements.txt` is up to date
- Verify API key is correctly set in secrets

**AI features not working:**
- Ensure `GEMINI_API_KEY` secret name matches exactly
- Check API key is valid at [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
- Verify you haven't exceeded API quota limits

**App is slow:**
- Free tier has resource limitations
- Consider upgrading to Streamlit Cloud paid plan for better performance

## 📱 Sharing Your App

Once deployed, you'll get a URL like:
```
https://your-app-name.streamlit.app
```

Share this URL with anyone - no sign-up required for users!

## 🔄 Updating Your Deployment

Simply push changes to GitHub:
```bash
git add .
git commit -m "Update features"
git push origin main
```

Streamlit Cloud will automatically detect changes and redeploy your app!

## 🌐 Custom Domain (Optional)

Streamlit Cloud Pro allows custom domains. Check the [Streamlit documentation](https://docs.streamlit.io/) for details.

---

**Need help?** Check the [Streamlit Community Forum](https://discuss.streamlit.io/)
