# 🔧 TROUBLESHOOTING - Model Loading Issues

**Issue**: Models failing to load
**Error**: "Failed to load llama-3.1-8b-instant — model may be unavailable on Groq"

## Possible Causes

1. **Invalid API Key**
   - Check `.streamlit/secrets.toml` has correct key
   - Key should start with `gsk_`
   - Verify key is not expired

2. **API Rate Limiting**
   - Too many requests
   - Wait a few minutes and try again

3. **Model Availability**
   - Models may be temporarily unavailable
   - Check https://console.groq.com/docs/models for current list

4. **Network Issues**
   - Check internet connection
   - Verify Groq API is accessible

## How to Check Available Models

Run this command to see what models are available:

```bash
python chk_models.py
```

This will list all available models on your account.

## Fallback Models to Try

If the current models fail, try these alternatives:

```python
# Option 1: Use mixtral (if still available)
agent_fast = load_agent("mixtral-8x7b-32768")

# Option 2: Use gemma
agent_fast = load_agent("gemma-7b-it")

# Option 3: Use whisper for audio
agent_fast = load_agent("whisper-large-v3")
```

## Steps to Fix

1. **Verify API Key**
   ```bash
   echo $GROQ_API_KEY
   ```

2. **Check Available Models**
   ```bash
   python chk_models.py
   ```

3. **Update app.py with Available Models**
   - Edit lines 344-346 in app.py
   - Replace model names with ones from step 2

4. **Restart the App**
   ```bash
   streamlit run app.py
   ```

## Example Fix

If `chk_models.py` shows these models available:
- gemma-7b-it
- mixtral-8x7b-32768
- whisper-large-v3

Update app.py to:
```python
agent_fast = load_agent("gemma-7b-it")
agent_smart = load_agent("mixtral-8x7b-32768")
```

## Need Help?

1. Run `python chk_models.py` to see available models
2. Update model names in app.py (lines 344-346)
3. Restart the app
4. Check https://console.groq.com/docs/models for latest info

---

**Status**: Troubleshooting guide created
**Next**: Run `python chk_models.py` to identify available models
