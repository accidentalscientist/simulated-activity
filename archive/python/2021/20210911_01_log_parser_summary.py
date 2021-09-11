"""Archive task: Log Parser Summary.

Generated for 2021-09-11. The implementation is intentionally compact so each
commit can stand alone as a small learning artefact.
"""

from collections import Counter


def summarise_status_codes(lines: list[str]) -> dict[str, int]:
    counts = Counter()
    for line in lines:
        parts = line.split()
        if len(parts) >= 2:
            counts[parts[-1]] += 1
    return dict(counts)
