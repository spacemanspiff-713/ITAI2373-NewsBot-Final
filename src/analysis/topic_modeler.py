"""LDA and NMF topic discovery with reproducible trend summaries."""

from __future__ import annotations

from collections import Counter
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation, NMF
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


class TopicDiscoveryEngine:
    def __init__(self, n_topics: int = 8, random_state: int = 42, top_words: int = 12) -> None:
        self.n_topics, self.random_state, self.top_words = n_topics, random_state, top_words
        self.lda_vectorizer = CountVectorizer(stop_words="english", min_df=2, max_df=0.95)
        self.nmf_vectorizer = TfidfVectorizer(stop_words="english", min_df=2, max_df=0.95, ngram_range=(1, 2))
        self.lda_model = LatentDirichletAllocation(n_components=n_topics, random_state=random_state, learning_method="batch")
        self.nmf_model = NMF(n_components=n_topics, random_state=random_state, init="nndsvda", max_iter=500)
        self.documents: list[str] = []; self.dates = None; self.selected_model = "nmf"

    def fit_topics(self, documents: Iterable[object], dates: Iterable[object] | None = None) -> "TopicDiscoveryEngine":
        self.documents = [str(document or "") for document in documents]
        if len(self.documents) < self.n_topics:
            raise ValueError("Number of documents must be at least n_topics.")
        lda_matrix = self.lda_vectorizer.fit_transform(self.documents)
        nmf_matrix = self.nmf_vectorizer.fit_transform(self.documents)
        self.lda_doc_topics = self.lda_model.fit_transform(lda_matrix)
        self.nmf_doc_topics = self.nmf_model.fit_transform(nmf_matrix)
        self.dates = pd.to_datetime(list(dates), errors="coerce") if dates is not None else None
        comparison = self.compare_models(self.documents)
        self.selected_model = max(comparison, key=lambda item: (item["topic_diversity"], item["coherence_proxy"]))["model"]
        return self

    def _model_parts(self, model: str | None = None):
        name = model or self.selected_model
        return (self.lda_model, self.lda_vectorizer, self.lda_doc_topics) if name.lower() == "lda" else (self.nmf_model, self.nmf_vectorizer, self.nmf_doc_topics)

    def get_topic_words(self, topic_id: int, n_words: int = 10, model: str | None = None) -> list[dict]:
        estimator, vectorizer, _ = self._model_parts(model)
        if not 0 <= topic_id < self.n_topics:
            raise IndexError("topic_id is out of range")
        names = vectorizer.get_feature_names_out(); scores = estimator.components_[topic_id]
        indices = np.argsort(scores)[-n_words:][::-1]
        return [{"word": str(names[i]), "weight": float(scores[i])} for i in indices]

    def get_article_topics(self, article_text: object, model: str | None = None) -> list[dict]:
        estimator, vectorizer, _ = self._model_parts(model)
        distribution = estimator.transform(vectorizer.transform([str(article_text or "")]))[0]
        return [{"topic_id": int(i), "probability": float(score), "words": self.get_topic_words(int(i), 5, model)} for i, score in sorted(enumerate(distribution), key=lambda item: item[1], reverse=True)]

    def compare_models(self, documents: Iterable[object] | None = None) -> list[dict]:
        del documents
        results = []
        for name in ("lda", "nmf"):
            words = [item["word"] for topic in range(self.n_topics) for item in self.get_topic_words(topic, self.top_words, name)]
            diversity = len(set(words)) / max(len(words), 1)
            # A transparent lexical-overlap proxy, not a claim of human coherence.
            topic_sets = [set(item["word"] for item in self.get_topic_words(topic, self.top_words, name)) for topic in range(self.n_topics)]
            overlaps = [len(left & right) / max(len(left | right), 1) for i, left in enumerate(topic_sets) for right in topic_sets[i + 1:]]
            results.append({"model": name, "topic_diversity": float(diversity), "coherence_proxy": float(1 - np.mean(overlaps) if overlaps else 1.0), "interpretation": "Compare top-word distinctiveness; validate qualitative meaning in the notebook."})
        return results

    def track_topic_trends(self, articles_with_dates: pd.DataFrame | None = None) -> dict:
        if articles_with_dates is None:
            if self.dates is None: raise ValueError("Dates are required for topic trends.")
            dates = self.dates
        else:
            dates = pd.to_datetime(articles_with_dates["date"], errors="coerce")
        _, _, matrix = self._model_parts()
        frame = pd.DataFrame(matrix, columns=[f"topic_{i}" for i in range(self.n_topics)])
        frame["date"] = dates
        frame = frame.dropna(subset=["date"]); frame["period"] = frame["date"].dt.to_period("Y").astype(str)
        trend = frame.groupby("period", as_index=False)[[f"topic_{i}" for i in range(self.n_topics)]].mean()
        slopes = {column: float(np.polyfit(range(len(trend)), trend[column], 1)[0]) if len(trend) > 1 else 0.0 for column in trend.columns if column.startswith("topic_")}
        return {"timeline": trend, "emerging_topics": sorted(slopes, key=slopes.get, reverse=True)[:3], "declining_topics": sorted(slopes, key=slopes.get)[:3], "spikes": {column: str(trend.loc[trend[column].idxmax(), "period"]) for column in slopes if not trend.empty}}
