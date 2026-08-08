# Deployment Guide

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m spacy download en_core_web_sm
.venv/bin/python -m pytest -q
```

Use CPU PyTorch by default. `gunicorn 'web.app:create_app()'` serves the optional Flask UI. Set `NEWSBOT_SECRET_KEY`; debug is off by default. `/health` is the deployment health check.
