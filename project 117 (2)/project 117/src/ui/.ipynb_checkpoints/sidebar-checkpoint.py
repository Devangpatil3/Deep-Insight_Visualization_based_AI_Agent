import streamlit as st
from config.models import TOGETHER_MODELS, MODEL_DESCRIPTIONS

def setup_sidebar():
    """Setup sidebar with API keys and model configuration"""
    
    # Initialize session state
    if 'together_api_key' not in st.session_state:
        st.session_state.together_api_key = ''
    if 'e2b_api_key' not in st.session_state:
        st.session_state.e2b_api_key = ''
    if 'model_name' not in st.session_state:
        st.session_state.model_name = TOGETHER_MODELS["Meta-Llama 3.1 405B"]

    with st.sidebar:
        st.header("🔐 API Configuration")
        
        # Together AI API Key
        st.subheader("Together AI")
        st.session_state.together_api_key = st.text_input(
            "API Key", 
            type="password",
            key="together_key",
            help="Enter your Together AI API key"
        )
        st.info("💡 Everyone gets a free $1 credit from Together AI")
        st.markdown("[Get API Key](https://api.together.ai/signin)")
        
        # E2B API Key
        st.subheader("E2B Code Interpreter")
        st.session_state.e2b_api_key = st.text_input(
            "E2B API Key", 
            type="password",
            key="e2b_key",
            help="Enter your E2B API key for code execution"
        )
        st.markdown("[Get E2B API Key](https://e2b.dev/docs/legacy/getting-started/api-key)")
        
        # Model Selection
        st.subheader("🤖 Model Selection")
        selected_model = st.selectbox(
            "Choose AI Model",
            list(TOGETHER_MODELS.keys()),
            index=0,
            help="Select the AI model for data analysis"
        )
        st.session_state.model_name = TOGETHER_MODELS[selected_model]
        
        # Show model description
        if selected_model in MODEL_DESCRIPTIONS:
            st.info(f"ℹ️ {MODEL_DESCRIPTIONS[selected_model]}")
        
        # API Status Check
        st.subheader("📊 Status")
        if st.session_state.together_api_key:
            st.success("✅ Together AI: Connected")
        else:
            st.error("❌ Together AI: Not connected")
            
        if st.session_state.e2b_api_key:
            st.success("✅ E2B: Connected")
        else:
            st.error("❌ E2B: Not connected")
        
        # Additional Settings
        with st.expander("⚙️ Advanced Settings"):
            st.slider("Temperature", 0.0, 1.0, 0.7, 0.1, key="temperature")
            st.slider("Max Tokens", 1000, 8000, 4000, 500, key="max_tokens")
            st.checkbox("Enable Debug Mode", key="debug_mode")