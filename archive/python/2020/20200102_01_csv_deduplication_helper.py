"""Archive task: Csv Deduplication Helper.

Generated for 2020-01-02. The implementation is intentionally compact so each
commit can stand alone as a small learning artefact.
"""

from statistics import mean


def rolling_average(values, window):
    if window <= 0:
        raise ValueError("window must be positive")
    return [mean(values[index:index + window]) for index in range(len(values) - window + 1)]


if __name__ == "__main__":
    sample = [3, 5, 8, 13, 21, 34]
    print(rolling_average(sample, 3))
