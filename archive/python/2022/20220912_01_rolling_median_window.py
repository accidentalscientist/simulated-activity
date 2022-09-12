"""Archive task: Rolling Median Window.

Generated for 2022-09-12. The implementation is intentionally compact so each
commit can stand alone as a small learning artefact.
"""

from statistics import median


def rolling_median(values: list[float], window: int) -> list[float]:
    if window <= 0:
        raise ValueError("window must be positive")
    return [median(values[index:index + window]) for index in range(len(values) - window + 1)]
