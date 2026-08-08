"""Evaluation framework for the integrated final system."""

from __future__ import annotations

from typing import Iterable

import numpy as np
from sklearn.metrics import accuracy_score

from src.utils.export import export_json


class NewsBot2Evaluator:
    def __init__(self, newsbot_system=None) -> None:
        self.newsbot_system = newsbot_system
        self.results: dict = {}

    def evaluate_classification_performance(self, texts: Iterable[object], labels: Iterable[str]) -> dict:
        if self.newsbot_system is None: raise RuntimeError("An integrated system is required.")
        self.results["classification"] = self.newsbot_system.classifier.evaluate(texts, labels)
        return self.results["classification"]

    def evaluate_topic_modeling_quality(self) -> dict:
        if self.newsbot_system is None: raise RuntimeError("An integrated system is required.")
        values = self.newsbot_system.topic_engine.compare_models()
        self.results["topic_modeling"] = {"models": values, "selected_model": self.newsbot_system.topic_engine.selected_model}
        return self.results["topic_modeling"]

    @staticmethod
    def semantic_search_metrics(results: list[list[dict]], expected_ids: list[set], k: int = 5) -> dict:
        hits = [bool({str(item.get("article_id")) for item in returned[:k]} & expected) for returned, expected in zip(results, expected_ids)]
        return {"hit_rate_at_k": float(np.mean(hits)) if hits else 0.0, "queries": len(hits), "k": k}

    @staticmethod
    def conversation_accuracy(predictions: list[str], expected: list[str]) -> dict:
        return {"intent_accuracy": float(accuracy_score(expected, predictions)) if expected else 0.0, "queries": len(expected)}

    def generate_evaluation_report(self, path=None) -> dict:
        if path is not None: export_json(self.results, path)
        return self.results
