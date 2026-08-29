import streamlit as st

from utils.gemini_client import generate_stream
from utils.ui import ensure_api_key, render_sidebar_settings

st.set_page_config(page_title="校正リライト", page_icon="✨", layout="wide")

model, temperature = render_sidebar_settings()
ensure_api_key()

st.title("✨ 校正・リライト")
st.caption("誤字脱字の修正や、文章のトーン変換を行います。")

PURPOSE_OPTIONS = [
    "誤字脱字・文法チェック",
    "より丁寧な表現に",
    "より簡潔に",
    "よりカジュアルに",
    "ビジネス文書らしく",
    "読みやすく整理（改行・構成調整）",
]

with st.form("rewrite_form"):
    source_text = st.text_area("元の文章 *", height=280, placeholder="校正・リライトしたい文章を貼り付けてください")
    purposes = st.multiselect("目的（複数選択可） *", PURPOSE_OPTIONS, default=["誤字脱字・文法チェック"])
    explain_changes = st.checkbox("主な変更点の説明を付ける", value=False)
    submitted = st.form_submit_button("校正・リライトする", type="primary")

if submitted:
    if not source_text.strip():
        st.error("元の文章を入力してください。")
    elif not purposes:
        st.error("目的を1つ以上選択してください。")
    else:
        system_instruction = (
            "あなたはプロの編集者・校正者です。文章の意味やニュアンスを保ちながら、"
            "指定された目的に沿って文章を改善します。元の文章と同じ言語で出力してください。"
        )
        prompt_parts = [
            "以下の文章を、次の目的に沿ってリライトしてください。",
            f"目的: {'、'.join(purposes)}",
        ]
        if explain_changes:
            prompt_parts.append(
                "出力は「## 修正後の文章」と「## 主な変更点」の2つの見出しに分けてください。"
            )
        else:
            prompt_parts.append("修正後の文章のみを出力してください（説明は不要）。")
        prompt_parts.append("---元の文章---")
        prompt_parts.append(source_text)
        prompt = "\n".join(prompt_parts)

        st.divider()
        st.subheader("結果")
        st.write_stream(generate_stream(prompt, system_instruction, temperature, model))
