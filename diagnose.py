#!/usr/bin/env python3
"""
Diagnostic tool to test Groq API connection and available models
"""
import os
import sys

def test_api_connection():
    """Test if API key is valid and models are accessible."""

    print("=" * 60)
    print("🔍 PRISMA AI PRO - API DIAGNOSTIC TOOL")
    print("=" * 60)

    # Check API key
    print("\n1️⃣ Checking API Key...")
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("❌ GROQ_API_KEY not found in environment")
        print("   Set it with: export GROQ_API_KEY='your_key_here'")
        return False

    if not api_key.startswith("gsk_"):
        print("❌ API Key format invalid (should start with 'gsk_')")
        return False

    print(f"✅ API Key found: {api_key[:20]}...")

    # Test Groq connection
    print("\n2️⃣ Testing Groq API Connection...")
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        print("✅ Groq client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize Groq client: {e}")
        return False

    # List available models
    print("\n3️⃣ Fetching Available Models...")
    try:
        models = client.models.list()
        print(f"✅ Found {len(models.data)} available models:")
        print("-" * 60)
        for model in models.data:
            print(f"  • {model.id}")
        print("-" * 60)
    except Exception as e:
        print(f"❌ Failed to fetch models: {e}")
        return False

    # Test model loading
    print("\n4️⃣ Testing Model Loading...")
    test_models = [
        "llama-3.1-8b-instant",
        "llama-3.3-70b-versatile",
        "gemma-7b-it",
        "mixtral-8x7b-32768"
    ]

    for model_name in test_models:
        try:
            from langchain_groq import ChatGroq
            llm = ChatGroq(model=model_name, temperature=0)
            print(f"✅ {model_name} - OK")
        except Exception as e:
            print(f"❌ {model_name} - FAILED: {str(e)[:50]}")

    print("\n" + "=" * 60)
    print("✅ DIAGNOSTIC COMPLETE")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_api_connection()
    sys.exit(0 if success else 1)
