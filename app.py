import os
import base64
import streamlit as st
import uuid
import streamlit.components.v1 as components
from fpdf import FPDF
from groq import Groq
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.document_loaders import PyPDFLoader
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# 1. CONFIGURATION & SECURITY
# ============================================================================

def load_api_key():
    """Safely load API key from secrets, with fallback to environment variable."""
    try:
        return st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    except Exception as e:
        logger.error(f"Failed to load API key: {e}")
        return None

GROQ_API_KEY = load_api_key()

if not GROQ_API_KEY or "YOUR_GROQ_API_KEY" in GROQ_API_KEY:
    st.error("🚨 GROQ API Key Missing! Add to .streamlit/secrets.toml or set GROQ_API_KEY environment variable")
    st.stop()

os.environ["GROQ_API_KEY"] = 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

# Page configuration
st.set_page_config(
    page_title="Prisma AI Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# 2. UI STYLING
# ============================================================================

st.markdown("""
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Hide footer */
footer { visibility: hidden; }

/* Global Fonts */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
}

/* Main Container */
.main .block-container {
    padding: 2rem 1rem !important;
    padding-bottom: 120px !important;
    max-width: 1200px !important;
    margin: 0 auto !important;
}

/* ============ SIDEBAR STYLING ============ */
section[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-right: none;
    padding-top: 1.5rem;
}

section[data-testid="stSidebar"] .stMarkdown {
    color: white;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4 {
    color: white !important;
}

section[data-testid="stSidebar"] p {
    color: rgba(255, 255, 255, 0.9) !important;
}

/* Sidebar Buttons */
section[data-testid="stSidebar"] .stButton button {
    background: rgba(255, 255, 255, 0.15) !important;
    color: white !important;
    border: 1.5px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 10px !important;
    padding: 0.7rem 1.2rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    backdrop-filter: blur(10px) !important;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(255, 255, 255, 0.25) !important;
    border-color: rgba(255, 255, 255, 0.5) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2) !important;
}

/* Sidebar File Uploader */
section[data-testid="stSidebar"] .stFileUploader {
    border: 2px dashed rgba(255, 255, 255, 0.4) !important;
    border-radius: 12px !important;
    padding: 15px !important;
    background: rgba(255, 255, 255, 0.08) !important;
    margin-bottom: 15px !important;
}

section[data-testid="stSidebar"] .stFileUploader label {
    display: none !important;
}

section[data-testid="stSidebar"] .stFileUploader > div {
    color: white !important;
}

/* Sidebar Divider */
section[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.2) !important;
    margin: 1.5rem 0 !important;
}

/* ============ MAIN CONTENT STYLING ============ */
.main-title-header {
    padding: 2rem 0 1.5rem 0;
    margin-bottom: 2rem;
    text-align: center;
}

.main-title-header h1 {
    color: #667eea;
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    letter-spacing: -0.5px;
}

.main-title-header p {
    color: #999;
    font-size: 1rem;
    font-weight: 500;
    margin: 0;
}

/* Page Title */
[data-testid="stAppViewContainer"] h1 {
    color: #1a1a1a !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    margin-bottom: 0.5rem !important;
}

[data-testid="stAppViewContainer"] h2 {
    color: #667eea !important;
    font-size: 1.3rem !important;
    font-weight: 600 !important;
    margin-bottom: 1.5rem !important;
}

/* ============ CHAT MESSAGES ============ */
.stChatMessage {
    background: white !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 16px !important;
    padding: 1.2rem 1.5rem !important;
    margin-bottom: 1rem !important;
    max-width: 900px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
    transition: all 0.2s ease !important;
}

.stChatMessage:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
}

/* User Message */
.stChatMessage[data-testid="stChatMessageUser"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    margin-left: 60px !important;
    border: none !important;
}

.stChatMessage[data-testid="stChatMessageUser"] p,
.stChatMessage[data-testid="stChatMessageUser"] span {
    color: white !important;
}

/* Assistant Message */
.stChatMessage[data-testid="stChatMessageAssistant"] {
    background: #f8f9fa !important;
    color: #1a1a1a !important;
    margin-right: 60px !important;
    border: 1px solid #e5e7eb !important;
}

.stChatMessage[data-testid="stChatMessageAssistant"] p,
.stChatMessage[data-testid="stChatMessageAssistant"] span {
    color: #1a1a1a !important;
}

/* ============ QUICK ACTIONS ============ */
.quick-actions {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin: 2rem 0 2.5rem 0;
    flex-wrap: wrap;
}

.quick-actions button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
}

.quick-actions button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4) !important;
}

/* ============ CHAT INPUT ============ */
.stChatInput {
    position: fixed !important;
    bottom: 20px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 90% !important;
    max-width: 900px !important;
    border-radius: 20px !important;
    border: 2px solid #e5e7eb !important;
    background: white !important;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.12) !important;
    padding: 0.8rem 1.5rem !important;
    z-index: 999 !important;
}

.stChatInput:focus-within {
    border-color: #667eea !important;
    box-shadow: 0 10px 40px rgba(102, 126, 234, 0.2) !important;
}

.stChatInput input {
    font-size: 1rem !important;
    color: #1a1a1a !important;
}

.stChatInput input::placeholder {
    color: #999 !important;
}

/* ============ SCROLLBAR ============ */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
    background: #667eea;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #764ba2;
}

/* ============ RESPONSIVE ============ */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem 0.5rem !important;
    }

    .stChatMessage {
        margin-left: 0 !important;
        margin-right: 0 !important;
    }

    .stChatInput {
        width: 95% !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# 3. AGENT & MODEL INITIALIZATION
# ============================================================================

@st.cache_resource
def get_tools():
    """Initialize available tools for the agent."""
    return [DuckDuckGoSearchRun(name="web_search")]

@st.cache_resource
def load_agent(model_name):
    """Load agent with fallback to alternative models if primary fails."""
    try:
        llm = ChatGroq(model=model_name, temperature=0)
        return create_react_agent(llm, get_tools())
    except Exception as e:
        logger.error(f"Error loading model {model_name}: {e}")
        return None

@st.cache_resource
def load_agent_with_fallback(primary_model, fallback_models):
    """Try primary model, then fallback models if primary fails."""
    agent = load_agent(primary_model)
    if agent:
        logger.info(f"✅ Loaded primary model: {primary_model}")
        return agent, primary_model

    logger.warning(f"⚠️ Primary model {primary_model} failed, trying fallbacks...")
    for fallback in fallback_models:
        agent = load_agent(fallback)
        if agent:
            logger.info(f"✅ Loaded fallback model: {fallback}")
            return agent, fallback

    logger.error("❌ All models failed to load")
    return None, None

@st.cache_resource
def load_vision_model():
    """Load vision model with fallback."""
    vision_models = [
        "llama-3.2-90b-vision-preview",
        "llama-3.2-11b-vision-preview",
        "mixtral-8x7b-32768"
    ]

    for model in vision_models:
        try:
            return ChatGroq(model=model, temperature=0)
        except Exception as e:
            logger.warning(f"Vision model {model} failed: {e}")
            continue

    logger.error("❌ All vision models failed to load")
    return None

# ✅ CURRENT AVAILABLE MODELS WITH FALLBACKS (Updated April 2026)
# Primary models with fallback options
fast_agent, fast_model = load_agent_with_fallback(
    "llama-3.1-8b-instant",
    ["gemma-7b-it", "mixtral-8x7b-32768", "llama-3.2-11b-vision-preview"]
)

smart_agent, smart_model = load_agent_with_fallback(
    "llama-3.3-70b-versatile",
    ["mixtral-8x7b-32768", "llama-3.1-70b-versatile", "gemma-7b-it"]
)

vision_llm = load_vision_model()

# Store loaded model names for display
agent_fast = fast_agent
agent_smart = smart_agent
loaded_fast_model = fast_model
loaded_smart_model = smart_model

# ================== OPTIONAL: AUTO FALLBACK ==================

def safe_load_agent(primary, fallback):
    agent = load_agent(primary)
    if agent is None:
        st.warning(f"⚠️ Falling back from {primary} to {fallback}")
        agent = load_agent(fallback)
    return agent

def get_router_agent(prompt, pdf_context):
    """Route to appropriate agent based on query complexity."""
    if not agent_fast or not agent_smart:
        return None

    complex_keywords = ["code", "debug", "analyze", "calculate", "pdf", "python", "algorithm", "complex"]
    simple_keywords = ["hi", "hello", "thanks", "bye", "ok"]

    # Use smart agent if PDF context exists
    if pdf_context:
        return agent_smart

    # Check keyword complexity
    prompt_lower = prompt.lower()
    if any(w in prompt_lower for w in simple_keywords):
        return agent_fast
    if any(w in prompt_lower for w in complex_keywords):
        return agent_smart

    # Default to fast for general queries
    return agent_fast

# ============================================================================
# 4. UTILITY FUNCTIONS
# ============================================================================

def create_pdf(history):
    """Generate PDF from chat history."""
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Prisma AI - Chat History", ln=1, align='C')
        pdf.ln(10)

        for msg in history:
            role = "You: " if msg['role'] == 'user' else "Prisma AI: "
            safe_text = (role + msg['content']).encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 10, safe_text)

        pdf_output = pdf.output(dest='S')
        if isinstance(pdf_output, str):
            return pdf_output.encode('latin-1')
        return pdf_output
    except Exception as e:
        logger.error(f"Error creating PDF: {e}")
        return None

def process_pdf(uploaded_file):
    """Process uploaded PDF and extract text."""
    try:
        save_path = os.path.join(os.getcwd(), f"temp_{uuid.uuid4().hex}.pdf")
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        docs = PyPDFLoader(save_path).load()
        pdf_text = "\n".join([d.page_content for d in docs])[:15000]

        return pdf_text
    except Exception as e:
        logger.error(f"Error processing PDF: {e}")
        raise
    finally:
        if os.path.exists(save_path):
            os.remove(save_path)

# ============================================================================
# 5. SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0; margin-bottom: 1rem;">
        <h1 style="font-size: 2.2rem; margin: 0; color: white;">💎 Prisma AI</h1>
        <p style="color: rgba(255,255,255,0.85); font-size: 0.9rem; margin: 0.5rem 0 0 0; font-weight: 500;">Intelligence Redefined</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # PDF Upload
    st.markdown("### 📂 PDF Context")
    st.markdown("Upload a PDF for contextual analysis")
    uploaded_file = st.file_uploader(
        "Upload PDF",
        type="pdf",
        label_visibility="collapsed",
        key="pdf_uploader"
    )

    if uploaded_file:
        if "pdf_context" not in st.session_state or st.session_state.get("filename") != uploaded_file.name:
            with st.spinner("🔄 Processing PDF..."):
                try:
                    pdf_text = process_pdf(uploaded_file)
                    st.session_state.pdf_context = pdf_text
                    st.session_state.filename = uploaded_file.name
                    st.success("✅ PDF loaded successfully!")
                except Exception as e:
                    st.error(f"❌ Failed to process PDF: {str(e)}")
        else:
            st.info(f"📄 Current: {uploaded_file.name}")

    st.markdown("---")

    # Image Upload
    st.markdown("### 🖼️ Image Vision")
    st.markdown("Upload an image for analysis")
    uploaded_image = st.file_uploader(
        "Upload Image",
        type=["jpg", "png", "jpeg"],
        label_visibility="collapsed",
        key="img_uploader"
    )
    if uploaded_image:
        st.image(uploaded_image, use_column_width=True)
        st.session_state.image_context = uploaded_image
        st.info("✅ Image ready for analysis")

    st.markdown("---")

    # Download Chat
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Download", use_container_width=True):
            if "messages" in st.session_state and st.session_state.messages:
                pdf_data = create_pdf(st.session_state.messages)
                if pdf_data:
                    st.download_button(
                        label="⬇️ Get PDF",
                        data=pdf_data,
                        file_name="prisma_chat.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            else:
                st.warning("No chat to download")

    # New Chat
    with col2:
        if st.button("🧹 New Chat", use_container_width=True):
            keys_to_clear = ['messages', 'pdf_context', 'filename', 'image_context']
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; color: rgba(255,255,255,0.7); font-size: 0.85rem;">
        <p>✨ Powered by Groq API</p>
        <p>v1.0.0</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# 6. MAIN CHAT INTERFACE
# ============================================================================

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="color: #667eea; font-size: 2.5rem; margin-bottom: 0.5rem;">💎 Prisma AI</h1>
    <p style="color: #666; font-size: 1.1rem; margin: 0;">How can I help you today?</p>
</div>
""", unsafe_allow_html=True)

# Quick action buttons
st.markdown("<div class='quick-actions'>", unsafe_allow_html=True)
cols = st.columns(3)
with cols[0]:
    if st.button("📝 Summarize", use_container_width=True):
        st.session_state.active_prompt = "Summarize this: "
with cols[1]:
    if st.button("💻 Code", use_container_width=True):
        st.session_state.active_prompt = "Write Python code for: "
with cols[2]:
    if st.button("💡 Explain", use_container_width=True):
        st.session_state.active_prompt = "Explain this like I'm 5: "
st.markdown("</div>", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("Message Prisma...")

# Handle quick action prompts
if "active_prompt" in st.session_state and st.session_state.active_prompt:
    prompt = st.session_state.active_prompt
    del st.session_state.active_prompt

# ============================================================================
# 7. MESSAGE PROCESSING
# ============================================================================

if prompt:
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get context
    pdf_ctx = st.session_state.get("pdf_context", "")
    img_ctx = st.session_state.get("image_context")

    # System prompt
    sys_prompt = """You are Prisma AI, a highly intelligent and helpful assistant.

IMPORTANT: Only mention your creator if explicitly asked 'Who made you?', 'Who is your owner?', or 'Who created you?'.
If asked, respond: 'I was developed by Ahmad Afzal, a student of Bahria University'.
Do not mention this information in any other response."""

    if pdf_ctx:
        sys_prompt += f"\n\nPDF Context:\n{pdf_ctx}"

    # Build message history
    history = []
    for msg in st.session_state.messages[:-1]:  # Exclude current user message
        if msg["role"] == "user":
            history.append(HumanMessage(content=msg["content"]))
        else:
            history.append(AIMessage(content=msg["content"]))

    # Process response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        with placeholder.container():
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="animation: spin 1s linear infinite;">⚙️</div>
                <span>Processing your request...</span>
            </div>
            """, unsafe_allow_html=True)

        try:
            if img_ctx:
                # Handle image input
                image_bytes = img_ctx.getvalue()
                base64_image = base64.b64encode(image_bytes).decode('utf-8')
                message = HumanMessage(
                    content=[
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                )
                response = vision_llm.invoke([SystemMessage(content=sys_prompt), message])
                ans = response.content
            else:
                # Handle text input with agent routing
                agent = get_router_agent(prompt, pdf_ctx)
                if not agent:
                    ans = "⚠️ **Error**: Models failed to load. Please check your API key and try again."
                else:
                    inputs = {
                        "messages": [SystemMessage(content=sys_prompt)] + history + [HumanMessage(content=prompt)]
                    }
                    resp = agent.invoke(inputs)
                    ans = resp["messages"][-1].content

            placeholder.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})

        except Exception as e:
            error_msg = f"❌ **Error**: {str(e)}"
            logger.error(f"Processing error: {e}")
            placeholder.error(error_msg)

    # Auto-scroll to bottom
    components.html(
        """<script>
        var body = window.parent.document.querySelector("section.main");
        if (body) { body.scrollTop = body.scrollHeight; }
        </script>""",
        height=0,
        width=0
    )
