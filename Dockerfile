FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && python -m spacy download en_core_web_sm
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["gunicorn","--bind","0.0.0.0:5000","web.app:create_app()"]
