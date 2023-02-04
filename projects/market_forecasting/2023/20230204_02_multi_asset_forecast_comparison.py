"""Archive task: Multi-Asset Forecast Comparison.

Generated for 2023-02-04. This synthetic market research code is educational
only and is not financial advice.
"""

def compare_forecasts(actual, baselines: dict[str, list[float]]) -> dict[str, float]:
    scores = {}
    for name, prediction in baselines.items():
        error = sum(abs(a - p) for a, p in zip(actual, prediction)) / len(actual)
        scores[name] = error
    return dict(sorted(scores.items(), key=lambda item: item[1]))
