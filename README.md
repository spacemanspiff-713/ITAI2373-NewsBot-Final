# NewsBot Intelligence System 2.0

## Project Overview

NewsBot 2.0 evolves the completed midterm HuffPost NewsBot into a modular local NLP system. It preserves deterministic data preparation, preprocessing, classification comparison, VADER sentiment, spaCy NER, evaluation, and visualizations, then adds LDA/NMF topics, trends, entity graphs, summaries, semantic search, multilingual demos, and a grounded conversational interface.

## Business Problem and Capabilities

Editors and analysts need faster ways to explore historical coverage without treating model output as truth. The system provides confidence-aware routing, topic and sentiment trends, entity co-occurrence, related article retrieval, multilingual examples, and local-corpus queries.

## Dataset

The project reuses the midterm’s unchanged 1,800-row, six-category HuffPost sample. It contains historical English headline/description text, not full article bodies. Authored multilingual examples are separate in `data/demo`.

## Installation and Quick Start

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m spacy download en_core_web_sm
.venv/bin/python -m pytest -q
.venv/bin/python scripts/run_phase2.py
./.venv/bin/python run.py
```

## Notebooks, Tests, and Web App

Run `01_Data_Exploration.ipynb` through `07_System_Integration.ipynb` from the repository root. The primary optional frontend is the Streamlit continuation of the midterm dashboard:

```bash
./.venv/bin/streamlit run streamlit_app.py
```

It provides dashboard, article analysis, batch processing, natural-language query, results, and dataset-explorer views. The Flask API remains available for container deployment at `/`, `/analyze`, `/batch`, `/query`, `/api/analyze`, `/api/query`, and `/health`.

## Model Performance

Current reproducible output: the midterm-style Multinomial Naive Bayes baseline selected on the held-out final split (accuracy 0.714; macro F1 0.712). NMF selected for top-word distinctiveness. See `data/results/metrics/evaluation_summary.json`.

## Limitations and Ethics

Confidence is not truth. Sentiment, topics, NER, translation, summaries, and semantic similarity can be wrong. Co-occurrence does not establish a real-world relationship; internal corroboration is not fact-checking. Historical dataset bias, language coverage limits, and privacy implications are documented in `docs/`.

## Repository Structure, Contribution, AI Assistance, Deployment, Future Work

See the relative Markdown sources in `docs/`, which include technical, executive, user, API, deployment, contribution, AI-disclosure, reflection, presentation, and references material. Before submission, replace `TODO_GROUP_NAME`, create polished PDF/PPTX exports, and push only after review.
