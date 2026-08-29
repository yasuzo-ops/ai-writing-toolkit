import streamlit as st

from utils.gemini_client import generate_stream
from utils.ui import ensure_api_key, render_sidebar_settings

st.set_page_config(page_title="メール返信作成", page_icon="📧", layout="wide")

model, temperature = render_sidebar_settings()
ensure_api_key()

st.title("📧 メール返信作成")
st.caption("受信したメールの内容から、適切なトーンの返信文を生成します。")

with st.form("email_form"):
    original_email = st.text_area("受信したメール本文 *", height=200, placeholder="相手から届いたメールの本文を貼り付けてください")
    key_points = st.text_area("返信で伝えたい要点 *", height=120, placeholder="例：来週火曜14時なら対応可能、資料は今週中に送付予定")

    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("トーン", ["丁寧・ビジネス", "フォーマル・かしこまった", "カジュアル・親しみやすい", "謝罪・お詫び"])
    with col2:
        signature = st.text_input("署名・自分の名前（任意）", placeholder="例：株式会社サンプル 山田")

    submitted = st.form_submit_button("返信文を生成する", type="primary")

if submitted:
    if not original_email.strip() or not key_points.strip():
        st.error("受信メール本文と、伝えたい要点は必須です。")
    else:
        system_instruction = (
            "あなたは優秀なビジネスアシスタントです。"
            "受信メールの文脈を踏まえ、失礼のない自然な返信メールを作成します。"
            "受信メールと同じ言語で返信を作成してください。"
            "件名は不要で、本文のみを出力してください。"
        )
        prompt = "\n".join(
            [
                "以下の受信メールに対する返信文を作成してください。",
                "---受信メール---",
                original_email,
                "---返信で伝えたい要点---",
                key_points,
                f"トーン: {tone}",
                f"署名: {signature}" if signature.strip() else "署名: 特に指定なし（汎用的な結びで良い）",
            ]
        )

        st.divider()
        st.subheader("生成結果")
        st.write_stream(generate_stream(prompt, system_instruction, temperature, model))
