# Prisma AI Pro - Quick Start Guide

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Get API Key
1. Go to [Groq Console](https://console.groq.com)
2. Create account or login
3. Generate API key
4. Copy the key (starts with `gsk_`)

### Step 3: Configure API Key
Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your_api_key_here"
```

### Step 4: Run Application
```bash
streamlit run app.py
```

### Step 5: Open Browser
Navigate to `http://localhost:8501`

---

## 🎯 Using the App

### Chat
- Type messages directly
- Use quick action buttons (Summarize, Code, Explain)
- Get instant AI responses

### Upload PDF
- Click "Upload PDF" in sidebar
- Select a PDF file
- AI will use PDF content for context

### Upload Image
- Click "Upload Image" in sidebar
- Select JPG/PNG image
- AI will analyze the image

### Download Chat
- Click "Download" button
- Get entire chat as PDF
- Save for records

### Start New Chat
- Click "New Chat" button
- Clear all history
- Start fresh conversation

---

## 🎨 UI Features

### Sidebar (Purple Gradient)
- 📂 PDF upload
- 🖼️ Image upload
- 📥 Download chat
- 🧹 New chat button

### Main Area
- 💬 Chat messages
- 📝 Quick actions
- 💻 Chat input

### Color Scheme
- Purple gradient (#667eea → #764ba2)
- Clean white background
- Professional typography

---

## 🔧 Troubleshooting

### App won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### API key error
- Verify key in `.streamlit/secrets.toml`
- Key should start with `gsk_`
- Check for typos

### PDF won't upload
- Ensure PDF is valid
- Try smaller PDF first
- Check file size

### Slow responses
- Check internet connection
- Verify API key is valid
- Try simpler queries first

---

## 📚 Documentation

- **README.md** - Full documentation
- **IMPROVEMENTS.md** - Code improvements
- **UI_IMPROVEMENTS.md** - Design details
- **PROJECT_SUMMARY.md** - Complete overview

---

## 🚀 You're Ready!

Your Prisma AI Pro is now running. Start chatting! 💎

For detailed info, see `README.md`
