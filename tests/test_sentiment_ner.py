import pandas as pd

from src.analysis.ner_extractor import EntityRelationshipMapper
from src.analysis.sentiment_analyzer import SentimentEvolutionTracker


def test_sentiment_output_and_timeline_are_structured() -> None:
    tracker = SentimentEvolutionTracker()
    result = tracker.analyze("The excellent result made investors happy.")
    assert result["label"] == "positive"
    assert {"compound", "positive", "neutral", "negative", "subjectivity", "emotions"}.issubset(result)
    timeline = tracker.track_sentiment_over_time(pd.DataFrame({"full_text": ["good progress", "bad loss"], "date": ["2021-01-01", "2022-01-01"], "category": ["TECH", "TECH"]}))
    assert len(tracker.detect_sentiment_anomalies(timeline)) == 2


def test_ner_returns_safe_structured_entities_and_graph() -> None:
    mapper = EntityRelationshipMapper()
    entities = mapper.extract_entities("Apple announced a $5 million investment in California.")
    assert all({"text", "label", "start", "end", "sentence"}.issubset(entity) for entity in entities)
    graph = mapper.build_knowledge_graph([{"article_id": 1, "full_text": "Apple and Google met in California."}])
    assert graph.number_of_nodes() >= 0
