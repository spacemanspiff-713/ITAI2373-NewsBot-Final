"""Small supervised intent model with transparent high-precision fallback rules."""

from __future__ import annotations

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


EXAMPLES = {
    "search": ["show tech news", "recent business coverage", "show wellness news from this week", "find news about technology", "browse sports coverage"],
    "summarize": ["summarize politics coverage", "give me a summary", "what happened in sports", "brief me on business coverage"],
    "sentiment": ["show negative news", "what is the sentiment", "positive technology stories", "what tone is politics coverage"],
    "topic_trend": ["how has technology changed over time", "topic trends", "emerging topics", "show trends in the coverage"],
    "entity_lookup": ["find articles about Google", "who is mentioned", "look up Apple", "find coverage about Biden"],
    "compare": ["compare Apple and Google coverage", "compare tech and business", "difference between categories", "contrast sports with entertainment"],
    "similar_articles": ["find similar articles", "articles like this paragraph", "related stories", "show related coverage"],
    "help": ["help", "what can you do", "how does this work", "show available commands"],
}


class IntentClassifier:
    def __init__(self):
        texts = [text for intent, examples in EXAMPLES.items() for text in examples]
        labels = [intent for intent, examples in EXAMPLES.items() for _ in examples]
        self.model = Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
        ]).fit(texts, labels)

    @staticmethod
    def _rule_intent(value):
        low = value.lower().strip()
        if re.fullmatch(r"help|what can you do|how does this work|show available commands", low):
            return "help"
        if "similar" in low or "related" in low:
            return "similar_articles"
        if low.startswith(("summarize", "summary", "brief me")):
            return "summarize"
        if low.startswith("compare") or "difference between" in low or "contrast " in low:
            return "compare"
        if "topic" in low and any(word in low for word in ("trend", "change", "emerging", "over time")):
            return "topic_trend"
        if ("about" in low and re.search(r"\b[A-Z][A-Za-z]+\b", value)) or "who is mentioned" in low or low.startswith("look up"):
            return "entity_lookup"
        if any(word in low for word in ("sentiment", "tone")):
            return "sentiment"
        if any(word in low for word in ("positive", "negative", "neutral")) and "this week" not in low and "this month" not in low:
            return "sentiment"
        if low.startswith(("show", "find", "browse", "recent")):
            return "search"
        return None

    def classify_intent(self, query):
        value = str(query or "")
        probabilities = self.model.predict_proba([value])[0]
        index = probabilities.argmax()
        model_intent, model_confidence = self.model.classes_[index], float(probabilities[index])
        rule_intent = self._rule_intent(value)
        if rule_intent:
            return {"intent": rule_intent, "confidence": max(model_confidence, 0.75), "fallback": False, "source": "rule+supervised"}
        return {"intent": model_intent, "confidence": model_confidence, "fallback": bool(model_confidence < 0.35), "source": "supervised"}
