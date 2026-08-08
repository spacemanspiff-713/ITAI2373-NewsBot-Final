from src.analysis.classifier import AdvancedNewsClassifier


def test_classifier_returns_valid_probability_output() -> None:
    labels = ["TECH", "SPORTS", "POLITICS", "WELLNESS", "BUSINESS", "ENTERTAINMENT"] * 2
    texts = [
        "software computer artificial intelligence technology", "team player game championship sports",
        "senate election government policy politics", "health sleep doctor wellness fitness",
        "market company investor economy business", "movie actor television music entertainment",
    ] * 2
    classifier = AdvancedNewsClassifier().fit(texts, labels, compare_models=False)
    result = classifier.predict_with_confidence("The software company launched an AI product.")
    assert result["primary_category"] in set(labels)
    assert 0 <= result["confidence"] <= 1
    assert result["confidence"] + sum(item["confidence"] for item in result["alternatives"]) <= 1.000001


def test_classifier_handles_unusual_input() -> None:
    classifier = AdvancedNewsClassifier().fit(["tech software", "sports game"] * 3, ["TECH", "SPORTS"] * 3, compare_models=False)
    assert classifier.predict_with_confidence("🤖 !!!")["primary_category"] in {"TECH", "SPORTS"}
