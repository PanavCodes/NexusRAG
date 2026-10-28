import streamlit as st


def set_page_config():
    if "sidebar_state" not in st.session_state:
        st.session_state["sidebar_state"] = "expanded"

    st.set_page_config(
        page_title="NexusRAG | AI Repository & Document Intelligence",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state=st.session_state["sidebar_state"],
    )

    # Modern Dark Theme Glassmorphism and UI Enhancements
    st.markdown(
        r"""
    <style>
    /* Hide default header buttons */
    .stDeployButton, footer {
        visibility: hidden !important;
        display: none !important;
    }

    /* Modern tab styling */
    button[data-baseweb="tab"] {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        border-radius: 8px !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    button[data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.05) !important;
    }

    /* Container Glassmorphism Cards */
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        background: rgba(17, 24, 39, 0.5) !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
    }

    /* Primary and Form Buttons */
    .stButton > button, .stFormSubmitButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        letter-spacing: 0.01em !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button[kind="primary"], .stFormSubmitButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #4F46E5 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3) !important;
    }

    .stButton > button[kind="primary"]:hover, .stFormSubmitButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.45) !important;
    }

    /* Expander modern styles */
    div[data-testid="stExpander"] {
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        background: rgba(15, 23, 42, 0.3) !important;
        overflow: hidden !important;
    }

    /* Streamlit Status Badge */
    div[data-testid="stStatusWidget"] {
        border-radius: 8px !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
    }

    /* Input focus styling */
    input:focus, textarea:focus {
        border-color: #38BDF8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
