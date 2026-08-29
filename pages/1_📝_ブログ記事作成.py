import streamlit as st

from utils.gemini_client import generate_stream
from utils.ui import ensure_api_key, render_sidebar_settings

st.set_page_config(page_title="ブログ記事作成", page_icon="📝", layout="wide")

model, temperature = render_sidebar_settings()
ensure_api_key()

st.title("📝 ブログ記事作成")
st.caption("テーマやキーワードから、ブログ記事の下書きを生成します。")

with st.form("blog_form"):
    theme = st.text_input("テーマ・タイトル案 *", placeholder="例：初心者向けの家庭菜園の始め方")
    audience = st.text_input("想定読者（任意）", placeholder="例：これから家庭菜園を始めたい30代の会社員")
    keywords = st.text_input("含めたいキーワード（任意・カンマ区切り）", placeholder="例：プランター, 初心者, 野菜")

    col1, col2, col3 = st.columns(3)
    with col1:
        tone = st.selectbox("文体・トーン", ["親しみやすい", "フォーマル", "専門的", "カジュアル", "情熱的"])
    with col2:
        length = st.selectbox("目安の文字数", ["短め（800字程度）", "標準（1500字程度）", "長め（2500字程度）"], index=1)
    with col3:
        include_headings = st.checkbox("見出し構成を含める", value=True)

    extra = st.text_area("追加の指示（任意）", placeholder="例：体験談を交えて、最後にまとめを入れてほしい")
    submitted = st.form_submit_button("記事を生成する", type="primary")

if submitted:
    if not theme.strip():
        st.error("テーマ・タイトル案は必須です。")
    else:
        system_instruction = (
            "あなたはプロのブログライター兼SEOライターです。"
            "読者にとって分かりやすく、有益で、最後まで読みたくなる文章を書きます。"
            "指定がない限り日本語で、入力言語に合わせて出力してください。"
            "Markdown形式で見出しを整理して出力してください。"
        )
        prompt_parts = [
            f"以下の条件でブログ記事の下書きを作成してください。",
            f"テーマ: {theme}",
        ]
        if audience.strip():
            prompt_parts.append(f"想定読者: {audience}")
        if keywords.strip():
            prompt_parts.append(f"含めたいキーワード: {keywords}")
        prompt_parts.append(f"文体・トーン: {tone}")
        prompt_parts.append(f"目安の文字数: {length}")
        prompt_parts.append("見出し構成: " + ("あり（H2/H3を適切に使う）" if include_headings else "なし（本文のみ）"))
        if extra.strip():
            prompt_parts.append(f"追加の指示: {extra}")
        prompt = "\n".join(prompt_parts)

        st.divider()
        st.subheader("生成結果")
        st.write_stream(generate_stream(prompt, system_instruction, temperature, model))
