import streamlit as st

from components.tabs.sources import sources
from components.tabs.settings import settings
from utils.browser_settings import persist_settings_to_browser_storage


def sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 16px; padding: 4px 0;">
                <span style="font-size: 1.6rem; filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.4));">⚡</span>
                <div>
                    <div style="font-size: 1.35rem; font-weight: 800; letter-spacing: -0.02em; background: linear-gradient(135deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        NexusRAG
                    </div>
                    <div style="font-size: 0.65rem; color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em;">
                        Intelligence Console
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        tab1, tab2 = st.sidebar.tabs(["📁 Data Sources", "⚙️ Settings"])

        with tab1:
            sources()

        with tab2:
            settings()

        persist_settings_to_browser_storage()

        st.markdown(
            """
            <div style="margin-top: 32px; padding: 12px; border-radius: 8px; background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); text-align: center;">
                <div style="font-size: 0.74rem; color: #94A3B8; font-weight: 600; letter-spacing: 0.02em;">
                    ⚡ NexusRAG Engine v2.0
                </div>
                <div style="font-size: 0.64rem; color: #64748B; margin-top: 2px;">
                    Autonomous Document & Code Intelligence
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
