import streamlit as st

from utils.gemini_client import generate_stream
from utils.ui import ensure_api_key, render_sidebar_settings

st.set_page_config(page_title="文章要約", page_icon="📄", layout="wide")

model, temperature = render_sidebar_settings()
ensure_api_key()

st.title("📄 文章要約")
st.caption("長文を、指定した形式・長さで要約します。")

with st.form("summary_form"):
    source_text = st.text_area("元の文章 *", height=280, placeholder="要約したい文章を貼り付けてください")

    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox("要約の形式", ["箇条書き", "一段落の文章", "一言（1文で）"])
    with col2:
        length = st.selectbox("要約の長さ", ["短め", "標準", "詳しめ"], index=1)

    bullet_count = None
    if style == "箇条書き":
        bullet_count = st.slider("箇条書きの項目数の目安", 3, 10, 5)

    submitted = st.form_submit_button("要約する", type="primary")

if submitted:
    if not source_text.strip():
        st.error("元の文章を入力してください。")
    else:
        system_instruction = (
            "あなたは優秀な編集者です。文章の要点を正確に捉え、過不足なく要約します。"
            "元の文章と同じ言語で出力してください。"
        )
        prompt_parts = [
            "以下の文章を要約してください。",
            f"要約の形式: {style}",
            f"要約の長さ: {length}",
        ]
        if bullet_count:
            prompt_parts.append(f"箇条書きの項目数: 目安{bullet_count}個程度")
        prompt_parts.append("---元の文章---")
        prompt_parts.append(source_text)
        prompt = "\n".join(prompt_parts)

        st.divider()
        st.subheader("要約結果")
        st.write_stream(generate_stream(prompt, system_instruction, temperature, model))
