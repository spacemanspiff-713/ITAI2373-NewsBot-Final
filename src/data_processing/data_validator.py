"""Dataset loading and transparent quality checks for the HuffPost sample."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd

from config import NewsBot2Config


REQUIRED_COLUMNS = ("headline", "short_description", "category", "authors", "date", "full_text")
ALIASES = {"headline": "title", "short_description": "content"}


@dataclass(frozen=True)
class ValidationReport:
    valid: bool
    row_count: int
    columns: list[str]
    categories: dict[str, int]
    missing_by_column: dict[str, int]
    duplicate_rows: int
    invalid_dates: int
    date_min: str | None
    date_max: str | None
    warnings: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


def normalize_news_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Normalize midterm column names without altering the source CSV."""
    df = dataframe.copy()
    for canonical, alias in ALIASES.items():
        if canonical not in df.columns and alias in df.columns:
            df[canonical] = df[alias]
    for column in ("headline", "short_description", "authors"):
        if column not in df.columns:
            df[column] = ""
        df[column] = df[column].fillna("").astype(str)
    if "category" not in df.columns:
        raise ValueError("Dataset must contain a category column.")
    if "date" not in df.columns:
        df["date"] = pd.NaT
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    if "full_text" not in df.columns:
        df["full_text"] = ""
    df["full_text"] = df["full_text"].fillna("").astype(str)
    empty_full_text = df["full_text"].str.strip().eq("")
    df.loc[empty_full_text, "full_text"] = (
        df.loc[empty_full_text, "headline"].str.strip()
        + ". "
        + df.loc[empty_full_text, "short_description"].str.strip()
    ).str.strip()
    return df


def load_news_dataset(
    path: str | Path | None = None, config: NewsBot2Config | None = None
) -> pd.DataFrame:
    """Load the copied midterm sample deterministically and normalize its schema."""
    runtime_config = config or NewsBot2Config()
    csv_path = Path(path) if path else runtime_config.processed_data_path
    if not csv_path.exists():
        raise FileNotFoundError(f"NewsBot dataset not found: {csv_path}")
    return normalize_news_columns(pd.read_csv(csv_path, low_memory=False))


def build_balanced_sample(
    raw_path: str | Path,
    *,
    rows_per_category: int = 300,
    min_words: int = 15,
    random_state: int = 42,
    categories: Iterable[str] | None = None,
) -> pd.DataFrame:
    """Reproduce the midterm's prepared HuffPost sample from a JSON Lines source.

    This is deliberately an explicit rebuild utility; the committed final project
    continues to use the copied prepared CSV and never silently replaces it.
    """
    allowed_categories = tuple(categories or NewsBot2Config().classification_categories)
    raw_file = Path(raw_path)
    if not raw_file.exists():
        raise FileNotFoundError(f"Raw HuffPost JSON Lines file not found: {raw_file}")
    raw_df = pd.read_json(raw_file, lines=True)
    required = {"headline", "short_description", "category", "date"}
    missing = required - set(raw_df.columns)
    if missing:
        raise ValueError(f"Raw dataset is missing required columns: {sorted(missing)}")

    df = raw_df[raw_df["category"].isin(allowed_categories)].copy()
    df["headline"] = df["headline"].fillna("").astype(str).str.strip()
    df["short_description"] = df["short_description"].fillna("").astype(str).str.strip()
    df["authors"] = df.get("authors", "Unknown").fillna("Unknown").replace("", "Unknown")
    df["link"] = df.get("link", "").fillna("").astype(str)
    df["title"] = df["headline"]
    df["content"] = df["short_description"]
    df["full_text"] = (df["title"] + " " + df["content"]).str.replace(r"\s+", " ", regex=True).str.strip()
    df["source"] = "HuffPost"
    df = df[(df["title"].ne("")) & (df["content"].ne(""))]
    df = df[df["full_text"].str.split().str.len() >= min_words]

    parts: list[pd.DataFrame] = []
    for category in allowed_categories:
        category_df = df[df["category"] == category]
        if len(category_df) < rows_per_category:
            raise ValueError(
                f"{category} has {len(category_df)} eligible records; expected at least {rows_per_category}."
            )
        parts.append(category_df.sample(n=rows_per_category, random_state=random_state))
    sample = pd.concat(parts, ignore_index=True).sample(frac=1, random_state=random_state).reset_index(drop=True)
    sample["article_id"] = range(1, len(sample) + 1)
    sample["date"] = pd.to_datetime(sample["date"], errors="coerce").dt.strftime("%Y-%m-%d")
    return sample[["article_id", "title", "content", "full_text", "category", "authors", "source", "date", "link"]]


class DatasetValidator:
    """Validate the normalized six-category HuffPost sample."""

    def __init__(self, expected_categories: Iterable[str] | None = None) -> None:
        self.expected_categories = set(expected_categories or NewsBot2Config().classification_categories)

    def validate(self, dataframe: pd.DataFrame) -> ValidationReport:
        df = normalize_news_columns(dataframe)
        missing = {column: int(df[column].isna().sum()) for column in REQUIRED_COLUMNS}
        category_counts = df["category"].fillna("<missing>").value_counts().sort_index().to_dict()
        unexpected = sorted(set(category_counts) - self.expected_categories)
        missing_categories = sorted(self.expected_categories - set(category_counts))
        warnings: list[str] = []
        if unexpected:
            warnings.append(f"Unexpected categories: {', '.join(unexpected)}")
        if missing_categories:
            warnings.append(f"Missing expected categories: {', '.join(missing_categories)}")
        if df["date"].isna().any():
            warnings.append("Some dates could not be parsed.")
        if df["full_text"].str.strip().eq("").any():
            warnings.append("Some articles have empty normalized full_text.")
        valid = not unexpected and not missing_categories and not df.empty
        return ValidationReport(
            valid=valid,
            row_count=int(len(df)),
            columns=list(df.columns),
            categories={str(key): int(value) for key, value in category_counts.items()},
            missing_by_column=missing,
            duplicate_rows=int(df.duplicated(subset=["full_text", "category"]).sum()),
            invalid_dates=int(df["date"].isna().sum()),
            date_min=df["date"].min().date().isoformat() if df["date"].notna().any() else None,
            date_max=df["date"].max().date().isoformat() if df["date"].notna().any() else None,
            warnings=warnings,
        )
