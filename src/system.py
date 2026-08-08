"""Integrated NewsBot Intelligence System 2.0 orchestration layer."""

from __future__ import annotations

import time
from collections import Counter

import pandas as pd

from config import NewsBot2Config
from src.analysis import AdvancedNewsClassifier, EntityRelationshipMapper, SentimentEvolutionTracker, TopicDiscoveryEngine
from src.conversation import QueryProcessor, ResponseGenerator
from src.data_processing.data_validator import load_news_dataset
from src.language_models import ContentEnhancer, IntelligentSummarizer, SemanticSearchEngine
from src.multilingual import CrossLingualAnalyzer, LanguageDetector, Translator


class NewsBot2IntegratedSystem:
    """Initialize reusable components once and isolate component failures."""

    def __init__(self, config=None):
        self.config = config or NewsBot2Config()
        self.classifier = AdvancedNewsClassifier(self.config)
        self.sentiment_tracker = SentimentEvolutionTracker()
        self.entity_mapper = EntityRelationshipMapper()
        self.topic_engine = TopicDiscoveryEngine(self.config.topic_count, self.config.random_state, self.config.topic_top_words)
        self.summarizer = IntelligentSummarizer(
            self.config.summarization_model,
            self.config.enable_transformers,
            self.config.transformer_local_files_only,
        )
        self.search_engine = SemanticSearchEngine(self.config.embedding_model, self.config.enable_transformers)
        self.enhancer = ContentEnhancer(self.search_engine)
        self.language_detector = LanguageDetector()
        self.translator = Translator(self.config.translation_backend)
        self.cross_lingual = CrossLingualAnalyzer(self.search_engine, self.translator)
        self.query_processor = QueryProcessor()
        self.response_generator = ResponseGenerator()
        self.dataframe = None
        self.conversation_state = {"last_intent": None, "last_filters": {}, "last_entities": [], "last_results": [], "turn_count": 0}

    def fit(self, dataframe=None):
        self.dataframe = dataframe.copy() if dataframe is not None else load_news_dataset(self.config.processed_data_path)
        self.dataframe["date"] = pd.to_datetime(self.dataframe["date"], errors="coerce")
        self.classifier.fit(self.dataframe["full_text"], self.dataframe["category"])
        self.topic_engine.fit_topics(self.dataframe["full_text"], self.dataframe["date"])
        self.search_engine.build_index(
            self.dataframe["full_text"],
            self.dataframe[["article_id", "title", "category", "date"]].to_dict("records"),
        )
        return self

    def _ready(self):
        if self.dataframe is None:
            self.fit()

    def comprehensive_analysis(self, article_text, metadata=None):
        del metadata  # Reserved for future source/locale metadata without changing the public API.
        self._ready()
        started = time.perf_counter()
        text = str(article_text or "")
        result = {"warnings": []}
        tasks = {
            "classification": lambda: self.classifier.predict_with_confidence(text),
            "sentiment": lambda: self.sentiment_tracker.analyze(text),
            "entities": lambda: self.entity_mapper.extract_entities(text),
            "relationships": lambda: self.entity_mapper.extract_relationships(text),
            "topics": lambda: self.topic_engine.get_article_topics(text)[:3],
            "summary": lambda: self.summarizer.summarize_article(text),
            "semantic_neighbors": lambda: self.search_engine.find_similar_articles(text, 5),
            "language": lambda: self.language_detector.detect_language(text),
        }
        for name, task in tasks.items():
            try:
                result[name] = task()
            except Exception as exc:
                result[name] = None
                result["warnings"].append(f"{name} unavailable: {type(exc).__name__}")
        language = (result.get("language") or {}).get("language", "unknown")
        try:
            result["translation"] = self.translator.translate_text(text, "en", language) if language not in {"en", "unknown"} else {
                "translation": text, "available": language == "en",
                "backend": "identity" if language == "en" else "unavailable",
                "warning": None if language == "en" else "Unknown source language.",
            }
        except Exception as exc:
            result["translation"] = {"translation": None, "available": False, "backend": "unavailable", "warning": type(exc).__name__}
            result["warnings"].append(f"translation unavailable: {type(exc).__name__}")
        result["text"] = text
        try:
            result["enhancements"] = self.enhancer.enhance(result)
        except Exception as exc:
            result["enhancements"] = None
            result["warnings"].append(f"enhancement unavailable: {type(exc).__name__}")
        result["runtime"] = {
            "summarization": self.summarizer.backend_status(),
            "retrieval": self.search_engine.backend_status(),
        }
        result["statistics"] = {
            "word_count": len(text.split()),
            "character_count": len(text),
            "processing_seconds": round(time.perf_counter() - started, 4),
        }
        return result

    def batch_analysis(self, articles):
        items = list(articles)
        if len(items) > self.config.max_batch_size:
            raise ValueError(f"Batch limit is {self.config.max_batch_size} articles.")
        return [
            self.comprehensive_analysis(item.get("full_text") or item.get("text") or item) if isinstance(item, dict) else self.comprehensive_analysis(item)
            for item in items
        ]

    def query_interface(self, user_query, conversation_context=None):
        self._ready()
        context = conversation_context or self.conversation_state
        max_date = self.dataframe["date"].max().date().isoformat()
        parsed = self.query_processor.parse(user_query, max_date, context)
        response = self.response_generator.respond(
            parsed, self.dataframe, self.search_engine, self.topic_engine,
            self.sentiment_tracker, self.summarizer,
        )
        self.conversation_state.update({
            "last_intent": parsed["intent"], "last_filters": response["applied_filters"],
            "last_entities": parsed["parameters"].get("entities", []),
            "last_results": response["results"], "turn_count": context.get("turn_count", 0) + 1,
        })
        return {**response, "intent": parsed, "conversation_context": self.conversation_state.copy()}

    def generate_insights_report(self, articles, report_type="comprehensive"):
        results = self.batch_analysis(articles)
        categories = Counter((item.get("classification") or {}).get("primary_category", "Unknown") for item in results)
        sentiment = Counter((item.get("sentiment") or {}).get("label", "unknown") for item in results)
        return {
            "report_type": report_type, "articles_analyzed": len(results),
            "category_distribution": dict(categories), "sentiment_labels": dict(sentiment),
            "note": "Corpus-derived descriptive insight; not independent fact verification.",
            "analyses": results if report_type == "comprehensive" else [],
        }
