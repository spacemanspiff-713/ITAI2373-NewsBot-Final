"""Grounded, intent-specific conversation responses over the stored corpus."""

from __future__ import annotations

import re

import pandas as pd


CATEGORIES = {
    "politics": "POLITICS", "entertainment": "ENTERTAINMENT", "business": "BUSINESS",
    "sports": "SPORTS", "tech": "TECH", "technology": "TECH", "wellness": "WELLNESS",
}


class ResponseGenerator:
    @staticmethod
    def _records(frame, count):
        rows = frame.sort_values("date", ascending=False).head(count)
        return [
            {"article_id": int(row.article_id), "title": row.title, "category": row.category, "date": str(pd.Timestamp(row.date).date())}
            for row in rows.itertuples()
        ]

    def _filter(self, dataframe, parameters, sentiment_tracker=None):
        filtered = dataframe.copy()
        if parameters.get("category"):
            filtered = filtered[filtered["category"] == parameters["category"]]
        if parameters.get("entities"):
            pattern = "|".join(re.escape(entity) for entity in parameters["entities"])
            filtered = filtered[filtered["full_text"].str.contains(pattern, case=False, na=False, regex=True)]
        if parameters.get("topic_keyword"):
            filtered = filtered[filtered["full_text"].str.contains(re.escape(parameters["topic_keyword"]), case=False, na=False, regex=True)]
        if parameters.get("date_start"):
            dates = pd.to_datetime(filtered["date"], errors="coerce")
            filtered = filtered[dates.between(parameters["date_start"], parameters.get("date_end", pd.Timestamp.max))]
        if parameters.get("sentiment") and sentiment_tracker is not None:
            labels = filtered["full_text"].map(lambda text: sentiment_tracker.analyze(text)["label"])
            filtered = filtered[labels == parameters["sentiment"]]
        return filtered

    @staticmethod
    def _applied(parameters):
        excluded = {"entities", "count", "inherited_category", "raw_query", "comparison_targets", "date_start", "date_end"}
        return ", ".join(f"{key}={value}" for key, value in parameters.items() if key not in excluded) or "no filters"

    def respond(self, query_data, dataframe, search_engine=None, topic_engine=None, sentiment_tracker=None, summarizer=None):
        parameters = query_data["parameters"]
        intent = query_data["intent"]
        count = parameters.get("count", 5)
        filtered = self._filter(dataframe, parameters, sentiment_tracker)
        records = self._records(filtered, count)
        applied = self._applied(parameters)

        if intent == "help":
            return {
                "response": "I can search the historical corpus, summarize coverage, describe sentiment, track topics, compare local coverage, find similar articles, and carry a category into a follow-up.",
                "results": [], "applied_filters": parameters,
                "next_actions": ["Try: Show me tech news", "Try: Summarize politics coverage", "Try: Compare tech and business"],
            }
        if intent == "summarize":
            source = filtered.head(min(count, 8)).to_dict("records")
            summary = summarizer.summarize_multiple_articles(source, parameters.get("topic_keyword")) if summarizer else " ".join(item["title"] for item in records)
            return {"response": f"Summary of {len(filtered)} matching historical articles with {applied}: {summary}", "results": records, "applied_filters": parameters, "next_actions": ["Ask for sentiment or topic trends for this coverage."]}
        if intent == "sentiment":
            if sentiment_tracker is None:
                detail = "Sentiment analysis is unavailable in this response context."
            else:
                labels = filtered["full_text"].map(lambda text: sentiment_tracker.analyze(text)["label"])
                compound = filtered["full_text"].map(lambda text: sentiment_tracker.analyze(text)["compound"])
                detail = f"Tone distribution: {labels.value_counts().to_dict()}; mean VADER compound: {compound.mean():+.3f}."
            return {"response": f"{detail} Based on {len(filtered)} matching historical articles with {applied}.", "results": records, "applied_filters": parameters, "next_actions": ["Ask for titles behind a sentiment label or compare two coverage areas."]}
        if intent == "topic_trend":
            if topic_engine is None:
                detail = "Topic trend analysis is unavailable in this response context."
            else:
                trends = topic_engine.track_topic_trends()
                detail = f"Emerging topic IDs: {', '.join(trends['emerging_topics'])}; declining topic IDs: {', '.join(trends['declining_topics'])}. These are historical corpus trends, not live news."
            return {"response": detail, "results": records, "applied_filters": parameters, "next_actions": ["Ask for a category filter or inspect the topic visualization."]}
        if intent == "compare":
            targets = parameters.get("comparison_targets", [])
            categories = [CATEGORIES.get(target.strip().lower()) for target in targets]
            categories = [category for category in categories if category]
            if len(categories) == 2:
                comparison = {}
                for category in categories:
                    subset = dataframe[dataframe["category"] == category]
                    comparison[category] = {"articles": int(len(subset)), "latest_date": str(pd.to_datetime(subset["date"]).max().date())}
                detail = f"Local coverage comparison: {comparison}. Counts describe this balanced historical sample, not real-world importance."
            else:
                detail = "I can compare two named categories such as technology and business. Entity comparisons remain limited to local corpus mentions."
            return {"response": detail, "results": records, "applied_filters": parameters, "next_actions": ["Ask about sentiment or summaries within either category."]}
        if intent == "similar_articles" and search_engine is not None:
            query = parameters.get("raw_query", "")
            filters = {"category": parameters["category"]} if parameters.get("category") else None
            similar = search_engine.semantic_search(query, count, filters)
            result_records = [{key: value for key, value in item.items() if key in {"article_id", "title", "category", "date", "score", "retrieval_backend"}} for item in similar]
            return {"response": f"Found {len(result_records)} related local records using {search_engine.backend_status()['backend']} retrieval. Similarity is topical proximity, not factual agreement.", "results": result_records, "applied_filters": parameters, "next_actions": ["Ask for a summary of these related records."]}
        return {"response": f"Found {len(filtered)} matching historical articles with {applied}.", "results": records, "applied_filters": parameters, "next_actions": ["Ask for a summary, sentiment, trend, comparison, or related articles."]}
