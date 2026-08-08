from src.data_processing.data_validator import DatasetValidator, load_news_dataset, normalize_news_columns
from src.data_processing.text_preprocessor import TextPreprocessor


def test_empty_text_is_safe() -> None:
    assert TextPreprocessor().preprocess(None) == ""
    assert TextPreprocessor().preprocess("") == ""


def test_normal_text_and_punctuation_are_normalized() -> None:
    result = TextPreprocessor().preprocess("Breaking: Markets rise, quickly!")
    # The refactored midterm pipeline lemmatizes plural nouns.
    assert result == "breaking market rise quickly"


def test_url_is_removed_and_unicode_is_retained() -> None:
    result = TextPreprocessor().preprocess("Café news: https://example.com/économie")
    assert "https" not in result
    assert "café" in result


def test_midterm_aliases_normalize_and_validation_reports_dates(tiny_news_dataframe) -> None:
    normalized = normalize_news_columns(tiny_news_dataframe)
    report = DatasetValidator().validate(normalized)
    assert {"headline", "short_description", "full_text"}.issubset(normalized.columns)
    assert normalized.loc[0, "full_text"] == "Technology update. New AI tools launch."
    assert report.invalid_dates == 1
    assert report.row_count == 3


def test_copied_midterm_dataset_loads_with_six_categories() -> None:
    dataframe = load_news_dataset()
    report = DatasetValidator().validate(dataframe)
    assert report.valid is True
    assert report.row_count == 1800
    assert set(report.categories) == {"POLITICS", "ENTERTAINMENT", "BUSINESS", "SPORTS", "TECH", "WELLNESS"}
    assert dataframe["date"].notna().all()
