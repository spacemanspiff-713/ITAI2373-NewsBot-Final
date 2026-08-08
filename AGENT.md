# AGENT.md — ITAI 2373 NewsBot Intelligence System 2.0 Final Project

## Mission

Build the user's **ITAI 2373 Final Project: NewsBot Intelligence System 2.0** as a polished, modular, reproducible, portfolio-quality NLP project that **extends the completed midterm NewsBot** rather than replacing it with an unrelated implementation.

The system must satisfy the required final-project architecture:

1. **Advanced Content Analysis Engine**
2. **Language Understanding & Generation**
3. **Multilingual Intelligence**
4. **Conversational Interface**
5. **System Integration, Testing, Evaluation, Documentation**
6. **Optional Web Application Frontend** for bonus credit
7. **Optional Advanced Research Extension** for bonus credit

The primary objective is a working local project and GitHub repository. Do not optimize for flashy complexity at the expense of reliability.

---

# 1. Authoritative Project Context

Use these project files/instructions as the source of truth:

- `ITAI 2373 - Final Project_ NewsBot Intelligence System 2.pdf`
- `NewsBot2_Student_Guidance_Notebook.ipynb`
- `🌐_Web_App_Development_Tutorial_for_NewsBot_Intelligence_System (1).pdf`
- the user's completed midterm NewsBot repository
- the user's existing HuffPost News Category dataset/sample

The final-project PDF requires:

- professional modular repository
- advanced classification with confidence
- LDA/NMF topic modeling
- topic evolution/trends
- advanced sentiment tracking
- entity relationship mapping / knowledge graph
- intelligent summarization
- semantic search using embeddings
- content enhancement / insight generation
- language detection
- translation integration
- cross-lingual comparison
- conversational intent/query handling
- context-aware follow-up questions
- comprehensive testing/evaluation
- technical documentation
- user documentation
- executive/business documentation
- presentation-ready outputs

The guidance notebook contains 24 cells and 7 sections:

1. Project Setup & Architecture Planning
2. Advanced Content Analysis Engine
3. Language Understanding & Generation
4. Multilingual Intelligence
5. Conversational Interface
6. System Integration & Testing
7. Evaluation & Documentation

It scaffolds the following classes/methods and should be treated as a requirements checklist:

- `NewsBot2Config`
- `NewsBot2System`
- `AdvancedNewsClassifier`
- `TopicDiscoveryEngine`
- `SentimentEvolutionTracker`
- `EntityRelationshipMapper`
- `IntelligentSummarizer`
- `SemanticSearchEngine`
- `ContentEnhancer`
- `MultilingualProcessor`
- `ConversationalInterface`
- `NewsBot2IntegratedSystem`
- `NewsBot2TestSuite`
- `NewsBot2Evaluator`

Do not leave TODO/pass implementations in the final project.

---

# 2. Important Instruction Conflicts

Some dates in the instructor PDF are clearly template/legacy dates and conflict with the current Canvas assignment. **Do not hardcode assignment due dates anywhere in the project.**

The current assignment page is more authoritative for submission timing.

For this independently completed project, use the following final artifact names:

```text
FP_TechnicalDoc_JasonTrimble_JasonTrimble_ITAI2373.pdf
FP_ExecutiveSummary_JasonTrimble_JasonTrimble_ITAI2373.pdf
FP_Presentation_JasonTrimble_JasonTrimble_ITAI2373.pptx
FP_VideoPresentation_JasonTrimble_JasonTrimble_ITAI2373.mp4
FP_ReflectiveJournal_JasonTrimble_ITAI2373.pdf
```

Known submitter name:

```text
JasonTrimble
```

This project is independently completed by Jason Trimble. Do not imply shared work.

---

# 3. Existing Midterm Foundation

The midterm NewsBot is already complete and used the **HuffPost News Category Dataset**.

Existing midterm design:

- source dataset: `News_Category_Dataset_v3.json`
- dataset format: JSON Lines
- selected categories:
  - `POLITICS`
  - `ENTERTAINMENT`
  - `BUSINESS`
  - `SPORTS`
  - `TECH`
  - `WELLNESS`
- balanced sample:
  - 300 rows/category
  - 1,800 articles total
- analysis text:
  - `headline + short_description`
- existing features:
  - preprocessing
  - TF-IDF
  - POS analysis
  - syntax/dependency analysis
  - VADER sentiment
  - multi-class classification
  - spaCy NER
  - integrated article analyzer
- classifier comparison included:
  - Multinomial Naive Bayes
  - Logistic Regression
  - Linear SVM
- Logistic Regression was retained in the integrated midterm system because it supports probabilities/confidence.

Existing midterm repository name:

```text
ITAI2373-NewsBot-Midterm
```

The final project must be a **new sibling project**:

```text
ITAI2373-NewsBot-Final
```

Do not overwrite or mutate the submitted midterm repository.

If the midterm repository is available locally, reuse its prepared sample and logic where appropriate. Likely source path from the user's previous work:

```text
/home/daddy/Desktop/_DEV/_SCHOOL/itai_2373/midterm/ITAI2373-NewsBot-Midterm
```

Do not assume that exact path exists. Detect it or accept a relative path.

---

# 4. Final Repository Structure

Create this structure, preserving the instructor's required hierarchy and adding a clean integration/web layer:

```text
ITAI2373-NewsBot-Final/
├── README.md
├── AGENT.md
├── requirements.txt
├── requirements-lock.txt
├── pyproject.toml                    # optional but preferred
├── .gitignore
├── .env.example
├── config/
│   ├── __init__.py
│   ├── settings.py
│   └── api_keys_template.txt
├── src/
│   ├── __init__.py
│   ├── system.py                    # integrated NewsBot2 orchestrator
│   ├── data_processing/
│   │   ├── __init__.py
│   │   ├── text_preprocessor.py
│   │   ├── feature_extractor.py
│   │   └── data_validator.py
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── classifier.py
│   │   ├── sentiment_analyzer.py
│   │   ├── ner_extractor.py
│   │   └── topic_modeler.py
│   ├── language_models/
│   │   ├── __init__.py
│   │   ├── summarizer.py
│   │   ├── generator.py
│   │   └── embeddings.py
│   ├── multilingual/
│   │   ├── __init__.py
│   │   ├── translator.py
│   │   ├── language_detector.py
│   │   └── cross_lingual_analyzer.py
│   ├── conversation/
│   │   ├── __init__.py
│   │   ├── query_processor.py
│   │   ├── intent_classifier.py
│   │   └── response_generator.py
│   └── utils/
│       ├── __init__.py
│       ├── visualization.py
│       ├── evaluation.py
│       ├── export.py
│       └── logging_config.py
├── notebooks/
│   ├── 01_Data_Exploration.ipynb
│   ├── 02_Advanced_Classification.ipynb
│   ├── 03_Topic_Modeling.ipynb
│   ├── 04_Language_Models.ipynb
│   ├── 05_Multilingual_Analysis.ipynb
│   ├── 06_Conversational_Interface.ipynb
│   ├── 07_System_Integration.ipynb
│   └── 08_Research_Extension_Transformer.ipynb  # optional bonus
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_preprocessing.py
│   ├── test_classification.py
│   ├── test_topic_modeling.py
│   ├── test_multilingual.py
│   ├── test_conversation.py
│   └── test_integration.py
├── data/
│   ├── raw/
│   │   └── README.md
│   ├── processed/
│   │   └── newsbot_dataset_sample.csv
│   ├── demo/
│   │   ├── multilingual_demo.json
│   │   └── summarization_gold.json
│   ├── models/
│   │   └── .gitkeep
│   └── results/
│       ├── metrics/
│       ├── figures/
│       ├── tables/
│       └── exports/
├── docs/
│   ├── technical_documentation.md
│   ├── executive_summary.md
│   ├── user_guide.md
│   ├── api_reference.md
│   ├── deployment_guide.md
│   ├── individual_contributions.md
│   ├── ai_assistance.md
│   ├── references.md
│   ├── presentation_outline.md
│   └── reflective_journal_draft.md
├── reports/
│   ├── source/
│   └── README.md
├── web/
│   ├── __init__.py
│   ├── app.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── results.html
│   │   ├── batch.html
│   │   ├── query.html
│   │   └── about.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
├── Dockerfile
├── Procfile
└── run.py
```

The instructor's structure is the minimum. Extra files above are allowed when they improve organization.

---

# 5. Git / Repository Guardrails

Before doing anything:

1. Confirm current working directory.
2. Confirm the midterm project is not being modified.
3. Create or enter `ITAI2373-NewsBot-Final`.
4. Initialize Git only if no `.git` exists.
5. Do not push until the user asks or a valid remote is already configured.
6. Never commit:
   - `.venv/`
   - model caches
   - Hugging Face caches
   - large raw JSON dataset
   - API keys
   - `.env`
   - generated temporary files
   - downloaded transformer weights

Recommended `.gitignore`:

```gitignore
.venv/
venv/
__pycache__/
*.pyc
.ipynb_checkpoints/
.env
.env.*
!.env.example

# raw/large data
data/raw/*.json
data/raw/*.jsonl
data/raw/*.zip

# model artifacts/caches
data/models/*
!data/models/.gitkeep
.cache/
huggingface/
transformers_cache/

# local exports
*.log
.DS_Store
```

Keep all README links relative. Never create `/home/...` absolute links inside Markdown.

---

# 6. Data Strategy

## 6.1 Primary Dataset

Reuse the same HuffPost sample from the midterm for continuity and reproducibility:

```text
data/processed/newsbot_dataset_sample.csv
```

Expected columns should include or be normalized to:

```text
headline
short_description
category
authors
date
full_text
```

If `full_text` is missing:

```python
df["headline"] = df["headline"].fillna("").astype(str)
df["short_description"] = df["short_description"].fillna("").astype(str)
df["full_text"] = (
    df["headline"].str.strip() + ". " + df["short_description"].str.strip()
).str.strip()
```

Parse dates:

```python
df["date"] = pd.to_datetime(df["date"], errors="coerce")
```

Keep the six-category schema from the midterm.

Do not silently replace the dataset.

## 6.2 Why this dataset is still appropriate

The final project needs time-based analysis. The HuffPost dataset includes article dates, making it suitable for:

- topic evolution
- sentiment evolution
- trend detection
- event spikes

The dataset is predominantly English. Therefore, do **not** pretend it is multilingual.

## 6.3 Multilingual Demo Dataset

Create a small, clearly labeled demo/evaluation dataset:

```text
data/demo/multilingual_demo.json
```

Use original project-authored examples in at least:

- English
- Spanish
- French

Optional:
- German

Each record:

```json
{
  "id": "es_001",
  "language": "es",
  "text": "...",
  "english_reference": "...",
  "topic": "technology"
}
```

Use these records to validate:

- language detection
- translation
- multilingual embeddings
- cross-language semantic similarity
- multilingual NER behavior

Do not claim the main HuffPost training corpus is multilingual.

---

# 7. Configuration

Implement `config/settings.py` using a dataclass.

Recommended settings:

```python
@dataclass
class NewsBot2Config:
    random_state: int = 42
    max_text_length: int = 20000
    max_batch_size: int = 20

    classification_categories: tuple = (
        "POLITICS",
        "ENTERTAINMENT",
        "BUSINESS",
        "SPORTS",
        "TECH",
        "WELLNESS",
    )

    topic_count: int = 8
    topic_top_words: int = 12

    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    summarization_model: str = "sshleifer/distilbart-cnn-12-6"

    min_summary_words: int = 25
    max_summary_words: int = 120

    translation_backend: str = "auto"

    confidence_threshold: float = 0.55
```

Read API keys from environment variables only.

No real API key may appear in the repo.

---

# 8. Module A — Advanced Content Analysis Engine

## 8.1 Enhanced Classification

Implement in:

```text
src/analysis/classifier.py
```

Required class:

```python
class AdvancedNewsClassifier:
    fit(...)
    predict(...)
    predict_with_confidence(...)
    explain_prediction(...)
    evaluate(...)
    save(...)
    load(...)
```

### Recommended model strategy

Create a clear progression:

**Baseline**
- midterm-style word TF-IDF + Logistic Regression

**Enhanced model**
- word TF-IDF:
  - unigrams + bigrams
  - `min_df`
  - `max_df`
- character TF-IDF:
  - character 3-5 grams
- combine with `FeatureUnion`
- compare:
  - Logistic Regression
  - LinearSVC
  - Calibrated LinearSVC if practical

The integrated system should use the best reliable probabilistic model.

Preferred candidates:

```python
LogisticRegression(max_iter=3000, class_weight="balanced")
```

or:

```python
CalibratedClassifierCV(LinearSVC(class_weight="balanced"))
```

Use:

- stratified train/test split
- fixed seed 42
- accuracy
- macro precision
- macro recall
- macro F1
- weighted F1
- per-class metrics
- confusion matrix

### Confidence output

Return:

```python
{
    "primary_category": "...",
    "confidence": 0.87,
    "alternatives": [
        {"category": "...", "confidence": 0.08},
        {"category": "...", "confidence": 0.03}
    ]
}
```

### Explainability

For linear models, expose top positive terms/features contributing to the selected class.

Do not claim causal reasoning.

### Multi-level classification

The dataset is single-label. Do not fake multi-label ground truth.

Implement:

1. learned primary category
2. top-N alternative probabilities
3. optional deterministic `content_family` mapping documented as a secondary taxonomy

Example:

```python
CONTENT_FAMILY_MAP = {
    "POLITICS": "Public Affairs",
    "BUSINESS": "Business & Economy",
    "TECH": "Technology",
    "SPORTS": "Sports",
    "ENTERTAINMENT": "Culture & Entertainment",
    "WELLNESS": "Lifestyle & Wellness",
}
```

This satisfies multi-level output without pretending the dataset contains multiple labels.

Persist lightweight classical models with `joblib`.

Do not commit huge transformer checkpoints.

---

## 8.2 Topic Modeling — LDA AND NMF

Implement:

```text
src/analysis/topic_modeler.py
```

Required class:

```python
class TopicDiscoveryEngine:
    fit_topics(documents, dates=None)
    get_topic_words(topic_id, n_words=10)
    get_article_topics(article_text)
    compare_models(documents)
    track_topic_trends(articles_with_dates)
    visualize_topics(...)
```

The assignment explicitly expects **LDA and NMF**.

Implement both:

### LDA
- `CountVectorizer`
- `LatentDirichletAllocation`

### NMF
- `TfidfVectorizer`
- `NMF`

Evaluate/compare:

- topic coherence if practical with gensim `CoherenceModel`
- topic diversity
- stability across fixed seeds if runtime permits
- qualitative interpretability

Use 6-10 topics. Pick the final topic count using documented evidence, not arbitrary tuning.

### Topic evolution

Use the real `date` column.

Aggregate topic probability by:

- year or quarter for full historical overview
- monthly only if enough data exists

Generate:

- topic prevalence over time
- top emerging/declining topics
- topic spike detection
- topic/category cross-tab

Save figures and CSV summaries to `data/results`.

Avoid overclaiming causation from a sample dataset.

---

## 8.3 Advanced Sentiment Analysis

Implement:

```text
src/analysis/sentiment_analyzer.py
```

Use a hybrid transparent approach:

- VADER overall polarity
- TextBlob subjectivity if available
- NRC-style emotion lexicon via `nrclex` if practical
- fallback gracefully if optional package fails

Required output:

```python
{
    "label": "positive|neutral|negative",
    "compound": ...,
    "positive": ...,
    "neutral": ...,
    "negative": ...,
    "subjectivity": ...,
    "emotions": {...},
    "key_sentiment_phrases": [...]
}
```

Implement:

```python
track_sentiment_over_time(df)
detect_sentiment_anomalies(timeline)
```

Use rolling mean / z-score style anomaly signals.

Create visualizations:

- sentiment by category
- sentiment over time
- emotion distribution
- anomaly markers

Do not describe an anomaly as a real-world event unless supported by article evidence.

---

## 8.4 Entity Relationship Mapping

Implement:

```text
src/analysis/ner_extractor.py
```

Use spaCy `en_core_web_sm` as the required baseline.

Extract:

- PERSON
- ORG
- GPE
- LOC
- DATE
- MONEY
- NORP
- EVENT
- PRODUCT

Return structured entities with:

```python
{
    "text": "...",
    "label": "...",
    "start": ...,
    "end": ...,
    "sentence": "..."
}
```

### Relationship extraction

Use two transparent methods:

1. same-sentence entity co-occurrence
2. dependency-based subject/verb/object heuristics when available

Relationships may include:

```text
co_occurs
subject_of
object_of
verb_relation
```

Do not pretend a co-occurrence edge proves a real-world relationship.

### Knowledge graph

Use `networkx`.

Nodes:
- entity text
- entity type
- frequency

Edges:
- relationship label
- weight/count
- source article IDs

Implement:

```python
build_knowledge_graph(articles)
find_entity_connections(entity1, entity2)
```

Export:

```text
data/results/exports/entity_graph.graphml
```

Create a readable static network visualization for the report.

---

# 9. Module B — Language Understanding & Generation

## 9.1 Intelligent Summarization

Implement:

```text
src/language_models/summarizer.py
```

Use a **lazy-loaded** pretrained summarization model.

Recommended:

```text
sshleifer/distilbart-cnn-12-6
```

Reason:
- smaller than BART-large
- enough to demonstrate pretrained language-model integration
- works locally/Colab with GPU acceleration
- manageable for a class project

Detect CUDA automatically:

```python
device = 0 if torch.cuda.is_available() else -1
```

Support:

```python
summarize_article(text, summary_type="brief|balanced|detailed")
summarize_multiple_articles(articles, focus_topic=None)
generate_headline(text)
assess_summary_quality(original_text, summary, reference=None)
```

Because the HuffPost dataset only contains headline + short description, do not pretend each record is a full article.

For meaningful summarization demos:

- concatenate several related articles into a multi-document context
- use user-entered full articles in web/demo
- maintain a small authored evaluation set in `data/demo/summarization_gold.json`

Evaluation:
- compression ratio
- readability
- ROUGE when a clean reference exists
- length constraints
- simple entity-preservation check

Do not evaluate against a reference that is already copied verbatim into the input and then present that as unbiased ROUGE.

Provide an extractive fallback if the transformer cannot load.

---

## 9.2 Semantic Search

Implement:

```text
src/language_models/embeddings.py
```

Use one multilingual embedding model for both English and cross-language search:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

This avoids maintaining separate English and multilingual embedding models.

Implement:

```python
encode_documents(documents)
build_index(documents, metadata)
semantic_search(query, top_k=5, filters=None)
find_similar_articles(article_text, top_k=5)
cluster_similar_content(...)
expand_query(query, top_results=None)
```

For ~1,800 documents, simple NumPy/scikit-learn cosine similarity is sufficient.

No vector database is required.

Precompute embeddings and cache locally:

```text
data/results/embeddings/news_embeddings.npy
data/results/embeddings/news_metadata.csv
```

Do not commit massive cache files if they become large; document regeneration.

---

## 9.3 Content Enhancement / Insight Generation

Implement:

```text
src/language_models/generator.py
```

Avoid hallucinated "facts."

The enhancer should produce **evidence-grounded local insights** from:

- classification
- topic distribution
- sentiment
- entities
- related articles
- temporal trends
- article similarity

Example output:

```python
{
    "key_entities": [...],
    "related_articles": [...],
    "topic_context": [...],
    "trend_context": {...},
    "coverage_gaps": [...],
    "corroboration": [...]
}
```

`cross_reference_facts()` must be conservative.

It may:
- locate corpus articles mentioning the same entities/numbers/dates
- report supporting/contradictory snippets
- return a "corroboration signal"

It may **not** claim "true" or "false" unless an actual trusted verification source is integrated.

Use wording such as:

> Internal corpus corroboration only; this is not an independent fact-check.

---

# 10. Module C — Multilingual Intelligence

The primary dataset is English, so this module needs a separate demonstration strategy.

Implement:

```text
src/multilingual/language_detector.py
src/multilingual/translator.py
src/multilingual/cross_lingual_analyzer.py
```

## 10.1 Language Detection

Use:

- `langdetect` or `langid`
- deterministic seed when available

Return:

```python
{
    "language": "es",
    "language_name": "Spanish",
    "confidence": ...,
    "is_supported": True
}
```

For very short or ambiguous text, return low confidence rather than pretending certainty.

## 10.2 Translation Integration

Design an adapter interface.

Preferred sequence:

1. optional local Hugging Face MarianMT model for supported demo pairs
2. optional `deep-translator` backend when network access is available
3. clean "translation unavailable" response if neither works

Do not require paid API keys for the core project.

Support at minimum demo translation:

```text
Spanish -> English
French -> English
```

Keep translation models lazy-loaded.

Translation quality evaluation:
- semantic similarity between translation and authored English reference using multilingual embeddings
- optional BLEU if a proper reference exists

## 10.3 Cross-Lingual Analysis

Use multilingual embeddings to compare semantically equivalent articles without requiring translation first.

Implement:

```python
compare_coverage(articles_by_language)
cross_lingual_similarity(text_a, text_b)
compare_entities(...)
compare_sentiment(...)
```

Produce:
- similarity score
- overlapping entities
- topic similarity
- sentiment differences
- translation availability
- coverage-depth statistics

## 10.4 Cultural Context

Do not claim the system deeply "understands culture."

Implement a lightweight transparent context layer:
- language/locale metadata
- source-language indicators
- named places and organizations
- differing sentiment/topic/entity emphasis across language examples

Phrase outputs as:
- "coverage difference"
- "language-specific framing signal"
- "regional context indicator"

not as definitive cultural conclusions.

---

# 11. Module D — Conversational Interface

Implement:

```text
src/conversation/intent_classifier.py
src/conversation/query_processor.py
src/conversation/response_generator.py
```

The interface must support natural-language queries over the stored article dataset.

## 11.1 Intent Classification

Use a small supervised intent classifier.

Create a compact authored training set for intents:

```text
search
summarize
sentiment
topic_trend
entity_lookup
compare
similar_articles
help
```

Train:

```python
TfidfVectorizer + LogisticRegression
```

Return intent confidence.

Rule-based fallback is allowed when confidence is low.

## 11.2 Query Entity/Parameter Extraction

Parse:

- category
- sentiment
- timeframe
- person/org/location
- topic keyword
- requested count
- comparison targets

Examples:

```text
"Show me positive tech news from this week"
"Summarize politics coverage about Biden"
"Compare Apple and Google coverage"
"How has sentiment around technology changed over time?"
"Find articles similar to this paragraph"
```

Because the dataset is historical, "this week" cannot mean live current news. Resolve time expressions **relative to the dataset's maximum date** unless the query explicitly provides an absolute date.

Make that behavior clear to the user.

## 11.3 Conversation Context

Maintain lightweight conversation state:

```python
{
    "last_intent": ...,
    "last_filters": ...,
    "last_entities": ...,
    "last_results": ...,
    "turn_count": ...
}
```

Support follow-up:

```text
User: Show me tech news.
Bot: ...
User: What about negative ones?
```

The second query should inherit `category=TECH`.

## 11.4 Response Generation

Use deterministic grounded response templates.

Responses should:
- name applied filters
- summarize result counts
- cite article titles/IDs from the local dataset
- avoid fabricated article content
- provide helpful next actions

No paid LLM API is required.

---

# 12. Integrated System

Implement:

```text
src/system.py
```

Required class:

```python
class NewsBot2IntegratedSystem:
    comprehensive_analysis(article_text, metadata=None)
    batch_analysis(articles)
    query_interface(user_query, conversation_context=None)
    generate_insights_report(articles, report_type="comprehensive")
```

Initialize components once.

Use lazy loading for heavy transformer models.

Example single-article result:

```python
{
    "classification": {...},
    "sentiment": {...},
    "entities": [...],
    "relationships": [...],
    "topics": [...],
    "summary": "...",
    "semantic_neighbors": [...],
    "enhancements": {...},
    "language": {...},
    "translation": {...},
    "statistics": {
        "word_count": ...,
        "character_count": ...,
        "processing_seconds": ...
    }
}
```

Graceful degradation is critical.

If summarization or translation fails:
- classification/sentiment/NER/topic analysis should still return
- include component-level warning
- do not crash entire analysis

---

# 13. Guidance Notebook Completion

The uploaded `NewsBot2_Student_Guidance_Notebook.ipynb` has code scaffolding but many TODO/pass blocks.

Do not make it the only final artifact.

Use it as a checklist and optionally save a completed copy:

```text
notebooks/00_NewsBot2_Student_Guidance_Completed.ipynb
```

However, the instructor's seven named notebooks are the priority.

Each notebook should import from `src/` rather than duplicate giant class implementations.

Notebooks should demonstrate, visualize, evaluate, and explain the reusable modules.

---

# 14. Required Notebooks

## `01_Data_Exploration.ipynb`

Include:
- dataset loading/validation
- category distribution
- date range
- text length
- missing data
- duplicate analysis
- date coverage by category
- sample records
- business framing

Save:
- category distribution
- date distribution
- text length distribution

## `02_Advanced_Classification.ipynb`

Include:
- baseline midterm classifier
- enhanced classifier
- model comparison
- accuracy/macro F1/weighted F1
- confusion matrix
- confidence examples
- explainability examples
- limitations

## `03_Topic_Modeling.ipynb`

Include:
- LDA
- NMF
- top words/topics
- model comparison
- coherence/diversity
- topic/category relationship
- topic evolution over time
- topic visualization

## `04_Language_Models.ipynb`

Include:
- transformer summarization
- extractive fallback
- single vs multi-document summary
- summarization quality metrics
- semantic embeddings
- semantic search examples
- similar article search
- content enhancement examples

## `05_Multilingual_Analysis.ipynb`

Include:
- multilingual demo dataset
- language detection
- translation
- translation quality
- cross-lingual embeddings
- semantic matching across languages
- entity/sentiment differences
- explicit limitations

## `06_Conversational_Interface.ipynb`

Include:
- intent classifier training/evaluation
- query parsing
- examples for each intent
- multi-turn follow-up example
- error/low-confidence handling
- no live-news claims

## `07_System_Integration.ipynb`

This is the capstone demo.

Include:
- initialize complete system
- load saved models/index
- analyze at least 3 NEW article texts not in training data
- run batch analysis
- run natural-language queries
- multilingual demo
- timing/performance
- integrated outputs
- final strengths/limitations
- business use cases
- ethical considerations

---

# 15. Testing

Use `pytest`.

Run:

```bash
pytest -q
```

Required tests:

## preprocessing
- empty text
- normal text
- punctuation
- URL
- Unicode

## classification
- returns valid category
- probabilities sum approximately to 1
- confidence is 0-1
- unknown/weird input handled

## topic modeling
- model fits small corpus
- correct topic count
- topic words returned
- article topic distribution valid

## multilingual
- language detection works on clear English/Spanish/French
- unsupported/very-short input handled
- translation test mocked or marked optional if network/model unavailable

## conversation
- intent classification
- parameter extraction
- follow-up inherits context

## integration
- comprehensive analysis returns required keys
- one component failure does not crash all components
- batch limit respected

Do not make tests download large transformer models.

Mock or skip heavyweight/network-dependent tests.

---

# 16. Evaluation Framework

Implement `src/utils/evaluation.py` and expose through `NewsBot2Evaluator`.

Required metrics:

## Classification
- accuracy
- macro precision
- macro recall
- macro F1
- weighted F1
- confusion matrix
- calibration / confidence reliability when feasible

## Topic modeling
- coherence
- diversity
- stability or documented qualitative check

## Summarization
- compression ratio
- ROUGE when clean reference exists
- readability
- entity/key-information retention

## Semantic search
Create a small authored relevance set:
- query
- expected relevant category/topic/article IDs

Calculate:
- Precision@K
- hit rate / Recall@K where possible

## Multilingual
- language-detection accuracy on demo data
- translation semantic similarity
- cross-lingual retrieval success on paired examples

## Conversation
Create authored test queries with expected:
- intent
- category
- sentiment
- timeframe
- entity

Calculate intent accuracy and slot/parameter extraction accuracy.

Generate:

```text
data/results/metrics/evaluation_summary.json
data/results/tables/model_comparison.csv
data/results/tables/topic_quality.csv
data/results/tables/conversation_eval.csv
```

---

# 17. Required Visual Outputs

At minimum generate and save:

```text
data/results/figures/category_distribution.png
data/results/figures/date_distribution.png
data/results/figures/classification_confusion_matrix.png
data/results/figures/model_comparison.png
data/results/figures/topic_words_lda.png
data/results/figures/topic_words_nmf.png
data/results/figures/topic_evolution.png
data/results/figures/sentiment_by_category.png
data/results/figures/sentiment_evolution.png
data/results/figures/entity_type_distribution.png
data/results/figures/entity_relationship_graph.png
data/results/figures/semantic_clusters.png
```

Use professional titles/labels.

No unreadable 30-color charts.

Prefer accessible visualizations.

---

# 18. Optional Bonus — Flask Web Application

The uploaded web tutorial explicitly supports a Flask interface and the final project awards up to 30 bonus points.

Build the web app **after the core system passes tests**.

Required pages/features:

1. **Dashboard**
2. **Single Article Analysis**
3. **Batch Processing**
4. **Natural Language Query Interface**
5. **Visualizations / results**
6. **About / project information**

Routes:

```text
GET  /
POST /analyze
POST /batch
GET  /query
POST /api/analyze
POST /api/query
GET  /health
```

Features:
- paste article text
- validate minimum/maximum input
- show classification + confidence
- sentiment
- named entities
- topics
- summary
- similar articles
- language detection
- translation when requested
- conversational queries
- downloadable JSON result
- responsive UI
- loading indicator
- graceful error messages

Security/production basics:
- `SECRET_KEY` from environment
- debug off by default
- request size limit
- no secrets in repo
- Jinja autoescaping
- safe error handling

Use:

```text
gunicorn
```

Add:

```text
Procfile
Dockerfile
```

Make deployment compatible with standard container hosts/Render-style deployment.

Do not block the required project if live deployment is unavailable.

Document deployment completely.

---

# 19. Optional Bonus — Advanced Research Extension

Only do this after all required features work.

Preferred extension:

```text
notebooks/08_Research_Extension_Transformer.ipynb
```

Fine-tune or evaluate a small transformer classifier:

```text
distilbert-base-uncased
```

Recommended constraints:
- use a subset of the 1,800 records
- max token length ~128
- 1-2 epochs
- GPU if available
- fixed seed
- compare with classical model on:
  - accuracy
  - macro F1
  - training time
  - inference time
  - resource cost

Do not commit the large trained checkpoint to GitHub.

The point is a research comparison, not replacing the stable core classifier.

If no GPU is available, document the extension as optional/skipped and do not destabilize the project.

---

# 20. Documentation Deliverables

## README.md

Must include:

```markdown
# NewsBot Intelligence System 2.0

## Project Overview
## Business Problem
## Key Capabilities
## System Architecture
## Dataset
## Installation
## Quick Start
## Running the Notebooks
## Running Tests
## Running the Web App
## Model Performance
## Topic Modeling Results
## Multilingual Capabilities
## Conversational Interface
## Example Outputs
## Repository Structure
## Limitations
## Ethical Considerations
## Individual Contribution
## AI / External Tool Assistance
## Deployment
## Future Enhancements
```

Include screenshots/figures with **relative** links.

## `docs/technical_documentation.md`

Must cover:
- architecture
- component interactions
- data flow
- class/function API
- models/algorithms
- installation
- configuration
- evaluation
- performance
- error handling
- limitations
- security
- deployment

This Markdown will later become:

```text
FP_TechnicalDoc_JasonTrimble_JasonTrimble_ITAI2373.pdf
```

## `docs/executive_summary.md`

Business focused, not code focused.

Must include:
- problem
- solution
- target users
- capabilities
- measurable benefit assumptions
- ROI analysis
- use cases
- competitive positioning
- risks/limitations
- recommendation

Be careful with ROI:
- clearly label assumptions
- show formulas
- do not fabricate audited business results

This Markdown will later become:

```text
FP_ExecutiveSummary_JasonTrimble_JasonTrimble_ITAI2373.pdf
```

## `docs/user_guide.md`

Non-technical instructions:
- analyze article
- read confidence
- understand topics
- use semantic search
- use conversational query
- multilingual usage
- download/export
- troubleshooting

## `docs/api_reference.md`

Document every public class/method and web API route.

## `docs/deployment_guide.md`

Include:
- local venv
- packages
- spaCy model
- Hugging Face first-run downloads
- Flask
- gunicorn
- Docker
- environment variables
- deployment health check

## `docs/individual_contributions.md`

Describe Jason's actual technical contribution areas based on what was built.

## `docs/ai_assistance.md`

Academic-integrity-friendly disclosure:
- AI used for planning/debugging/documentation assistance
- final code tested locally
- external libraries/models cited
- no claim that AI-generated output was independently verified unless it was

Do not hide AI assistance.

## `docs/reflective_journal_draft.md`

Create a strong 3-page-content draft covering:
- independent project management
- individual contributions
- integration challenges
- lessons learned
- business value
- ethical concerns
- future improvements
- professional development

Do not invent interactions that did not occur.

## `docs/presentation_outline.md`

Prepare 15-20 slide outline:
- title
- business problem
- architecture
- dataset
- midterm -> final evolution
- advanced classification
- topic modeling
- sentiment/entity graph
- language models
- multilingual intelligence
- conversational interface
- integrated demo
- evaluation
- business impact
- limitations/ethics
- future work
- contribution summary
- Q&A

Include demo script and speaker-note bullets.

---

# 21. PDF / Presentation Boundary

The coding agent's priority is to produce accurate source content and evidence.

Generate polished Markdown sources first.

If local PDF/PPTX tooling is already installed and reliable, basic exports are okay, but **do not spend significant time fighting PDF styling or slide layout**.

The final polished PDFs and presentation can be produced separately from the completed source content.

Required eventual filenames:

```text
FP_TechnicalDoc_JasonTrimble_JasonTrimble_ITAI2373.pdf
FP_ExecutiveSummary_JasonTrimble_JasonTrimble_ITAI2373.pdf
FP_Presentation_JasonTrimble_JasonTrimble_ITAI2373.pptx
FP_ReflectiveJournal_JasonTrimble_ITAI2373.pdf
```

---

# 22. Academic / Ethical Requirements

Include an ethics section in notebook + docs.

Discuss:
- dataset/source bias
- category imbalance in original corpus
- historical nature of the dataset
- sentiment model limitations
- entity/relationship false positives
- translation errors
- cultural interpretation risks
- hallucination risk in abstractive summarization
- confidence != truth
- semantic similarity != factual agreement
- internal corroboration != fact checking
- privacy implications if the system were adapted to private documents

Use transparent language.

Never label an article "misinformation" based only on sentiment, topics, or similarity.

---

# 23. Performance / Resource Strategy

The user's midterm already runs locally. Preserve local-first operation and keep Colab compatibility.

Important:

- lazy-load transformer models
- cache embeddings
- avoid re-running spaCy across the entire corpus unnecessarily
- use batched sentence-transformer encoding
- use sample-based knowledge graph visualizations
- cap web batch inputs
- time major operations
- use GPU automatically when available
- include CPU fallback

Set:

```python
RANDOM_STATE = 42
```

everywhere relevant.

Use deterministic sampling.

Do not force a transformer model download during unit tests.

---

# 24. Dependencies

Recommended direct dependencies:

```text
pandas
numpy
scipy
scikit-learn
matplotlib
seaborn
plotly
nltk
spacy
textblob
vaderSentiment
nrclex
gensim
networkx
sentence-transformers
transformers
torch
rouge-score
langdetect
deep-translator
flask
gunicorn
joblib
pytest
psutil
wordcloud
```

Optional:

```text
pyLDAvis
```

After the environment works, pin tested versions in `requirements.txt`.

Generate a full environment snapshot:

```bash
pip freeze > requirements-lock.txt
```

Install spaCy model:

```bash
python -m spacy download en_core_web_sm
```

If an optional package causes major dependency conflicts, remove it and document the fallback. Do not break the project to satisfy an optional library.

---

# 25. Build Order

Follow this order exactly unless a concrete technical blocker requires a change.

## Phase 0 — Inventory
- locate midterm repo
- locate prepared CSV
- inspect columns
- inspect current Python version
- inspect venv
- confirm GPU availability
- create final project folder
- copy only reusable assets

## Phase 1 — Foundation
- repository structure
- config
- logging
- data validator
- text preprocessing
- deterministic dataset loader
- tests for foundation

## Phase 2 — Advanced Content Analysis
- enhanced classifier
- sentiment evolution
- NER
- relationship graph
- LDA
- NMF
- topic evolution
- evaluation + plots
- tests

## Phase 3 — Language Models
- summarization
- extractive fallback
- summary evaluation
- embeddings
- semantic search
- query expansion
- local content enhancement
- tests

## Phase 4 — Multilingual
- demo dataset
- detection
- translation adapter
- cross-lingual semantic comparison
- multilingual evaluation
- tests

## Phase 5 — Conversation
- authored intent dataset
- intent classifier
- query parsing
- response generation
- context handling
- tests

## Phase 6 — Integration
- `NewsBot2IntegratedSystem`
- comprehensive article analysis
- batch analysis
- query interface
- insight report
- component-level warnings
- full integration tests

## Phase 7 — Notebooks
- create all seven required notebooks
- use reusable `src/` code
- run notebooks top-to-bottom
- save outputs

## Phase 8 — Documentation
- README
- technical doc source
- executive summary source
- user guide
- API reference
- deployment guide
- contribution document
- AI assistance disclosure
- reflection draft
- presentation outline

## Phase 9 — Bonus Web App
- Flask app
- UI
- API
- batch
- query chat
- results export
- Docker/gunicorn
- local smoke test

## Phase 10 — Research Bonus
- DistilBERT comparison if time/resources permit

## Phase 11 — Final Validation
- fresh environment test
- `pytest -q`
- run notebooks
- run web smoke tests
- inspect Git status
- verify no secrets
- verify no absolute README links
- verify no placeholder text remains
- verify required outputs exist

---

# 26. Definition of Done

Do not call the project complete until all required items below pass.

## Repository
- [ ] folder is `ITAI2373-NewsBot-Final`
- [ ] professional structure exists
- [ ] README complete
- [ ] requirements pinned
- [ ] no secrets
- [ ] no large raw dataset committed
- [ ] no huge model checkpoints committed

## Data
- [ ] reuses HuffPost midterm data
- [ ] 6 categories preserved
- [ ] date parsed
- [ ] data validation report produced
- [ ] multilingual demo explicitly separated from main corpus

## Advanced Analysis
- [ ] enhanced classifier
- [ ] confidence scoring
- [ ] alternative class scores
- [ ] explainability
- [ ] LDA implemented
- [ ] NMF implemented
- [ ] topic trends over time
- [ ] sentiment evolution
- [ ] sentiment anomaly signals
- [ ] entity extraction
- [ ] relationship extraction
- [ ] knowledge graph

## Language Understanding
- [ ] transformer summarization
- [ ] fallback summarization
- [ ] summary quality metrics
- [ ] semantic embeddings
- [ ] semantic search
- [ ] similar article search
- [ ] query expansion
- [ ] evidence-grounded content enhancement

## Multilingual
- [ ] language detection
- [ ] confidence/uncertainty handling
- [ ] translation integration
- [ ] Spanish demo
- [ ] French demo
- [ ] cross-lingual semantic comparison
- [ ] limitations documented

## Conversational
- [ ] intent classifier
- [ ] query entities/filters
- [ ] natural language querying
- [ ] context state
- [ ] follow-up questions
- [ ] grounded response generation

## Integration
- [ ] single article analysis
- [ ] batch analysis
- [ ] query interface
- [ ] component failure isolation
- [ ] timing/performance output
- [ ] JSON-serializable results

## Evaluation
- [ ] classification metrics
- [ ] topic quality metrics
- [ ] summarization metrics
- [ ] semantic search relevance test
- [ ] language detection/translation metrics
- [ ] conversational intent/slot metrics
- [ ] comprehensive evaluation summary

## Notebooks
- [ ] 01 Data Exploration
- [ ] 02 Advanced Classification
- [ ] 03 Topic Modeling
- [ ] 04 Language Models
- [ ] 05 Multilingual Analysis
- [ ] 06 Conversational Interface
- [ ] 07 System Integration
- [ ] all required notebooks execute cleanly

## Documentation
- [ ] technical documentation source
- [ ] executive summary source
- [ ] user guide
- [ ] API reference
- [ ] deployment guide
- [ ] contribution document
- [ ] AI assistance disclosure
- [ ] reflection draft
- [ ] presentation outline
- [ ] ethics/limitations section

## Bonus
- [ ] Flask web frontend if time allows
- [ ] web app locally tested
- [ ] Docker/gunicorn ready
- [ ] optional transformer research notebook if stable

---

# 27. Final Agent Handoff Report

When finished, do not just say "done."

Return a concise report with:

```markdown
# NewsBot 2.0 Build Report

## Completed
- ...

## Model Results
- best classifier:
- accuracy:
- macro F1:
- topic model selected:
- topic coherence:
- sentiment outputs:
- semantic search evaluation:
- conversational intent accuracy:

## Files Created
- ...

## Tests
- pytest:
- notebook execution:
- web smoke test:

## Bonus Features
- ...

## Known Limitations
- ...

## Manual Items Still Needed
- polished PDFs
- final presentation export
- live deployment URL, if required
- GitHub push, if not already done

## Exact Commands to Run
```bash
...
```
```

Flag any missing package/model/network dependency precisely.

Do not hide failures.

---

# 28. Quality Bar

The project should look like a strong student capstone, not a fake enterprise SaaS product.

Priorities:

1. correct and reproducible
2. integrated
3. evaluated
4. clearly documented
5. visually professional
6. portfolio-ready
7. bonus features only after required features are stable

Prefer transparent classical/compact NLP methods over fragile complexity.

The final system must demonstrate that the user understands:

- what each model does
- why it was chosen
- how it was evaluated
- where it can fail
- how the components work together
- what business value the system provides

Build something that can be demonstrated live without crossing fingers.
