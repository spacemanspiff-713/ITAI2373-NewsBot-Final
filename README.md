# NewsBot Intelligence System 2.0

Streamlit Web App Link - https://itai2373-newsbot-final-3tlthu4qutdmrh6bhegevf.streamlit.app/

NewsBot 2.0 is a reproducible NLP capstone that extends the completed midterm NewsBot rather than replacing it. It preserves the deterministic HuffPost data preparation, preprocessing, TF-IDF classification comparison, VADER sentiment, spaCy NER, evaluation, visualizations, and Streamlit dashboard foundation, then adds topic discovery, temporal analysis, entity graphs, summarization, retrieval, multilingual demonstrations, and grounded conversational exploration.

## Business Problem

Editors and analysts need a faster way to triage a large historical corpus without confusing an automated score with editorial truth. NewsBot supports first-pass routing and research: it describes patterns in the local source corpus, exposes uncertainty, and keeps article IDs, titles, and limitations visible.

## Key Capabilities

- Confidence-aware six-category classification with alternative class scores and linear-model explanation when applicable.
- LDA and NMF topic discovery, topic evolution, sentiment trends, and a transparent entity co-occurrence graph.
- Extractive summarization fallback plus opt-in lazy DistilBART summarization; semantic retrieval fallback plus opt-in multilingual sentence embeddings.
- Spanish/French authored paired demos with language detection, translation provenance, and careful cross-language comparisons.
- Intent classification, query parameters, historical time handling, follow-up category context, and deterministic grounded responses.
- Streamlit “Signal Desk” frontend and optional Flask API with batch limits, JSON export, health check, Dockerfile, and Procfile.

## System Architecture

```text
HuffPost CSV + authored multilingual demos
        ↓ validation / normalization / preprocessing
classification | topics | sentiment | entities | retrieval | language
        ↓
NewsBot2IntegratedSystem → JSON report / conversational responses / web UI
        ↓
evaluation tables, metrics, figures, and presentation artifacts
```

## Dataset

The final project reuses the unchanged midterm sample: 1,800 balanced HuffPost records across BUSINESS, ENTERTAINMENT, POLITICS, SPORTS, TECH, and WELLNESS. Records contain historical headlines and short descriptions, not complete article bodies. Spanish/French material is intentionally separated under `data/demo/`; it is not represented as corpus-wide multilingual coverage.

## Installation and Quick Start

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements-local.txt
./.venv/bin/python -m spacy download en_core_web_sm
./.venv/bin/python -m pytest -q
./.venv/bin/python scripts/run_phase2.py
```

Run the primary optional dashboard:

```bash
./.venv/bin/streamlit run streamlit_app.py
```

Run the Flask API locally:

```bash
./.venv/bin/python run.py
```

## Notebooks, Tests, and Outputs

Run notebooks `01_Data_Exploration.ipynb` through `07_System_Integration.ipynb` from the repository root. They import the reusable `src/` modules and demonstrate every required module. To run them headlessly:

```bash
./.venv/bin/python scripts/execute_notebooks.py
```

The reproducible evaluation pipeline writes figures, tables, and JSON metrics to `data/results/`. The current default, CPU-safe run reports 0.714 held-out accuracy and 0.712 macro F1 for the selected midterm-style Multinomial Naive Bayes baseline. NMF is selected by top-word distinctiveness; topic “coherence” is explicitly labeled as a lexical-overlap proxy.

## Pretrained Model Option

The required pretrained integrations are lazy so a classroom laptop remains reliable. The default run records the extractive and TF-IDF fallbacks. To permit Hugging Face downloads and activate DistilBART plus multilingual Sentence-Transformers:

```bash
NEWSBOT_ENABLE_TRANSFORMERS=1 ./.venv/bin/python scripts/run_phase2.py
```

For offline use after downloading models, set `NEWSBOT_TRANSFORMERS_LOCAL_ONLY=1`. Set `NEWSBOT_TRANSLATION_BACKEND=marian` only when you explicitly want a first-run MarianMT download; `auto` uses authored demos, cached local models, then an optional network adapter.

## Repository Structure

```text
src/                 reusable NLP modules and orchestration
notebooks/           seven required, executed demonstrations
data/demo/           authored evaluation and multilingual examples
data/results/        reproducible figures, metrics, tables, exports
tests/               focused unit and integration tests
web/                 optional Flask frontend/API
docs/                submission source documents and presentation script
deliverables/        generated PDF/PPTX submission artifacts
```

## Limits, Ethics, and Responsible Use

This is historical, predominantly English coverage. Confidence is not truth; sentiment, topics, NER, translation, and similarity can be wrong. Entity co-occurrence does not prove a real relationship. Related local articles provide internal corpus corroboration only, never independent fact verification. Any adaptation to private documents needs privacy review, source governance, human editorial review, and bias monitoring.

## Documentation, Contribution, and Deployment

See [technical documentation](docs/technical_documentation.md), [executive summary](docs/executive_summary.md), [user guide](docs/user_guide.md), [API reference](docs/api_reference.md), [deployment guide](docs/deployment_guide.md), [individual contributions](docs/individual_contributions.md), and [AI assistance disclosure](docs/ai_assistance.md).

Jason Trimble completed this project independently, including the documented technical integration work. Push the latest reviewed changes to GitHub before final submission and keep the deployed Streamlit URL available if claiming the web-app bonus.

### Streamlit Community Cloud

Deploy `streamlit_app.py` from the repository root. Community Cloud automatically installs the lightweight `requirements.txt`, which supports its Python 3.14 runtime and excludes the optional PyTorch/Transformers stack. The reproducible Python 3.12 development environment remains in `requirements-local.txt` and `requirements-lock.txt`; it is not installed by the hosted app.
