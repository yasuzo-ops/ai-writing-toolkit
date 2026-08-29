# AIライティングツール

Gemini API を使った、個人用オールインワン・ライティングアシスタント。Streamlit のマルチページアプリで、データベースや認証機構を持たない、ローカル1ユーザー向けのツールです。

## 機能

左サイドバーから各ツールを選んで利用します。

- 📝 ブログ記事作成 — テーマ・キーワードから下書きを生成
- 📧 メール返信作成 — 受信メールから適切なトーンの返信文を生成
- 📄 文章要約 — 長文を指定形式・長さで要約
- ✨ 校正リライト — 誤字脱字修正・トーン変換
- 🏷️ タイトル生成 — 記事内容からタイトル・キャッチコピー候補
- 🌐 翻訳 — 指定言語・トーンで自然な訳文
- 📱 SNS投稿文 — プラットフォームに合わせた投稿文

## セットアップ（Windows）

```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## APIキーの設定

[Google AI Studio](https://aistudio.google.com/apikey) で Gemini API キーを取得し、次のいずれかで設定します。

- アプリのサイドバー「🔑 Gemini APIキー」欄に入力（そのセッションのみ有効）
- `.streamlit/secrets.toml.example` を `.streamlit/secrets.toml` にコピーして `GEMINI_API_KEY` を設定
- 環境変数 `GEMINI_API_KEY` を設定

`.streamlit/secrets.toml` と `.env` は `.gitignore` 済みで、Git 管理対象になりません。

## 起動

```
.venv\Scripts\python.exe -m streamlit run app.py
```

## 構成

- `app.py` — ホームページ
- `pages/` — 各ツールページ（ファイル名の先頭番号でサイドバー順が決まる）
- `utils/gemini_client.py` — Gemini API との通信を担う唯一のモジュール
- `utils/ui.py` — ページ共通のサイドバー UI
