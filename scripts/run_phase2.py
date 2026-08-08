"""Generate reproducible Phase 2 models, metrics, and core visual outputs."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.analysis.classifier import AdvancedNewsClassifier
from src.analysis.ner_extractor import EntityRelationshipMapper
from src.analysis.sentiment_analyzer import SentimentEvolutionTracker
from src.analysis.topic_modeler import TopicDiscoveryEngine
from src.data_processing.data_validator import DatasetValidator, load_news_dataset
from src.utils.export import export_json, export_table
from src.utils.visualization import (
    category_distribution, confusion, date_distribution, entity_chart, entity_graph,
    model_comparison, semantic_clusters, sentiment_by_category, sentiment_timeline, topic_evolution, topic_words,
)


RESULTS = ROOT / "data" / "results"
FIGURES, TABLES, METRICS, EXPORTS = (RESULTS / name for name in ("figures", "tables", "metrics", "exports"))


def main() -> None:
    for directory in (FIGURES, TABLES, METRICS, EXPORTS): directory.mkdir(parents=True, exist_ok=True)
    dataframe = load_news_dataset(ROOT / "data" / "processed" / "newsbot_dataset_sample.csv")
    validation = DatasetValidator().validate(dataframe)
    export_json(validation.to_dict(), METRICS / "data_validation_report.json")
    category_distribution(dataframe, FIGURES / "category_distribution.png")
    date_distribution(dataframe, FIGURES / "date_distribution.png")

    classifier = AdvancedNewsClassifier().fit(dataframe["full_text"], dataframe["category"])
    classification = classifier.evaluation_results
    export_json(classification, METRICS / "classification_evaluation.json")
    export_table(__import__("pandas").DataFrame(classification["model_comparison"]), TABLES / "model_comparison.csv")
    model_comparison(classification["model_comparison"], FIGURES / "model_comparison.png")
    confusion(classification["labels"], classification["confusion_matrix"], FIGURES / "classification_confusion_matrix.png")
    classifier.save(ROOT / "data" / "models" / "advanced_classifier.joblib")

    topics = TopicDiscoveryEngine(n_topics=8).fit_topics(dataframe["full_text"], dataframe["date"])
    topic_quality = topics.compare_models(); trends = topics.track_topic_trends()
    export_table(__import__("pandas").DataFrame(topic_quality), TABLES / "topic_quality.csv")
    export_json({"selected_model": topics.selected_model, "emerging_topics": trends["emerging_topics"], "declining_topics": trends["declining_topics"], "spikes": trends["spikes"]}, METRICS / "topic_trends.json")
    topic_words(topics, "lda", FIGURES / "topic_words_lda.png"); topic_words(topics, "nmf", FIGURES / "topic_words_nmf.png"); topic_evolution(trends["timeline"], FIGURES / "topic_evolution.png")
    from src.language_models.embeddings import SemanticSearchEngine
    semantic = SemanticSearchEngine().build_index(dataframe["full_text"], dataframe[["article_id", "category"]].to_dict("records")); semantic_clusters(semantic.cluster_similar_content(6), FIGURES / "semantic_clusters.png")
    semantic_queries = [("software artificial intelligence", "TECH"), ("team championship game", "SPORTS"), ("health sleep doctor", "WELLNESS")]
    semantic_hits = [semantic.semantic_search(query, 1)[0]["category"] == expected for query, expected in semantic_queries]
    semantic_metrics = {"precision_at_1": sum(semantic_hits) / len(semantic_hits), "queries": len(semantic_hits), "note": "Small authored relevance set."}
    export_json(semantic_metrics, METRICS / "semantic_search_evaluation.json")
    from src.conversation.intent_classifier import IntentClassifier
    intent_examples = [("show tech news", "search"), ("summarize politics coverage", "summarize"), ("what is the sentiment", "sentiment"), ("topic trends", "topic_trend"), ("compare Apple and Google coverage", "compare"), ("help", "help")]
    intent_model = IntentClassifier(); conversation_rows = [{"query": query, "expected_intent": expected, "predicted_intent": intent_model.classify_intent(query)["intent"]} for query, expected in intent_examples]
    conversation_accuracy = sum(row["expected_intent"] == row["predicted_intent"] for row in conversation_rows) / len(conversation_rows)
    export_table(__import__("pandas").DataFrame(conversation_rows), TABLES / "conversation_eval.csv")

    sentiment = SentimentEvolutionTracker(); dataframe["compound"] = dataframe["full_text"].map(lambda text: sentiment.analyzer.polarity_scores(str(text))["compound"])
    timeline = sentiment.detect_sentiment_anomalies(sentiment.track_sentiment_over_time(dataframe))
    export_table(timeline, TABLES / "sentiment_timeline.csv"); sentiment_by_category(dataframe, FIGURES / "sentiment_by_category.png"); sentiment_timeline(timeline, FIGURES / "sentiment_evolution.png")

    sample = dataframe.groupby("category", group_keys=False).head(8)
    mapper = EntityRelationshipMapper(); articles = sample[["article_id", "full_text"]].to_dict("records")
    entities = [entity for article in articles for entity in mapper.extract_entities(article["full_text"])]
    graph = mapper.build_knowledge_graph(articles); mapper.export_graph(graph, EXPORTS / "entity_graph.graphml")
    entity_chart(entities, FIGURES / "entity_type_distribution.png"); entity_graph(graph, FIGURES / "entity_relationship_graph.png")

    summary = {"classification": {key: classification[key] for key in ("selected_model", "accuracy", "macro_f1", "weighted_f1")}, "topic_model": {"selected": topics.selected_model, "quality": topic_quality}, "sentiment": {"timeline_rows": len(timeline), "anomalies": int(timeline["is_anomaly"].sum())}, "entity_graph": {"nodes": graph.number_of_nodes(), "edges": graph.number_of_edges()}, "semantic_search": semantic_metrics, "conversation": {"intent_accuracy": conversation_accuracy, "queries": len(conversation_rows)}, "data_validation": validation.to_dict()}
    export_json(summary, METRICS / "evaluation_summary.json")
    print("Phase 2 artifacts generated in data/results.")


if __name__ == "__main__": main()
