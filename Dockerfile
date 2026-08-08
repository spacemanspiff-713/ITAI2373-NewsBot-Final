FROM python:3.12-slim
WORKDIR /app
COPY requirements-local.txt .
RUN pip install --no-cache-dir -r requirements-local.txt && python -m spacy download en_core_web_sm
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["gunicorn","--bind","0.0.0.0:5000","web.app:create_app()"]
