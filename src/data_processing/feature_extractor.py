"""Feature constructors shared by baseline and enhanced classifiers."""

from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion


def build_word_tfidf() -> TfidfVectorizer:
    return TfidfVectorizer(
        lowercase=True,
        strip_accents="unicode",
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95,
        sublinear_tf=True,
        max_features=30_000,
    )


def build_enhanced_features() -> FeatureUnion:
    """Combine word and character n-grams for robust short-news classification."""
    return FeatureUnion(
        [
            ("word", build_word_tfidf()),
            (
                "char",
                TfidfVectorizer(
                    analyzer="char_wb",
                    ngram_range=(3, 5),
                    min_df=2,
                    max_features=25_000,
                    sublinear_tf=True,
                ),
            ),
        ]
    )
