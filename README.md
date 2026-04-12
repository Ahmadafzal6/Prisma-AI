# Prisma AI Pro

A professional AI agent application built with Streamlit, LangChain, and Groq API. Features intelligent routing, PDF context awareness, and image vision capabilities.

## Features

✨ **Intelligent Agent Routing** - Automatically selects fast or smart models based on query complexity
📄 **PDF Context** - Upload PDFs for contextual analysis and Q&A
🖼️ **Image Vision** - Analyze images with vision-capable models
💬 **Chat History** - Download conversations as PDF
🔍 **Web Search** - Real-time information retrieval via DuckDuckGo
⚡ **Fast & Smart Models** - Llama 3.1 8B for speed, Llama 3.3 70B for complex tasks

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

Or set environment variable:
```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

Get your API key from [Groq Console](https://console.groq.com)

### 3. Run the Application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Project Structure

```
prisma_ai/
├── app.py                 # Main Streamlit application
├── chk_models.py         # Utility to check available models
├── requirements.txt      # Python dependencies
├── .streamlit/
│   ├── config.toml       # Streamlit configuration
│   └── secrets.toml      # API keys (git-ignored)
└── README.md             # This file
```

## Usage

### Chat Interface
- Type messages directly or use quick action buttons
- Upload PDFs for context-aware responses
- Upload images for vision analysis
- Download chat history as PDF

### Quick Actions
- **📝 Summarize** - Summarize content
- **💻 Code** - Generate Python code
- **💡 Explain** - Explain concepts simply

### Model Selection
The app automatically routes queries:
- **Fast Model** (Llama 3.1 8B): Simple questions, greetings
- **Smart Model** (Llama 3.3 70B): Complex analysis, coding, PDF context

## Security

⚠️ **Important Security Notes:**
- Never commit API keys to version control
- Use `.streamlit/secrets.toml` for local development
- Use environment variables in production
- The app validates API keys on startup

## Troubleshooting

### "GROQ API Key Missing"
- Ensure `GROQ_API_KEY` is set in `.streamlit/secrets.toml` or environment
- Verify the key format starts with `gsk_`

### PDF Processing Errors
- Ensure PDF is valid and not corrupted
- Check file size (max 200MB per Streamlit config)
- Try with a smaller PDF first

### Model Loading Failures
- Verify internet connection
- Check API key validity
- Ensure Groq API is accessible

## Development

### Check Available Models
```bash
python chk_models.py
```

### Code Quality
- Uses logging for debugging
- Proper error handling with user feedback
- Secure API key management
- Type hints and docstrings

## Performance

- **Caching**: Models and tools are cached for faster subsequent requests
- **Streaming**: Chat responses stream in real-time
- **Auto-scroll**: Chat automatically scrolls to latest message

## License

Developed by Ahmad Afzal, Bahria University

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify API key and internet connection
3. Review logs for detailed error messages
