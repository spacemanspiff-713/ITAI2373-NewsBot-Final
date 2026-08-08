# Deployment Guide

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m spacy download en_core_web_sm
.venv/bin/python -m pytest -q
```

Use CPU PyTorch by default. Run the primary optional dashboard with `./.venv/bin/streamlit run streamlit_app.py`. Streamlit Community Cloud can use `streamlit_app.py` as its entry point, mirroring the midterm deployment approach. `gunicorn 'web.app:create_app()'` remains available for the Flask API. Set `NEWSBOT_SECRET_KEY`; debug is off by default. `/health` is the deployment health check.
