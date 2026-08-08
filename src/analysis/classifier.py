"""Probability-aware extension of the midterm TF-IDF classifier comparison."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import joblib
import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from config import NewsBot2Config
from src.data_processing.feature_extractor import build_enhanced_features, build_word_tfidf
from src.data_processing.text_preprocessor import TextPreprocessor


CONTENT_FAMILY_MAP = {
    "POLITICS": "Public Affairs", "BUSINESS": "Business & Economy", "TECH": "Technology",
    "SPORTS": "Sports", "ENTERTAINMENT": "Culture & Entertainment", "WELLNESS": "Lifestyle & Wellness",
}


class AdvancedNewsClassifier:
    """Compare midterm-style models and deploy the strongest calibrated classifier."""

    def __init__(self, config: NewsBot2Config | None = None) -> None:
        self.config = config or NewsBot2Config()
        self.preprocessor = TextPreprocessor(self.config.max_text_length)
        self.model: Pipeline | None = None
        self.model_name: str | None = None
        self.evaluation_results: dict = {}

    def _candidates(self) -> dict[str, Pipeline]:
        seed = self.config.random_state
        return {
            "Multinomial Naive Bayes (midterm baseline)": Pipeline([
                ("features", build_word_tfidf()), ("classifier", MultinomialNB())]),
            "Logistic Regression (enhanced)": Pipeline([
                ("features", build_enhanced_features()),
                ("classifier", LogisticRegression(max_iter=3000, class_weight="balanced", random_state=seed)),
            ]),
            "Calibrated Linear SVM (enhanced)": Pipeline([
                ("features", build_enhanced_features()),
                ("classifier", CalibratedClassifierCV(LinearSVC(class_weight="balanced", random_state=seed), cv=3)),
            ]),
        }

    def fit(self, texts: Iterable[object], labels: Iterable[str], *, compare_models: bool = True) -> "AdvancedNewsClassifier":
        X = self.preprocessor.preprocess_many(texts)
        y = np.asarray(list(labels), dtype=str)
        if len(X) != len(y) or len(set(y)) < 2:
            raise ValueError("Training requires equally sized texts/labels and at least two classes.")
        candidates = self._candidates()
        if compare_models and min(np.bincount(np.unique(y, return_inverse=True)[1])) >= 3:
            train_X, test_X, train_y, test_y = train_test_split(
                X, y, test_size=0.2, random_state=self.config.random_state, stratify=y
            )
            comparisons: list[dict] = []
            fitted: dict[str, Pipeline] = {}
            for name, candidate in candidates.items():
                candidate.fit(train_X, train_y)
                prediction = candidate.predict(test_X)
                comparisons.append({
                    "model": name, "accuracy": float(accuracy_score(test_y, prediction)),
                    "macro_f1": float(f1_score(test_y, prediction, average="macro")),
                    "weighted_f1": float(f1_score(test_y, prediction, average="weighted")),
                })
                fitted[name] = candidate
            best = max(comparisons, key=lambda item: (item["macro_f1"], item["accuracy"]))
            self.model_name = best["model"]
            self.evaluation_results = self._metrics(
                test_y, fitted[self.model_name].predict(test_X), comparisons,
                fitted[self.model_name].predict_proba(test_X),
            )
            self.model = candidates[self.model_name].fit(X, y)
        else:
            self.model_name = "Logistic Regression (enhanced)"
            self.model = candidates[self.model_name].fit(X, y)
            self.evaluation_results = {"model_comparison": [], "selection_note": "Small corpus: fitted stable probabilistic enhanced model without holdout comparison."}
        return self

    @staticmethod
    def _calibration_metrics(y_true: np.ndarray, prediction: np.ndarray, probabilities: np.ndarray | None) -> dict:
        """Report transparent top-label calibration rather than a misleading binary score."""
        if probabilities is None or not len(y_true):
            return {"expected_calibration_error": None, "mean_confidence": None, "top_label_accuracy": None}
        confidence = probabilities.max(axis=1)
        correct = (prediction == y_true).astype(float)
        bins = np.linspace(0, 1, 11)
        ece = 0.0
        for lower, upper in zip(bins[:-1], bins[1:]):
            mask = (confidence >= lower) & ((confidence < upper) if upper < 1 else (confidence <= upper))
            if mask.any():
                ece += abs(float(confidence[mask].mean()) - float(correct[mask].mean())) * float(mask.mean())
        return {
            "expected_calibration_error": float(ece),
            "mean_confidence": float(confidence.mean()),
            "top_label_accuracy": float(correct.mean()),
            "interpretation": "Top-label expected calibration error on the held-out split; lower is better.",
        }

    def _metrics(self, y_true: np.ndarray, prediction: np.ndarray, comparisons: list[dict], probabilities: np.ndarray | None = None) -> dict:
        p, r, f, _ = precision_recall_fscore_support(y_true, prediction, average="macro", zero_division=0)
        return {
            "selected_model": self.model_name, "accuracy": float(accuracy_score(y_true, prediction)),
            "macro_precision": float(p), "macro_recall": float(r), "macro_f1": float(f),
            "weighted_f1": float(f1_score(y_true, prediction, average="weighted")),
            "per_class": classification_report(y_true, prediction, output_dict=True, zero_division=0),
            "confusion_matrix": confusion_matrix(y_true, prediction, labels=sorted(set(y_true))).tolist(),
            "labels": sorted(set(y_true)), "model_comparison": comparisons,
            "calibration": self._calibration_metrics(y_true, prediction, probabilities),
        }

    def _require_model(self) -> Pipeline:
        if self.model is None:
            raise RuntimeError("Classifier has not been fitted or loaded.")
        return self.model

    def predict(self, texts: Iterable[object]) -> list[str]:
        return self._require_model().predict(self.preprocessor.preprocess_many(texts)).tolist()

    def predict_with_confidence(self, text: object, top_n: int = 3) -> dict:
        model = self._require_model()
        probabilities = model.predict_proba(self.preprocessor.preprocess_many([text]))[0]
        ranked = sorted(zip(model.classes_, probabilities), key=lambda item: item[1], reverse=True)
        primary, confidence = ranked[0]
        return {
            "primary_category": str(primary), "content_family": CONTENT_FAMILY_MAP.get(str(primary), "Other"),
            "confidence": float(confidence),
            "alternatives": [{"category": str(label), "confidence": float(score)} for label, score in ranked[1:top_n]],
            "manual_review_recommended": bool(confidence < self.config.confidence_threshold),
        }

    def explain_prediction(self, text: object, top_n: int = 10) -> dict:
        result = self.predict_with_confidence(text)
        model = self._require_model()
        classifier = model.named_steps["classifier"]
        if not isinstance(classifier, LogisticRegression):
            return {**result, "top_features": [], "explanation_note": "Feature coefficients are available for the logistic-regression model only."}
        features = model.named_steps["features"]
        names = features.get_feature_names_out()
        class_index = list(classifier.classes_).index(result["primary_category"])
        transformed = features.transform(self.preprocessor.preprocess_many([text])).toarray()[0]
        scores = transformed * classifier.coef_[class_index]
        indices = np.argsort(scores)[-top_n:][::-1]
        return {**result, "top_features": [{"feature": str(names[i]), "contribution": float(scores[i])} for i in indices if scores[i] > 0], "explanation_note": "Linear feature association, not causal reasoning."}

    def evaluate(self, texts: Iterable[object], labels: Iterable[str]) -> dict:
        texts = list(texts)
        y = np.asarray(list(labels), dtype=str)
        prediction = np.asarray(self.predict(texts), dtype=str)
        model = self._require_model()
        probabilities = model.predict_proba(self.preprocessor.preprocess_many(texts))
        return self._metrics(y, prediction, [], probabilities)

    def save(self, path: str | Path) -> None:
        joblib.dump(self, Path(path))

    @classmethod
    def load(cls, path: str | Path) -> "AdvancedNewsClassifier":
        return joblib.load(Path(path))
