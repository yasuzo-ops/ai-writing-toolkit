import streamlit as st

from utils.gemini_client import generate_stream
from utils.ui import ensure_api_key, render_sidebar_settings

st.set_page_config(page_title="翻訳", page_icon="🌐", layout="wide")

model, temperature = render_sidebar_settings()
ensure_api_key()

st.title("🌐 翻訳")
st.caption("自然な訳文を、指定した言語・トーンで生成します。")

LANGUAGES = ["日本語", "英語", "中国語（簡体字）", "中国語（繁体字）", "韓国語", "フランス語", "スペイン語", "ドイツ語", "その他（自由入力）"]

with st.form("translate_form"):
    source_text = st.text_area("原文 *", height=250, placeholder="翻訳したい文章を貼り付けてください")

    col1, col2 = st.columns(2)
    with col1:
        target_language = st.selectbox("翻訳先言語", LANGUAGES)
        if target_language == "その他（自由入力）":
            target_language = st.text_input("翻訳先言語を入力", placeholder="例：タイ語")
    with col2:
        tone = st.selectbox("トーン", ["自然な文章", "フォーマル", "カジュアル", "ビジネス"])

    natural_priority = st.checkbox("直訳よりも自然さを優先する", value=True)
    submitted = st.form_submit_button("翻訳する", type="primary")

if submitted:
    if not source_text.strip():
        st.error("原文を入力してください。")
    elif not target_language.strip():
        st.error("翻訳先言語を入力してください。")
    else:
        system_instruction = (
            "あなたはプロの翻訳者です。文脈やニュアンスを正確に汲み取り、"
            "指定された言語・トーンに合わせた訳文のみを出力してください（説明や注釈は不要）。"
        )
        prompt_parts = [
            f"以下の文章を{target_language}に翻訳してください。",
            f"トーン: {tone}",
            "翻訳方針: " + ("直訳よりも自然な表現を優先する" if natural_priority else "原文の構造や表現に忠実に翻訳する"),
            "---原文---",
            source_text,
        ]
        prompt = "\n".join(prompt_parts)

        st.divider()
        st.subheader("翻訳結果")
        st.write_stream(generate_stream(prompt, system_instruction, temperature, model))
