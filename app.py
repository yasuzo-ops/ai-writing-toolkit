import streamlit as st

from utils.ui import render_sidebar_settings

st.set_page_config(page_title="AIライティングツール", page_icon="✍️", layout="wide")

render_sidebar_settings()

st.title("✍️ AIライティングツール")
st.caption("Gemini APIを使った、個人用オールインワン・ライティングアシスタント")

st.markdown("左のメニューから使いたいツールを選んでください。")

tools = [
    ("📝", "ブログ記事作成", "テーマ・キーワードからブログ記事の下書きを生成します。"),
    ("📧", "メール返信作成", "受信メールの内容から、適切なトーンの返信文を生成します。"),
    ("📄", "文章要約", "長文を、指定した形式・長さで要約します。"),
    ("✨", "校正リライト", "誤字脱字の修正や、文章のトーン変換（丁寧に／簡潔に等）を行います。"),
    ("🏷️", "タイトル生成", "記事内容から、複数のタイトル・キャッチコピー候補を生成します。"),
    ("🌐", "翻訳", "自然な訳文を、指定した言語・トーンで生成します。"),
    ("📱", "SNS投稿文", "X・Instagramなど、プラットフォームに合わせた投稿文を生成します。"),
]

cols = st.columns(2)
for i, (icon, name, desc) in enumerate(tools):
    with cols[i % 2]:
        with st.container(border=True):
            st.markdown(f"#### {icon} {name}")
            st.write(desc)

st.divider()
st.subheader("セットアップ")
st.markdown(
    """
1. [Google AI Studio](https://aistudio.google.com/apikey) でGemini APIキーを取得します。
2. 次のいずれかの方法でキーを設定します。
   - サイドバーの「🔑 Gemini APIキー」欄に直接入力する（このセッションのみ有効）
   - `.streamlit/secrets.toml.example` を `.streamlit/secrets.toml` にコピーし、`GEMINI_API_KEY` を設定する
   - 環境変数 `GEMINI_API_KEY` を設定する
3. サイドバーでモデルや創造性(temperature)を調整しつつ、各ページでツールを利用できます。

このアプリはデータベースや認証機能を持たない、個人利用向けのローカルツールです。
"""
)
