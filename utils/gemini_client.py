"""Gemini APIとの通信を担う共通モジュール。"""
import os

import streamlit as st
from google import genai
from google.genai import types

DEFAULT_MODEL = "gemini-3.6-flash"
AVAILABLE_MODELS = [
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-pro-preview",
]


def get_api_key():
    """優先順位: サイドバーで入力した値 > secrets.toml > 環境変数"""
    if st.session_state.get("gemini_api_key"):
        return st.session_state["gemini_api_key"]
    try:
        secret_key = st.secrets.get("GEMINI_API_KEY")
        if secret_key:
            return secret_key
    except Exception:
        pass
    return os.environ.get("GEMINI_API_KEY")


def get_client() -> genai.Client:
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError("Gemini APIキーが設定されていません。")
    return genai.Client(api_key=api_key)


def _build_config(system_instruction: str, temperature: float) -> types.GenerateContentConfig:
    return types.GenerateContentConfig(
        system_instruction=system_instruction or None,
        temperature=temperature,
    )


def generate_stream(prompt: str, system_instruction: str = "", temperature: float = 0.7, model: str = DEFAULT_MODEL):
    """テキストをストリーミング生成するジェネレータ。st.write_stream に渡して使う。"""
    client = get_client()
    config = _build_config(system_instruction, temperature)
    response_stream = client.models.generate_content_stream(
        model=model,
        contents=prompt,
        config=config,
    )
    for chunk in response_stream:
        if chunk.text:
            yield chunk.text


def generate(prompt: str, system_instruction: str = "", temperature: float = 0.7, model: str = DEFAULT_MODEL) -> str:
    """テキストを一括生成する（ストリーミング不要な場合用）。"""
    client = get_client()
    config = _build_config(system_instruction, temperature)
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )
    return response.text or ""
