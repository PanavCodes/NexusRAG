import streamlit as st


def set_page_header():
    col1, col2 = st.columns([0.65, 0.35])
    with col1:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 2px;">
                <div style="font-size: 2.3rem; font-weight: 800; letter-spacing: -0.03em; background: linear-gradient(135deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    NexusRAG
                </div>
                <span style="font-size: 0.72rem; font-weight: 600; padding: 3px 10px; border-radius: 9999px; background: rgba(56, 189, 248, 0.12); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.25);">
                    v2.0 • AI Multi-Engine
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption(
            "High-Performance Autonomous Retrieval-Augmented Generation for Codebases, Excel Workbooks, Documents & Web."
        )

    with col2:
        provider = st.session_state.get("llm_provider", "Google Gemini")
        if provider == "OpenRouter (Free Models)":
            model_name = st.session_state.get("openrouter_model", "cohere/north-mini-code:free")
            badge_color = "#34D399"
            badge_bg = "rgba(52, 211, 153, 0.12)"
            badge_border = "rgba(52, 211, 153, 0.25)"
            provider_label = "OpenRouter Free"
        else:
            model_name = st.session_state.get("gemini_model", "gemini-3.5-flash-lite")
            badge_color = "#818CF8"
            badge_bg = "rgba(129, 140, 248, 0.12)"
            badge_border = "rgba(129, 140, 248, 0.25)"
            provider_label = "Google Gemini"

        emb_backend = st.session_state.get("embedding_backend", "OpenRouter")
        st.markdown(
            f"""
            <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 4px; padding-top: 4px;">
                <div style="display: flex; align-items: center; gap: 6px; font-size: 0.78rem; color: {badge_color}; background: {badge_bg}; border: 1px solid {badge_border}; border-radius: 6px; padding: 4px 10px;">
                    <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: {badge_color}; box-shadow: 0 0 6px {badge_color};"></span>
                    <strong>{provider_label}:</strong> {model_name}
                </div>
                <div style="font-size: 0.72rem; color: #94A3B8;">
                    Embeddings: <span style="color: #E2E8F0; font-weight: 600;">{emb_backend}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<hr style='margin: 8px 0 16px 0; border: none; border-bottom: 1px solid rgba(255, 255, 255, 0.08);' />", unsafe_allow_html=True)
