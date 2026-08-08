import json

import numpy as np
import pandas as pd

from src.utils.export import serialize_json


def test_serialize_json_handles_analysis_runtime_types():
    payload = {
        "date": pd.Timestamp("2025-12-10"),
        "score": np.float64(0.75),
        "topics": np.array([1, 2]),
    }

    restored = json.loads(serialize_json(payload))

    assert restored == {
        "date": "2025-12-10T00:00:00",
        "score": 0.75,
        "topics": [1, 2],
    }
