"""Lazy transformer summarization with a deterministic extractive fallback."""

from __future__ import annotations

import re
from collections import Counter


class IntelligentSummarizer:
    """Summarize entered or multi-document text without making the app fragile.

    The pretrained DistilBART path is deliberately opt-in through configuration.
    This keeps the required local/Colab fallback reliable while allowing the
    notebook and deployed app to demonstrate model-backed summarization when a
    model is available.
    """

    def __init__(self, model_name="sshleifer/distilbart-cnn-12-6", use_transformer=False, local_files_only=False):
        self.model_name = model_name
        self.use_transformer = use_transformer
        self.local_files_only = local_files_only
        self._pipeline = None
        self.warning = None
        self.backend = "extractive"

    def _load(self):
        if not self.use_transformer:
            return None
        if self._pipeline is None:
            try:
                import torch
                from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

                tokenizer = AutoTokenizer.from_pretrained(self.model_name, local_files_only=self.local_files_only)
                model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name, local_files_only=self.local_files_only)
                self._pipeline = pipeline(
                    "summarization", model=model, tokenizer=tokenizer,
                    device=0 if torch.cuda.is_available() else -1,
                )
                self.backend = "transformer"
            except Exception as exc:  # Runtime/model availability is intentionally non-fatal.
                self.warning = f"Transformer unavailable; extractive fallback used ({type(exc).__name__})."
                self.backend = "extractive"
        return self._pipeline

    def backend_status(self):
        """Return an explicit description of the active summarization path."""
        return {
            "backend": self.backend,
            "model": self.model_name if self.backend == "transformer" else None,
            "transformer_requested": self.use_transformer,
            "warning": self.warning,
        }

    @staticmethod
    def _sentences(text):
        return [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", str(text or "")) if sentence.strip()]

    def _extractive(self, text, max_words):
        sentences = self._sentences(text)
        words = re.findall(r"[A-Za-z']+", str(text).lower())
        frequency = Counter(word for word in words if len(word) > 2)
        ranked = sorted(
            enumerate(sentences),
            key=lambda item: sum(frequency[word.lower()] for word in re.findall(r"[A-Za-z']+", item[1])) / (len(item[1].split()) + 1),
            reverse=True,
        )
        chosen, word_count = [], 0
        for _, sentence in sorted(ranked[: max(1, min(3, len(ranked)))]):
            if word_count + len(sentence.split()) <= max_words or not chosen:
                chosen.append(sentence)
                word_count += len(sentence.split())
        return " ".join(chosen)

    def summarize_article(self, text, summary_type="balanced"):
        limits = {"brief": 45, "balanced": 80, "detailed": 120}
        max_words = limits.get(summary_type, 80)
        value = str(text or "").strip()
        if not value:
            return ""
        pipe = self._load()
        if pipe and len(value.split()) > 40:
            try:
                return pipe(value[:12000], max_length=max_words, min_length=min(25, max_words // 2), do_sample=False)[0]["summary_text"]
            except Exception as exc:
                self.warning = f"Transformer summarization failed; extractive fallback used ({type(exc).__name__})."
                self.backend = "extractive"
        return self._extractive(value, max_words)

    def summarize_multiple_articles(self, articles, focus_topic=None):
        selected = [str(article.get("full_text") or article.get("text") or article) if isinstance(article, dict) else str(article) for article in articles]
        if focus_topic:
            selected = [text for text in selected if focus_topic.lower() in text.lower()] or selected
        return self.summarize_article(" ".join(selected), "detailed")

    def generate_headline(self, text):
        summary = self.summarize_article(text, "brief")
        return " ".join(summary.split()[:14]).rstrip(".,;:") or "News analysis summary"

    def assess_summary_quality(self, original_text, summary, reference=None):
        original_words = max(len(str(original_text).split()), 1)
        summary_words = len(str(summary).split())
        sentences = max(len(self._sentences(summary)), 1)
        words = re.findall(r"[A-Za-z]+", str(summary))
        syllables = sum(max(1, len(re.findall(r"[aeiouy]+", word.lower()))) for word in words)
        readability = 206.835 - 1.015 * (len(words) / sentences) - 84.6 * (syllables / max(len(words), 1))
        entities = re.findall(r"\b[A-Z][A-Za-z]+\b", str(original_text))
        result = {
            "compression_ratio": summary_words / original_words,
            "summary_words": summary_words,
            "length_within_target": 25 <= summary_words <= 120,
            "flesch_reading_ease": round(float(readability), 2),
            "entity_preservation_proxy": sum(token.lower() in str(summary).lower() for token in entities) / max(len(entities), 1),
            "backend": self.backend,
        }
        if reference:
            try:
                from rouge_score import rouge_scorer

                result["rougeL"] = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True).score(str(reference), str(summary))["rougeL"].fmeasure
            except Exception:
                result["rougeL"] = None
        return result
