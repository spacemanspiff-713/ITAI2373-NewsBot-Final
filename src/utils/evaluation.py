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
        hits, precision, recall = [], [], []
        for returned, expected in zip(results, expected_ids):
            returned_ids = {str(item.get("article_id")) for item in returned[:k]}
            overlap = returned_ids & {str(item) for item in expected}
            hits.append(bool(overlap))
            precision.append(len(overlap) / max(len(returned_ids), 1))
            recall.append(len(overlap) / max(len(expected), 1))
        return {
            "precision_at_k": float(np.mean(precision)) if precision else 0.0,
            "recall_at_k": float(np.mean(recall)) if recall else 0.0,
            "hit_rate_at_k": float(np.mean(hits)) if hits else 0.0,
            "queries": len(hits), "k": k,
        }

    @staticmethod
    def conversation_accuracy(predictions: list[str], expected: list[str]) -> dict:
        return {"intent_accuracy": float(accuracy_score(expected, predictions)) if expected else 0.0, "queries": len(expected)}

    @staticmethod
    def parameter_accuracy(predicted_rows: list[dict], expected_rows: list[dict], fields=("category", "sentiment", "entities")) -> dict:
        scores = {}
        for field in fields:
            matches = [predicted.get(field) == expected.get(field) for predicted, expected in zip(predicted_rows, expected_rows) if field in expected]
            scores[field] = float(np.mean(matches)) if matches else None
        measured = [score for score in scores.values() if score is not None]
        return {"slot_accuracy": float(np.mean(measured)) if measured else 0.0, "by_field": scores, "queries": len(expected_rows)}

    def generate_evaluation_report(self, path=None) -> dict:
        if path is not None: export_json(self.results, path)
        return self.results
