"""Generate reproducible NewsBot 2.0 metrics, tables, and figures.

This script intentionally evaluates lightweight default fallbacks. Set
``NEWSBOT_ENABLE_TRANSFORMERS=1`` to exercise configured pretrained models;
the summary records the active backend so neither path is misrepresented.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config import NewsBot2Config
from src.analysis.classifier import AdvancedNewsClassifier
from src.analysis.ner_extractor import EntityRelationshipMapper
from src.analysis.sentiment_analyzer import SentimentEvolutionTracker
from src.analysis.topic_modeler import TopicDiscoveryEngine
from src.conversation.query_processor import QueryProcessor
from src.data_processing.data_validator import DatasetValidator, load_news_dataset
from src.language_models.embeddings import SemanticSearchEngine
from src.language_models.summarizer import IntelligentSummarizer
from src.multilingual.cross_lingual_analyzer import CrossLingualAnalyzer
from src.multilingual.language_detector import LanguageDetector
from src.multilingual.translator import Translator
from src.utils.export import export_json, export_table
from src.utils.visualization import (
    category_distribution, confusion, date_distribution, entity_chart, entity_graph,
    model_comparison, semantic_clusters, sentiment_by_category, sentiment_timeline,
    topic_evolution, topic_words,
)


RESULTS = ROOT / "data" / "results"
FIGURES, TABLES, METRICS, EXPORTS, EMBEDDINGS = (RESULTS / name for name in ("figures", "tables", "metrics", "exports", "embeddings"))


def load_demo(name):
    return json.loads((ROOT / "data" / "demo" / name).read_text(encoding="utf-8"))


def evaluate_semantic_search(engine, evaluation_rows):
    rows = []
    for item in evaluation_rows:
        returned = engine.semantic_search(item["query"], 5)
        categories = [record.get("category") for record in returned]
        expected = item["expected_category"]
        rows.append({
            "query": item["query"], "expected_category": expected,
            "top_category": categories[0] if categories else None,
            "precision_at_1": float(bool(categories and categories[0] == expected)),
            "precision_at_5": sum(category == expected for category in categories) / max(len(categories), 1),
            "hit_at_5": float(expected in categories),
            "retrieval_backend": engine.backend,
        })
    frame = pd.DataFrame(rows)
    return frame, {
        "precision_at_1": float(frame["precision_at_1"].mean()),
        "precision_at_5": float(frame["precision_at_5"].mean()),
        "hit_rate_at_5": float(frame["hit_at_5"].mean()),
        "queries": int(len(frame)),
        "note": "Category-based authored relevance evaluation; it measures topical retrieval, not factual agreement.",
    }


def evaluate_summaries(summarizer, examples):
    rows = []
    for item in examples:
        summary = summarizer.summarize_article(item["text"], "balanced")
        quality = summarizer.assess_summary_quality(item["text"], summary, item.get("reference"))
        rows.append({"id": item["id"], "summary": summary, **quality})
    frame = pd.DataFrame(rows)
    numeric = [column for column in ("compression_ratio", "flesch_reading_ease", "entity_preservation_proxy", "rougeL") if column in frame]
    return frame, {"examples": int(len(frame)), "backend": summarizer.backend_status(), "mean": {column: float(frame[column].dropna().mean()) for column in numeric}}


def evaluate_multilingual(engine, demo):
    detector, translator = LanguageDetector(), Translator()
    analyzer = CrossLingualAnalyzer(engine, translator)
    rows = []
    for item in demo:
        detected = detector.detect_language(item["text"])
        translation = translator.translate_text(item["text"], "en", item["language"])
        comparison = analyzer.cross_lingual_similarity(item["text"], item["english_reference"])
        rows.append({
            "id": item["id"], "expected_language": item["language"], "detected_language": detected["language"],
            "detection_correct": float(detected["language"] == item["language"]), "detection_confidence": detected["confidence"],
            "translation_available": bool(translation["available"]), "translation_backend": translation["backend"],
            "translation_similarity": comparison["similarity"], "similarity_backend": comparison["backend"],
            "cross_lingual_retrieval_success": float(comparison["similarity"] >= 0.85),
        })
    frame = pd.DataFrame(rows)
    return frame, {
        "examples": int(len(frame)), "language_detection_accuracy": float(frame["detection_correct"].mean()),
        "translation_availability": float(frame["translation_available"].mean()),
        "mean_translation_similarity": float(frame["translation_similarity"].mean()),
        "cross_lingual_retrieval_success": float(frame["cross_lingual_retrieval_success"].mean()),
        "note": "Spanish/French examples are authored paired demonstrations; this is not a broad machine-translation benchmark.",
    }


def evaluate_conversation(max_date, examples):
    processor = QueryProcessor()
    rows = []
    expected_slots, predicted_slots = [], []
    for item in examples:
        parsed = processor.parse(item["query"], max_date)
        expected = item.get("parameters", {})
        predicted = parsed["parameters"]
        slot_match = {}
        for field, value in expected.items():
            slot_match[field] = bool(predicted.get(field)) if value == "relative" else predicted.get(field) == value
        rows.append({
            "query": item["query"], "expected_intent": item["intent"], "predicted_intent": parsed["intent"],
            "intent_correct": float(parsed["intent"] == item["intent"]), "intent_confidence": parsed["confidence"],
            "slot_matches": json.dumps(slot_match),
        })
        expected_slots.append(expected)
        predicted_slots.append(predicted)
    frame = pd.DataFrame(rows)
    fields = ("category", "sentiment", "entities", "comparison_targets")
    by_field = {}
    for field in fields:
        values = [predicted.get(field) == expected.get(field) for predicted, expected in zip(predicted_slots, expected_slots) if field in expected]
        by_field[field] = float(sum(values) / len(values)) if values else None
    values = [value for value in by_field.values() if value is not None]
    return frame, {"intent_accuracy": float(frame["intent_correct"].mean()), "slot_accuracy": float(sum(values) / len(values)) if values else 0.0, "slot_accuracy_by_field": by_field, "queries": int(len(frame))}


def main() -> None:
    for directory in (FIGURES, TABLES, METRICS, EXPORTS, EMBEDDINGS):
        directory.mkdir(parents=True, exist_ok=True)
    config = NewsBot2Config()
    dataframe = load_news_dataset(config.processed_data_path)
    validation = DatasetValidator().validate(dataframe)
    export_json(validation.to_dict(), METRICS / "data_validation_report.json")
    category_distribution(dataframe, FIGURES / "category_distribution.png")
    date_distribution(dataframe, FIGURES / "date_distribution.png")

    classifier = AdvancedNewsClassifier(config).fit(dataframe["full_text"], dataframe["category"])
    classification = classifier.evaluation_results
    export_json(classification, METRICS / "classification_evaluation.json")
    export_table(pd.DataFrame(classification["model_comparison"]), TABLES / "model_comparison.csv")
    model_comparison(classification["model_comparison"], FIGURES / "model_comparison.png")
    confusion(classification["labels"], classification["confusion_matrix"], FIGURES / "classification_confusion_matrix.png")
    classifier.save(ROOT / "data" / "models" / "advanced_classifier.joblib")

    topics = TopicDiscoveryEngine(n_topics=config.topic_count).fit_topics(dataframe["full_text"], dataframe["date"])
    topic_quality = topics.compare_models()
    for item in topic_quality:
        item["stability_check"] = "Fixed random seed and qualitative topic review required; coherence is a lexical-overlap proxy."
    trends = topics.track_topic_trends()
    export_table(pd.DataFrame(topic_quality), TABLES / "topic_quality.csv")
    export_json({"selected_model": topics.selected_model, "emerging_topics": trends["emerging_topics"], "declining_topics": trends["declining_topics"], "spikes": trends["spikes"]}, METRICS / "topic_trends.json")
    topic_words(topics, "lda", FIGURES / "topic_words_lda.png")
    topic_words(topics, "nmf", FIGURES / "topic_words_nmf.png")
    topic_evolution(trends["timeline"], FIGURES / "topic_evolution.png")

    semantic = SemanticSearchEngine(config.embedding_model, config.enable_transformers).build_index(
        dataframe["full_text"], dataframe[["article_id", "title", "category", "date"]].to_dict("records")
    )
    semantic_clusters(semantic.cluster_similar_content(6), FIGURES / "semantic_clusters.png")
    semantic_rows, semantic_metrics = evaluate_semantic_search(semantic, load_demo("evaluation_sets.json")["semantic_search"])
    export_table(semantic_rows, TABLES / "semantic_search_eval.csv")
    export_json(semantic_metrics, METRICS / "semantic_search_evaluation.json")
    if semantic.backend == "sentence_transformer":
        export_json(semantic.save_cache(EMBEDDINGS), METRICS / "embedding_cache.json")
    else:
        export_json({"generated": False, "reason": "TF-IDF fallback was active; rebuild after enabling the sentence-transformer model."}, METRICS / "embedding_cache.json")

    summarizer = IntelligentSummarizer(config.summarization_model, config.enable_transformers, config.transformer_local_files_only)
    summary_rows, summary_metrics = evaluate_summaries(summarizer, load_demo("summarization_gold.json"))
    export_table(summary_rows, TABLES / "summarization_evaluation.csv")
    export_json(summary_metrics, METRICS / "summarization_evaluation.json")

    multilingual_rows, multilingual_metrics = evaluate_multilingual(semantic, load_demo("multilingual_demo.json"))
    export_table(multilingual_rows, TABLES / "multilingual_evaluation.csv")
    export_json(multilingual_metrics, METRICS / "multilingual_evaluation.json")

    conversation_rows, conversation_metrics = evaluate_conversation(str(pd.to_datetime(dataframe["date"]).max().date()), load_demo("evaluation_sets.json")["conversation"])
    export_table(conversation_rows, TABLES / "conversation_eval.csv")
    export_json(conversation_metrics, METRICS / "conversation_evaluation.json")

    sentiment = SentimentEvolutionTracker()
    dataframe["compound"] = dataframe["full_text"].map(lambda text: sentiment.analyzer.polarity_scores(str(text))["compound"])
    timeline = sentiment.detect_sentiment_anomalies(sentiment.track_sentiment_over_time(dataframe))
    export_table(timeline, TABLES / "sentiment_timeline.csv")
    sentiment_by_category(dataframe, FIGURES / "sentiment_by_category.png")
    sentiment_timeline(timeline, FIGURES / "sentiment_evolution.png")

    sample = dataframe.groupby("category", group_keys=False).head(8)
    mapper = EntityRelationshipMapper()
    articles = sample[["article_id", "full_text"]].to_dict("records")
    entities = [entity for article in articles for entity in mapper.extract_entities(article["full_text"])]
    graph = mapper.build_knowledge_graph(articles)
    mapper.export_graph(graph, EXPORTS / "entity_graph.graphml")
    entity_chart(entities, FIGURES / "entity_type_distribution.png")
    entity_graph(graph, FIGURES / "entity_relationship_graph.png")

    summary = {
        "classification": {key: classification[key] for key in ("selected_model", "accuracy", "macro_precision", "macro_recall", "macro_f1", "weighted_f1", "calibration")},
        "topic_model": {"selected": topics.selected_model, "quality": topic_quality},
        "summarization": summary_metrics,
        "semantic_search": semantic_metrics,
        "multilingual": multilingual_metrics,
        "conversation": conversation_metrics,
        "sentiment": {"timeline_rows": int(len(timeline)), "anomalies": int(timeline["is_anomaly"].sum())},
        "entity_graph": {"nodes": graph.number_of_nodes(), "edges": graph.number_of_edges()},
        "runtime_backends": {"summarization": summarizer.backend_status(), "retrieval": semantic.backend_status()},
        "data_validation": validation.to_dict(),
    }
    export_json(summary, METRICS / "evaluation_summary.json")
    print("NewsBot 2.0 evaluation artifacts generated in data/results.")


if __name__ == "__main__":
    main()
