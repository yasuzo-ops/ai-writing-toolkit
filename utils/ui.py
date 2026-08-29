"""ページ共通のUIコンポーネント。"""
import streamlit as st

from utils.gemini_client import AVAILABLE_MODELS, DEFAULT_MODEL, get_api_key


def render_sidebar_settings():
    """モデル選択・温度設定・APIキー入力をサイドバーに描画し、(model, temperature) を返す。"""
    with st.sidebar:
        st.markdown("### ⚙️ 生成設定")
        model = st.selectbox(
            "モデル",
            AVAILABLE_MODELS,
            index=AVAILABLE_MODELS.index(DEFAULT_MODEL),
            key="selected_model",
            help="pro-preview は高品質・低速、flash はバランス型、flash-lite は高速・軽量です。",
        )
        temperature = st.slider(
            "創造性 (temperature)",
            0.0, 1.5, 0.7, 0.1,
            key="selected_temperature",
            help="低いほど堅実・一貫的、高いほど独創的な文章になります。",
        )
        st.divider()
        _render_api_key_box()
    return model, temperature


def _render_api_key_box():
    st.markdown("### 🔑 Gemini APIキー")
    current = get_api_key()
    if current:
        st.success("APIキー設定済み")
        with st.expander("キーを変更する"):
            new_key = st.text_input("新しいAPIキー", type="password", key="api_key_input_change")
            if st.button("更新", key="update_api_key_btn") and new_key:
                st.session_state["gemini_api_key"] = new_key
                st.rerun()
    else:
        st.warning("APIキーが未設定です")
        new_key = st.text_input("Gemini APIキーを入力", type="password", key="api_key_input_new")
        if st.button("設定する", key="set_api_key_btn") and new_key:
            st.session_state["gemini_api_key"] = new_key
            st.rerun()
        st.caption(
            "環境変数 `GEMINI_API_KEY` か `.streamlit/secrets.toml` に設定しておくと、"
            "毎回の入力が不要になります。"
        )


def ensure_api_key():
    """APIキーが無ければ案内を出してページの実行を止める。"""
    key = get_api_key()
    if not key:
        st.info("👈 サイドバーからGemini APIキーを設定してください。")
        st.stop()
    return key
