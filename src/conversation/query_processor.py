"""Deterministic parameter extraction for grounded local-corpus queries."""

from __future__ import annotations

import re
from datetime import timedelta

import pandas as pd

from src.conversation.intent_classifier import IntentClassifier


CATEGORIES = {
    "politics": "POLITICS", "entertainment": "ENTERTAINMENT", "business": "BUSINESS",
    "sports": "SPORTS", "tech": "TECH", "technology": "TECH", "wellness": "WELLNESS",
}


class QueryProcessor:
    def __init__(self, intent_classifier=None):
        self.intent_classifier = intent_classifier or IntentClassifier()

    def parse(self, query, dataset_max_date=None, context=None):
        value = str(query or "").strip()
        low = value.lower()
        intent = self.intent_classifier.classify_intent(value)
        parameters = {"raw_query": value}
        for word, category in CATEGORIES.items():
            if re.search(r"\b" + re.escape(word) + r"\b", low):
                parameters["category"] = category
                break
        for sentiment in ("positive", "negative", "neutral"):
            if sentiment in low:
                parameters["sentiment"] = sentiment
        count = re.search(r"\b(\d+)\b", low)
        if count:
            parameters["count"] = min(int(count.group(1)), 20)

        if dataset_max_date and "this week" in low:
            end = pd.Timestamp(dataset_max_date)
            start = end - timedelta(days=6)
            parameters.update({
                "date_start": start.date().isoformat(), "date_end": end.date().isoformat(),
                "timeframe_note": f"'This week' is resolved relative to the historical dataset maximum date ({end.date().isoformat()}).",
            })
        elif dataset_max_date and "this month" in low:
            end = pd.Timestamp(dataset_max_date)
            start = end - timedelta(days=29)
            parameters.update({
                "date_start": start.date().isoformat(), "date_end": end.date().isoformat(),
                "timeframe_note": f"'This month' is resolved relative to the historical dataset maximum date ({end.date().isoformat()}).",
            })

        comparison = re.search(r"compare\s+(.+?)\s+(?:and|with|to|versus|vs\.? )\s+(.+?)(?:\?|$)", low)
        if comparison:
            parameters["comparison_targets"] = [comparison.group(1).strip(), comparison.group(2).strip()]
        about = re.search(r"\b(?:about|around|on)\s+([\w\s-]{2,60})(?:\?|$)", low)
        if about:
            parameters["topic_keyword"] = about.group(1).strip()
        command_words = {"Show", "Find", "What", "How", "Compare", "Summarize", "Help", "Tell", "Give"}
        entities = [entity for entity in re.findall(r"\b[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*\b", value) if entity not in command_words]
        if entities:
            parameters["entities"] = entities
        if context and not parameters.get("category") and context.get("last_filters", {}).get("category"):
            parameters["category"] = context["last_filters"]["category"]
            parameters["inherited_category"] = True
        return {**intent, "parameters": parameters}
