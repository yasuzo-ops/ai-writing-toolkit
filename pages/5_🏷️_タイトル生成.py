import streamlit as st

from utils.gemini_client import generate_stream
from utils.ui import ensure_api_key, render_sidebar_settings

st.set_page_config(page_title="タイトル生成", page_icon="🏷️", layout="wide")

model, temperature = render_sidebar_settings()
ensure_api_key()

st.title("🏷️ タイトル・キャッチコピー生成")
st.caption("記事内容から、複数のタイトル・キャッチコピー候補を生成します。")

STYLE_OPTIONS = [
    "SEOを意識した検索されやすい表現",
    "好奇心を刺激する表現",
    "数字を使った具体性のある表現",
    "簡潔で分かりやすい表現",
    "エモーショナル・感情に訴える表現",
]

with st.form("title_form"):
    content = st.text_area("記事の内容・要約 *", height=200, placeholder="タイトルを付けたい記事の内容や要約を入力してください")
    count = st.slider("生成する候補数", 3, 10, 5)
    styles = st.multiselect("重視したいスタイル（任意・複数選択可）", STYLE_OPTIONS)
    submitted = st.form_submit_button("タイトルを生成する", type="primary")

if submitted:
    if not content.strip():
        st.error("記事の内容・要約を入力してください。")
    else:
        system_instruction = (
            "あなたは読者の目を引くタイトルを作るプロのコピーライターです。"
            "入力内容と同じ言語で出力してください。出力は番号付きの箇条書きのみとしてください。"
        )
        prompt_parts = [
            f"以下の内容に対して、タイトル・キャッチコピー候補を{count}個生成してください。",
        ]
        if styles:
            prompt_parts.append(f"重視するスタイル: {'、'.join(styles)}")
        prompt_parts.append("---内容---")
        prompt_parts.append(content)
        prompt = "\n".join(prompt_parts)

        st.divider()
        st.subheader("生成結果")
        st.write_stream(generate_stream(prompt, system_instruction, temperature, model))
