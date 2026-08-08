"""Transparent VADER-led sentiment evolution, extending the midterm implementation."""

from __future__ import annotations

import re
from typing import Iterable

import numpy as np
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

try:
    from textblob import TextBlob
except ImportError:  # pragma: no cover
    TextBlob = None


EMOTION_WORDS = {"joy": {"joy", "happy", "win", "hope", "celebrate"}, "anger": {"anger", "angry", "outrage", "furious"}, "fear": {"fear", "risk", "threat", "crisis"}, "sadness": {"sad", "loss", "grief", "tragic"}, "trust": {"trust", "support", "secure", "reliable"}, "surprise": {"surprise", "unexpected", "sudden"}}


class SentimentEvolutionTracker:
    def __init__(self) -> None:
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze(self, text: object) -> dict:
        value = "" if text is None else str(text)
        scores = self.analyzer.polarity_scores(value)
        compound = float(scores["compound"])
        label = "positive" if compound >= 0.05 else "negative" if compound <= -0.05 else "neutral"
        tokens = set(re.findall(r"[A-Za-z']+", value.lower()))
        emotions = {emotion: sum(word in tokens for word in words) for emotion, words in EMOTION_WORDS.items()}
        phrases = [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", value) if sentence.strip()]
        ranked_phrases = sorted(phrases, key=lambda phrase: abs(self.analyzer.polarity_scores(phrase)["compound"]), reverse=True)[:3]
        subjectivity = float(TextBlob(value).sentiment.subjectivity) if TextBlob is not None and value.strip() else 0.0
        return {"label": label, "compound": compound, "positive": float(scores["pos"]), "neutral": float(scores["neu"]), "negative": float(scores["neg"]), "subjectivity": subjectivity, "emotions": emotions, "key_sentiment_phrases": ranked_phrases}

    def track_sentiment_over_time(self, dataframe: pd.DataFrame, text_column: str = "full_text") -> pd.DataFrame:
        df = dataframe.copy()
        if text_column not in df or "date" not in df:
            raise ValueError("Timeline requires text and date columns.")
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
        results = df[text_column].fillna("").map(self.analyze)
        df["compound"] = results.map(lambda item: item["compound"])
        df["sentiment_label"] = results.map(lambda item: item["label"])
        df["period"] = df["date"].dt.to_period("Y").astype(str)
        groups = ["period"] + (["category"] if "category" in df else [])
        return df.groupby(groups, as_index=False).agg(mean_compound=("compound", "mean"), article_count=("compound", "size"), positive_share=("sentiment_label", lambda values: float((values == "positive").mean())))

    def detect_sentiment_anomalies(self, timeline: pd.DataFrame, window: int = 3) -> pd.DataFrame:
        result = timeline.copy().sort_values("period")
        group_cols = ["category"] if "category" in result else []
        def mark(group: pd.DataFrame) -> pd.DataFrame:
            rolling = group["mean_compound"].rolling(window, min_periods=2).mean()
            std = group["mean_compound"].rolling(window, min_periods=2).std().replace(0, np.nan)
            group["rolling_mean"] = rolling
            group["z_score"] = ((group["mean_compound"] - rolling) / std).fillna(0.0)
            group["is_anomaly"] = group["z_score"].abs() >= 2.0
            return group
        return result.groupby(group_cols, group_keys=False).apply(mark, include_groups=False) if group_cols else mark(result)
