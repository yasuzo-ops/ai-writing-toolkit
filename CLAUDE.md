# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal, single-user AI writing toolkit built with Streamlit and the Gemini API. No database, no authentication — it runs entirely locally for one user. There is no test suite.

## Commands

Setup (Windows, from repo root):
```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run the app:
```
.venv\Scripts\python.exe -m streamlit run app.py
```

Check for syntax errors across the app (no test suite exists, so this plus manually loading pages in-browser is the verification path):
```
.venv\Scripts\python.exe -m py_compile app.py utils/gemini_client.py utils/ui.py pages/*.py
```

## Architecture

Streamlit multipage app (MPA). `app.py` is the home page; every file in `pages/` becomes a sidebar-navigable tool page automatically, ordered by the leading number in the filename (`1_📝_...py`, `2_📧_...py`, etc.). Each page is a fully independent script re-run top-to-bottom on every interaction — there's no shared page-level state beyond `st.session_state`.

Shared logic lives in `utils/` and is imported by every page:

- **`utils/gemini_client.py`** — the only place that talks to the Gemini API (via the `google-genai` SDK, `from google import genai`). `get_api_key()` resolves the key with priority: `st.session_state["gemini_api_key"]` (set via sidebar) → `st.secrets["GEMINI_API_KEY"]` → `GEMINI_API_KEY` env var. `generate_stream()` is what pages use for output (yields text chunks for `st.write_stream`); `generate()` is the non-streaming equivalent, currently unused by pages but kept for cases where a full string is needed before further processing.
- **`utils/ui.py`** — `render_sidebar_settings()` draws the model/temperature/API-key sidebar and must be called near the top of every page (it also returns `(model, temperature)` for that page's generation call). `ensure_api_key()` halts page execution (`st.stop()`) with a friendly message if no key is configured yet.

### Adding a new tool page

Follow the pattern already established in every `pages/*.py` file:
1. `st.set_page_config(...)` first.
2. `model, temperature = render_sidebar_settings()` then `ensure_api_key()`.
3. Build inputs inside an `st.form(...)` so the whole tool submits at once.
4. On submit, assemble a `system_instruction` (the tool's persona/rules) and a `prompt` (the actual request + user inputs), then call `st.write_stream(generate_stream(prompt, system_instruction, temperature, model))`.
5. Name the file `N_<emoji>_<name>.py` — the leading number controls sidebar ordering, the emoji becomes the sidebar icon.

Prompts are built inline per-page as `\n`.join(...) blocks rather than via a shared template system — keep new pages consistent with that style rather than introducing a new abstraction.

### API key handling

There is intentionally no persistence layer. A key entered via the sidebar lives only in `st.session_state` for that running session. `.streamlit/secrets.toml` (gitignored; see `.streamlit/secrets.toml.example` for the format) and the `GEMINI_API_KEY` env var are the two ways to avoid re-entering it every run.
