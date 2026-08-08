"""Predictable, Unicode-safe preprocessing used by classical NLP modules."""

from __future__ import annotations

import html
import re
import unicodedata
from collections.abc import Iterable

try:  # Optional at import time; unit tests never trigger downloads.
    from nltk import word_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
except ImportError:  # pragma: no cover - requirements include nltk.
    word_tokenize = None
    stopwords = None
    WordNetLemmatizer = None


URL_PATTERN = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
EMAIL_PATTERN = re.compile(r"\S+@\S+")
HTML_PATTERN = re.compile(r"<[^>]+>")
WHITESPACE_PATTERN = re.compile(r"\s+")
TOKEN_PATTERN = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)?", re.UNICODE)


class TextPreprocessor:
    """Clean input while retaining meaningful Unicode letters and contractions."""

    def __init__(
        self,
        max_text_length: int = 20_000,
        remove_stopwords: bool = True,
        lemmatize: bool = True,
    ) -> None:
        self.max_text_length = max_text_length
        self.remove_stopwords = remove_stopwords
        self.lemmatize = lemmatize
        self._stop_words = self._load_stopwords() if remove_stopwords else set()
        self._lemmatizer = WordNetLemmatizer() if lemmatize and WordNetLemmatizer else None

    @staticmethod
    def _load_stopwords() -> set[str]:
        if stopwords is None:
            return set()
        try:
            return set(stopwords.words("english"))
        except LookupError:
            return set()

    def clean_text(self, text: object) -> str:
        if text is None:
            return ""
        normalized = unicodedata.normalize("NFKC", str(text))
        normalized = html.unescape(normalized)
        normalized = HTML_PATTERN.sub(" ", normalized)
        normalized = URL_PATTERN.sub(" ", normalized)
        normalized = EMAIL_PATTERN.sub(" ", normalized)
        normalized = WHITESPACE_PATTERN.sub(" ", normalized).strip()
        return normalized[: self.max_text_length]

    def tokenize(self, text: object) -> list[str]:
        cleaned = self.clean_text(text).lower()
        if not cleaned:
            return []
        if word_tokenize is not None:
            try:
                tokens = word_tokenize(cleaned)
            except LookupError:
                tokens = TOKEN_PATTERN.findall(cleaned)
        else:
            tokens = TOKEN_PATTERN.findall(cleaned)
        return [token for token in tokens if TOKEN_PATTERN.fullmatch(token)]

    def preprocess(self, text: object) -> str:
        """Return a normalized token string suited to vectorizers."""
        tokens = self.tokenize(text)
        if self._stop_words:
            tokens = [token for token in tokens if token not in self._stop_words]
        if self._lemmatizer is not None:
            try:
                tokens = [self._lemmatizer.lemmatize(token) for token in tokens]
            except LookupError:
                pass
        return " ".join(token for token in tokens if len(token) > 2)

    def preprocess_many(self, texts: Iterable[object]) -> list[str]:
        return [self.preprocess(text) for text in texts]
