"""Archive task: Feature Scaling Utility.

Generated for 2022-04-07. The implementation is intentionally compact so each
commit can stand alone as a small learning artefact.
"""

def min_max_scale(values: list[float]) -> list[float]:
    if not values:
        return []
    low, high = min(values), max(values)
    if high == low:
        return [0.0 for _ in values]
    return [(value - low) / (high - low) for value in values]
