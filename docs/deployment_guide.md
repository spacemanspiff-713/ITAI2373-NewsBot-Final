# Deployment Guide

## Local setup and verification

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/python -m spacy download en_core_web_sm
./.venv/bin/python -m pytest -q
./.venv/bin/python scripts/run_phase2.py
./.venv/bin/python scripts/execute_notebooks.py
```

Run the Streamlit bonus interface with `./.venv/bin/streamlit run streamlit_app.py`. Run the Flask interface/API with `./.venv/bin/python run.py`, then visit `/health`. Production Flask startup is `gunicorn 'web.app:create_app()'`.

## Environment variables

Set `NEWSBOT_SECRET_KEY` to a unique deployment secret. Optional variables are `NEWSBOT_MAX_BATCH_SIZE` (default 20), `NEWSBOT_ENABLE_TRANSFORMERS=1` to permit lazy model downloads, `NEWSBOT_TRANSFORMERS_LOCAL_ONLY=1` for a cached offline model, and `NEWSBOT_TRANSLATION_BACKEND=marian` to explicitly permit a MarianMT model download. Do not commit `.env` files, raw data, or downloaded model caches.

## Containers and hosted deployment

`Dockerfile` and `Procfile` support a standard container/Render-style Flask deployment. Build from the repository root, inject environment variables through the host, run the health check at `/health`, and keep debug disabled. Streamlit Community Cloud can use `streamlit_app.py` as its entry point; confirm the full requirements install and the spaCy model availability on that host before publishing a URL.

## First-run and operational notes

The default runtime uses CPU-safe extractive and TF-IDF fallbacks. Enabling pretrained models can require a large first download and should be tested on the target host. The application caps request and batch size and continues when one optional component fails. It must not be exposed as live-news retrieval or an automated fact-checking service.
