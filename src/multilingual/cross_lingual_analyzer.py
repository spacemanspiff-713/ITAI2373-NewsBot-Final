"""Conservative cross-language comparison with transparent translation evidence."""

from __future__ import annotations

from collections import Counter

from src.language_models.embeddings import SemanticSearchEngine
from src.multilingual.language_detector import LanguageDetector
from src.multilingual.translator import Translator


class CrossLingualAnalyzer:
    def __init__(self, search_engine=None, translator=None):
        self.search_engine = search_engine
        self.translator = translator or Translator()
        self.detector = LanguageDetector()

    def _english_proxy(self, text):
        detected = self.detector.detect_language(text)
        language = detected["language"]
        if language in {"en", "unknown"}:
            return str(text), {
                "translation": str(text), "available": language == "en",
                "backend": "identity" if language == "en" else "unavailable",
                "warning": detected.get("warning"),
            }
        translated = self.translator.translate_text(text, "en", language)
        return translated.get("translation") or str(text), translated

    def cross_lingual_similarity(self, text_a, text_b):
        """Compare a pair without mutating the main corpus retrieval index."""
        left, left_translation = self._english_proxy(text_a)
        right, right_translation = self._english_proxy(text_b)
        isolated_engine = SemanticSearchEngine(
            getattr(self.search_engine, "model_name", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"),
            getattr(self.search_engine, "use_transformer", False),
        ).build_index([left, right])
        result = isolated_engine.semantic_search(left, 2)[1]
        return {
            "similarity": float(result["score"]),
            "backend": isolated_engine.backend,
            "left_translation": left_translation,
            "right_translation": right_translation,
        }

    def compare_entities(self, entities_a, entities_b):
        left = {str(entity["text"]).lower() for entity in entities_a}
        right = {str(entity["text"]).lower() for entity in entities_b}
        return {"overlapping_entities": sorted(left & right), "overlap_count": len(left & right)}

    def compare_sentiment(self, first, second):
        return {
            "compound_difference": float(first.get("compound", 0) - second.get("compound", 0)),
            "labels": [first.get("label"), second.get("label")],
        }

    def compare_coverage(self, articles_by_language):
        counts = {language: len(items) for language, items in articles_by_language.items()}
        topic_counts = {
            language: dict(Counter(str(item.get("topic", "unlabeled")) for item in items if isinstance(item, dict)))
            for language, items in articles_by_language.items()
        }
        languages = list(articles_by_language)
        comparisons = []
        if len(languages) >= 2 and articles_by_language[languages[0]] and articles_by_language[languages[1]]:
            first, second = languages[:2]
            first_item = articles_by_language[first][0]
            second_item = articles_by_language[second][0]
            first_text = first_item.get("text", "") if isinstance(first_item, dict) else str(first_item)
            second_text = second_item.get("text", "") if isinstance(second_item, dict) else str(second_item)
            comparisons.append({"languages": [first, second], **self.cross_lingual_similarity(first_text, second_text)})
        return {
            "coverage_depth": counts,
            "topic_counts": topic_counts,
            "comparisons": comparisons,
            "language_specific_framing_signal": "Descriptive coverage difference only; this does not establish cultural understanding or a regional viewpoint.",
        }
