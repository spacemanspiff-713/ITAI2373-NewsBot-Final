"""Central, environment-safe settings for NewsBot 2.0."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class NewsBot2Config:
    """Runtime configuration with reproducible defaults.

    Secrets are intentionally read from environment variables rather than stored
    in project files. Paths resolve from the repository root by default.
    """

    random_state: int = 42
    max_text_length: int = 20_000
    max_batch_size: int = field(
        default_factory=lambda: int(os.getenv("NEWSBOT_MAX_BATCH_SIZE", "20"))
    )
    classification_categories: tuple[str, ...] = (
        "POLITICS",
        "ENTERTAINMENT",
        "BUSINESS",
        "SPORTS",
        "TECH",
        "WELLNESS",
    )
    topic_count: int = 8
    topic_top_words: int = 12
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    summarization_model: str = "sshleifer/distilbart-cnn-12-6"
    enable_transformers: bool = field(
        default_factory=lambda: os.getenv("NEWSBOT_ENABLE_TRANSFORMERS", "0").strip().lower()
        in {"1", "true", "yes", "on"}
    )
    transformer_local_files_only: bool = field(
        default_factory=lambda: os.getenv("NEWSBOT_TRANSFORMERS_LOCAL_ONLY", "0").strip().lower()
        in {"1", "true", "yes", "on"}
    )
    min_summary_words: int = 25
    max_summary_words: int = 120
    translation_backend: str = field(
        default_factory=lambda: os.getenv("NEWSBOT_TRANSLATION_BACKEND", "auto")
    )
    confidence_threshold: float = 0.55
    project_root: Path = field(
        default_factory=lambda: Path(__file__).resolve().parents[1]
    )

    @property
    def processed_data_path(self) -> Path:
        return self.project_root / "data" / "processed" / "newsbot_dataset_sample.csv"

    @property
    def results_path(self) -> Path:
        return self.project_root / "data" / "results"

    @property
    def secret_key(self) -> str | None:
        return os.getenv("NEWSBOT_SECRET_KEY")
