"""Archive task: Csv Deduplication Helper.

Generated for 2021-08-11. The implementation is intentionally compact so each
commit can stand alone as a small learning artefact.
"""

from collections.abc import Iterable


def deduplicate_records(records: Iterable[dict], keys: tuple[str, ...]) -> list[dict]:
    seen = set()
    unique = []
    for record in records:
        signature = tuple(record.get(key) for key in keys)
        if signature in seen:
            continue
        seen.add(signature)
        unique.append(record)
    return unique
