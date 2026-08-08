"""Safe, JSON-serializable result export helpers."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


class _Encoder(json.JSONEncoder):
    def default(self, value):  # noqa: D401
        if isinstance(value, (np.integer, np.floating)): return value.item()
        if isinstance(value, np.ndarray): return value.tolist()
        if isinstance(value, (pd.Timestamp,)): return value.isoformat()
        return super().default(value)


def serialize_json(data: dict | list) -> str:
    """Serialize analysis output, including pandas and NumPy values."""
    return json.dumps(data, indent=2, cls=_Encoder)


def export_json(data: dict | list, path: str | Path) -> Path:
    target = Path(path); target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(serialize_json(data), encoding="utf-8")
    return target


def export_table(data: pd.DataFrame, path: str | Path) -> Path:
    target = Path(path); target.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(target, index=False)
    return target
