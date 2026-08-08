from __future__ import annotations

import pandas as pd
import pytest


@pytest.fixture
def tiny_news_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "title": ["Technology update", "Election update", "Health update"],
            "content": ["New AI tools launch.", "Voters discuss policy.", "Doctors share wellness advice."],
            "category": ["TECH", "POLITICS", "WELLNESS"],
            "authors": ["A", "B", "C"],
            "date": ["2022-09-01", "2022-09-02", "not-a-date"],
        }
    )
