# Technical Documentation

## Architecture
NewsBot 2.0 refactors the completed midterm’s deterministic HuffPost sampling, NLTK preprocessing, TF-IDF comparison, VADER sentiment, spaCy NER, evaluation, and visualizations into modules. New layers add LDA/NMF, topic trends, graph construction, lazy transformer summarization, semantic search, multilingual demo processing, and grounded conversation.

## Data flow
CSV → validation/normalization → preprocessing → classifier/topic/sentiment/NER/search → integrated JSON report. Components fail independently and return warnings.

## Evaluation and limits
See `data/results/metrics`. The main corpus is historical English headline/description text, not full articles. Confidence is not truth and graph co-occurrence is not a real-world relationship.

## Security
Environment variables hold secrets. No raw dataset, model cache, or `.env` is committed.
