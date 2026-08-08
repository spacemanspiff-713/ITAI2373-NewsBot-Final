# API Reference

## Core system

`NewsBot2IntegratedSystem(config=None)` creates the orchestrator. Call `fit(dataframe=None)` once to load the project corpus or a compatible DataFrame. `comprehensive_analysis(article_text, metadata=None)` returns classification, sentiment, entities, relationships, topics, summary, similar records, language, translation, enhancements, runtime backend status, timing, and warnings. `batch_analysis(articles)` applies the same pipeline subject to the configured batch limit. `query_interface(user_query, conversation_context=None)` returns grounded local-corpus records, parsed intent/parameters, follow-up state, and next actions. `generate_insights_report(articles, report_type="comprehensive")` aggregates batch outputs.

## Analysis modules

`AdvancedNewsClassifier.fit(texts, labels)` compares candidate models. `predict`, `predict_with_confidence`, `explain_prediction`, `evaluate`, `save`, and `load` support inference and review. `TopicDiscoveryEngine.fit_topics(documents, dates)` trains LDA/NMF; use `get_topic_words`, `get_article_topics`, `compare_models`, and `track_topic_trends`. `SentimentEvolutionTracker.analyze`, `track_sentiment_over_time`, and `detect_sentiment_anomalies` expose VADER-based analysis. `EntityRelationshipMapper.extract_entities`, `extract_relationships`, `build_knowledge_graph`, `find_entity_connections`, and `export_graph` expose transparent local graph evidence.

## Language and multilingual modules

`IntelligentSummarizer.summarize_article`, `summarize_multiple_articles`, `generate_headline`, `assess_summary_quality`, and `backend_status` provide summary output and provenance. `SemanticSearchEngine.build_index`, `semantic_search`, `find_similar_articles`, `cluster_similar_content`, `expand_query`, `save_cache`, and `backend_status` provide retrieval. `LanguageDetector.detect_language` returns language, name, confidence, support status, and warning. `Translator.translate_text` returns translation, availability, backend, and warning. `CrossLingualAnalyzer.cross_lingual_similarity`, `compare_entities`, `compare_sentiment`, and `compare_coverage` return descriptive comparisons.

## Web routes

`GET /` returns the Flask dashboard. `POST /analyze` and `POST /api/analyze` accept form or JSON `{ "text": "..." }`; input must be 20–20,000 characters. `POST /batch` accepts JSON `{ "articles": [...] }`. `GET /query` or `POST /api/query` accepts a `query`. `GET /health` returns `{ "status": "ok" }`. Responses use JSON, enforce request-size limits, and should be treated as local analytical output rather than verified reporting.
