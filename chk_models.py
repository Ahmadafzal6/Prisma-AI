"""
Utility script to check available models from Groq API.
Requires GROQ_API_KEY environment variable or .streamlit/secrets.toml
"""
import requests
import os
import sys

def get_api_key():
    """Load API key from environment or secrets."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("GROQ_API_KEY")
        except:
            pass
    return api_key

def fetch_models():
    """Fetch and display available models from Groq API."""
    api_key = get_api_key()

    if not api_key or "gsk_" not in api_key:
        print("❌ Error: GROQ_API_KEY not found or invalid")
        print("   Set GROQ_API_KEY environment variable or add to .streamlit/secrets.toml")
        sys.exit(1)

    url = "https://api.groq.com/openai/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    print("🔄 Fetching available models from Groq...")

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            models = data.get('data', [])

            if models:
                print("\n✅ Available Models:")
                print("-" * 50)
                for model in models:
                    model_id = model.get('id', 'Unknown')
                    print(f"  • {model_id}")
                print("-" * 50)
                print(f"\nTotal: {len(models)} models available\n")
            else:
                print("⚠️  No models found in response")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Response: {response.text}")
            sys.exit(1)

    except requests.exceptions.Timeout:
        print("❌ Error: Request timeout. Check your internet connection.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_models()
