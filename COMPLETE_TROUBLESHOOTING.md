# 🔧 COMPLETE TROUBLESHOOTING GUIDE

**Issue**: Models failing to load with error "Models failed to load. Please check your API key and try again."

---

## 🚨 Quick Diagnosis

Run this command to diagnose the issue:

```bash
python diagnose.py
```

This will check:
- ✅ API key validity
- ✅ Groq connection
- ✅ Available models
- ✅ Model loading capability

---

## 🔍 Step-by-Step Troubleshooting

### Step 1: Verify API Key

**Check if API key is set**:
```bash
echo $GROQ_API_KEY
```

**Expected output**: Should show a key starting with `gsk_`

**If empty or wrong**:
1. Go to https://console.groq.com
2. Create/get your API key
3. Add to `.streamlit/secrets.toml`:
   ```toml
   GROQ_API_KEY = "gsk_your_actual_key_here"
   ```

### Step 2: Verify API Key Format

API key must:
- ✅ Start with `gsk_`
- ✅ Be at least 50 characters long
- ✅ Not contain spaces
- ✅ Not be expired

### Step 3: Check Available Models

Run the diagnostic:
```bash
python diagnose.py
```

This will show:
- Your API key status
- All available models on your account
- Which models can be loaded

### Step 4: Update Model Names

If certain models aren't available, update `app.py` lines 360-370:

```python
# Replace with models from diagnose.py output
fast_agent, fast_model = load_agent_with_fallback(
    "YOUR_AVAILABLE_MODEL_HERE",
    ["FALLBACK_1", "FALLBACK_2"]
)

smart_agent, smart_model = load_agent_with_fallback(
    "YOUR_AVAILABLE_MODEL_HERE",
    ["FALLBACK_1", "FALLBACK_2"]
)
```

### Step 5: Restart App

```bash
streamlit run app.py
```

---

## 🆘 Common Issues & Solutions

### Issue: "API Key Missing"
**Solution**:
1. Create `.streamlit/secrets.toml`
2. Add: `GROQ_API_KEY = "gsk_..."`
3. Restart app

### Issue: "Invalid API Key"
**Solution**:
1. Verify key starts with `gsk_`
2. Check for typos
3. Get new key from https://console.groq.com

### Issue: "Model Not Found"
**Solution**:
1. Run `python diagnose.py`
2. Use models from the list
3. Update app.py with available models

### Issue: "Connection Timeout"
**Solution**:
1. Check internet connection
2. Verify Groq API is accessible
3. Try again in a few minutes

### Issue: "Rate Limited"
**Solution**:
1. Wait 5-10 minutes
2. Try again
3. Check Groq console for usage limits

---

## 📋 Diagnostic Checklist

- [ ] API key is set in `.streamlit/secrets.toml`
- [ ] API key starts with `gsk_`
- [ ] API key is not expired
- [ ] Internet connection is working
- [ ] Groq API is accessible
- [ ] At least one model is available
- [ ] Model names in app.py match available models

---

## 🎯 What to Do Next

1. **Run diagnostic**:
   ```bash
   python diagnose.py
   ```

2. **Check output** for available models

3. **Update app.py** if needed with available models

4. **Restart app**:
   ```bash
   streamlit run app.py
   ```

5. **Test** by sending a message

---

## 📞 Still Having Issues?

1. **Check logs**: Look for error messages in terminal
2. **Run diagnostic**: `python diagnose.py`
3. **Verify API key**: https://console.groq.com
4. **Check models**: https://console.groq.com/docs/models
5. **Try fallback models**: gemma-7b-it, mixtral-8x7b-32768

---

## 🔗 Useful Links

- **Groq Console**: https://console.groq.com
- **API Documentation**: https://console.groq.com/docs/api
- **Available Models**: https://console.groq.com/docs/models
- **Troubleshooting**: https://console.groq.com/docs/troubleshooting

---

**Status**: Troubleshooting guide complete
**Next**: Run `python diagnose.py` to identify the issue
