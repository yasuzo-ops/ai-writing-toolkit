import streamlit as st

from utils.gemini_client import generate_stream
from utils.ui import ensure_api_key, render_sidebar_settings

st.set_page_config(page_title="SNS投稿文", page_icon="📱", layout="wide")

model, temperature = render_sidebar_settings()
ensure_api_key()

st.title("📱 SNS投稿文生成")
st.caption("プラットフォームに合わせたSNS投稿文を生成します。")

PLATFORM_GUIDE = {
    "X (Twitter)": "140字前後を目安に、簡潔でインパクトのある投稿文にしてください。",
    "Instagram": "冒頭2〜3行で興味を引き、その後に詳細を書くキャプション形式にしてください。改行を効果的に使ってください。",
    "Facebook": "やや丁寧で説明的な、読みやすい文章にしてください。",
    "LinkedIn": "ビジネスパーソン向けに、プロフェッショナルで示唆に富む文章にしてください。",
    "Threads": "カジュアルで会話的なトーンの、短い投稿文にしてください。",
}

with st.form("sns_form"):
    content = st.text_area("投稿したい内容 *", height=180, placeholder="伝えたい内容や、元になる文章を入力してください")

    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox("プラットフォーム", list(PLATFORM_GUIDE.keys()))
    with col2:
        tone = st.selectbox("トーン", ["カジュアル", "フォーマル", "親しみやすい", "ユーモラス", "熱意的"])

    col3, col4 = st.columns(2)
    with col3:
        use_hashtags = st.checkbox("ハッシュタグを含める", value=True)
        hashtag_count = st.slider("ハッシュタグ数", 1, 10, 5, disabled=not use_hashtags)
    with col4:
        use_emoji = st.checkbox("絵文字を使う", value=True)
        variation_count = st.slider("生成するパターン数", 1, 5, 3)

    submitted = st.form_submit_button("投稿文を生成する", type="primary")

if submitted:
    if not content.strip():
        st.error("投稿したい内容を入力してください。")
    else:
        system_instruction = (
            "あなたはSNSマーケティングに精通したプロのコンテンツライターです。"
            "プラットフォームの特性を踏まえた、エンゲージメントの高い投稿文を作成します。"
            "入力内容と同じ言語で出力してください。"
        )
        prompt_parts = [
            f"以下の内容をもとに、{platform}向けの投稿文を{variation_count}パターン生成してください。",
            f"プラットフォームの特徴: {PLATFORM_GUIDE[platform]}",
            f"トーン: {tone}",
            "絵文字: " + ("適度に使う" if use_emoji else "使わない"),
            "ハッシュタグ: " + (f"末尾に{hashtag_count}個程度付ける" if use_hashtags else "付けない"),
            "各パターンは番号付きで、区切りを分かりやすくして出力してください。",
            "---内容---",
            content,
        ]
        prompt = "\n".join(prompt_parts)

        st.divider()
        st.subheader("生成結果")
        st.write_stream(generate_stream(prompt, system_instruction, temperature, model))
