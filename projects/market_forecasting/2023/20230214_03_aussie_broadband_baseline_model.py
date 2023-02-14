"""Archive task: Aussie Broadband Baseline Model.

Generated for 2023-02-14. This synthetic market research code is educational
only and is not financial advice.
"""

def fit_baseline_forecast(history: list[float], horizon: int = 5) -> list[float]:
    slope = (history[-1] - history[0]) / max(len(history) - 1, 1)
    return [history[-1] + slope * step for step in range(1, horizon + 1)]
