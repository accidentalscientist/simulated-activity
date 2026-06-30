from __future__ import annotations

import argparse
import calendar
import csv
import json
import os
import random
import subprocess
from dataclasses import asdict, dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Iterable


START_DATE = date(2020, 1, 1)
END_DATE = date(2025, 12, 31)
DEFAULT_SEED = 20200101

COMMIT_COUNT_WEIGHTS = {
    1: 0.05,
    2: 0.15,
    3: 0.30,
    4: 0.30,
    5: 0.15,
    6: 0.05,
}

FIELDNAMES = [
    "date",
    "timestamp",
    "day_commit_count",
    "sequence",
    "track",
    "language",
    "content_type",
    "path",
    "message",
    "task_title",
]


@dataclass(frozen=True)
class PlanEntry:
    date: str
    timestamp: str
    day_commit_count: int
    sequence: int
    track: str
    language: str
    content_type: str
    path: str
    message: str
    task_title: str


TASKS = {
    "python": [
        ("rolling median window", "algorithm", "solve rolling median window in python"),
        ("csv deduplication helper", "data_cleaning", "add csv deduplication helper"),
        ("log parser summary", "parsing", "summarise service logs with python"),
        ("feature scaling utility", "ml_utility", "add feature scaling utility"),
        ("unit tests for edge cases", "test", "cover python edge cases"),
    ],
    "sql": [
        ("customer cohort retention", "query", "write customer cohort retention query"),
        ("monthly revenue rollup", "query", "add monthly revenue rollup query"),
        ("windowed churn analysis", "query", "model churn with sql windows"),
        ("schema for experiment metrics", "schema", "define experiment metrics schema"),
        ("slow query refactor", "query", "refactor reporting query with ctes"),
    ],
    "rust": [
        ("bounded queue", "algorithm", "implement bounded queue in rust"),
        ("fast line counter", "cli", "add rust line counting utility"),
        ("graph traversal", "algorithm", "solve graph traversal in rust"),
        ("config parser", "parser", "parse config blocks in rust"),
    ],
    "typescript": [
        ("request validator", "validation", "add request validator in typescript"),
        ("typed api client", "api_client", "build typed api client"),
        ("normalise payload helper", "transform", "normalise event payloads"),
        ("date range guard", "validation", "add date range guard"),
    ],
    "go": [
        ("worker pool", "concurrency", "implement worker pool in go"),
        ("json stream parser", "parser", "add json stream parser"),
        ("health check service", "service", "add health check service"),
        ("csv aggregation command", "cli", "aggregate csv metrics in go"),
    ],
    "market_forecasting": [
        ("Evera Lithium factor set", "feature_engineering", "add evera lithium factor set"),
        ("Aussie Broadband baseline model", "model", "fit aussie broadband baseline model"),
        ("Origin Energy volatility study", "analysis", "analyse origin energy volatility"),
        ("multi-asset forecast comparison", "evaluation", "compare forecast baselines"),
        ("forecast assumptions note", "report", "document forecasting assumptions"),
    ],
    "notebook": [
        ("long-range synthetic data notebook", "notebook", "extend long-range analysis notebook"),
        ("rolling trend visualisation", "notebook", "add rolling trend visualisation"),
        ("model comparison charts", "notebook", "chart model comparison results"),
        ("seasonality decomposition", "notebook", "add seasonality decomposition section"),
    ],
}


def iter_days(start: date, end: date) -> Iterable[date]:
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def month_days(year: int, month: int) -> list[date]:
    _, days_in_month = calendar.monthrange(year, month)
    return [date(year, month, day) for day in range(1, days_in_month + 1)]


def weighted_choice(weights: dict[int, float], rng: random.Random) -> int:
    values = list(weights.keys())
    probabilities = list(weights.values())
    return rng.choices(values, weights=probabilities, k=1)[0]


def choose_track(day: date, rng: random.Random) -> str:
    if day.year <= 2021:
        weights = {
            "python": 30,
            "sql": 22,
            "typescript": 18,
            "go": 12,
            "rust": 12,
            "notebook": 6,
        }
    elif day.year == 2022:
        weights = {
            "python": 28,
            "sql": 24,
            "typescript": 14,
            "go": 12,
            "rust": 10,
            "notebook": 8,
            "market_forecasting": 4,
        }
    elif day.year in (2023, 2024):
        weights = {
            "python": 24,
            "sql": 18,
            "typescript": 12,
            "go": 10,
            "rust": 8,
            "notebook": 13,
            "market_forecasting": 15,
        }
    else:
        weights = {
            "python": 18,
            "sql": 14,
            "typescript": 10,
            "go": 8,
            "rust": 8,
            "notebook": 20,
            "market_forecasting": 22,
        }
    return rng.choices(list(weights.keys()), weights=list(weights.values()), k=1)[0]


def timestamp_for(day: date, sequence: int, total: int, rng: random.Random) -> datetime:
    start_seconds = 8 * 3600 + 30 * 60
    end_seconds = 22 * 3600 + 15 * 60
    span = end_seconds - start_seconds
    base = start_seconds + int(span * sequence / (total + 1))
    jitter = rng.randint(-28 * 60, 28 * 60)
    seconds = max(start_seconds, min(end_seconds, base + jitter))
    return datetime.combine(day, time.min) + timedelta(seconds=seconds)


def path_for(day: date, track: str, content_type: str, task_title: str, sequence: int) -> str:
    slug = task_title.lower().replace(" ", "_").replace("-", "_")
    stamp = f"{day:%Y%m%d}_{sequence:02d}"
    if track == "python":
        return f"archive/python/{day.year}/{stamp}_{slug}.py"
    if track == "sql":
        return f"archive/sql/{day.year}/{stamp}_{slug}.sql"
    if track == "rust":
        return f"archive/rust/{day.year}/{stamp}_{slug}.rs"
    if track == "typescript":
        return f"archive/typescript/{day.year}/{stamp}_{slug}.ts"
    if track == "go":
        return f"archive/go/{day.year}/{stamp}_{slug}.go"
    if track == "market_forecasting":
        ext = "md" if content_type == "report" else "py"
        return f"projects/market_forecasting/{day.year}/{stamp}_{slug}.{ext}"
    return f"projects/long_range_analysis/notebooks/{day.year}/{stamp}_{slug}.ipynb"


def plan_entries(seed: int = DEFAULT_SEED) -> list[PlanEntry]:
    rng = random.Random(seed)
    off_days: set[date] = set()

    for year in range(START_DATE.year, END_DATE.year + 1):
        for month in range(1, 13):
            days = month_days(year, month)
            if year == START_DATE.year and month == START_DATE.month:
                days = [day for day in days if day >= START_DATE]
            if year == END_DATE.year and month == END_DATE.month:
                days = [day for day in days if day <= END_DATE]
            off_count = rng.choice([1, 2])
            off_days.update(rng.sample(days, off_count))

    entries: list[PlanEntry] = []
    for day in iter_days(START_DATE, END_DATE):
        if day in off_days:
            continue

        commit_count = weighted_choice(COMMIT_COUNT_WEIGHTS, rng)
        for sequence in range(1, commit_count + 1):
            track = choose_track(day, rng)
            task_title, content_type, message = rng.choice(TASKS[track])
            ts = timestamp_for(day, sequence, commit_count, rng)
            path = path_for(day, track, content_type, task_title, sequence)
            language = language_for(track)
            entries.append(
                PlanEntry(
                    date=day.isoformat(),
                    timestamp=ts.isoformat(timespec="seconds"),
                    day_commit_count=commit_count,
                    sequence=sequence,
                    track=track,
                    language=language,
                    content_type=content_type,
                    path=path,
                    message=message,
                    task_title=task_title,
                )
            )
    return entries


def language_for(track: str) -> str:
    return {
        "python": "python",
        "sql": "sql",
        "rust": "rust",
        "typescript": "typescript",
        "go": "go",
        "market_forecasting": "python",
        "notebook": "jupyter",
    }[track]


def write_manifest(entries: list[PlanEntry], manifest_path: Path) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for entry in entries:
            writer.writerow(asdict(entry))


def summarize(entries: list[PlanEntry]) -> dict[str, object]:
    active_dates = {entry.date for entry in entries}
    total_days = sum(1 for _ in iter_days(START_DATE, END_DATE))
    by_year: dict[str, int] = {}
    by_track: dict[str, int] = {}
    monthly_zero_days: dict[str, int] = {}

    for entry in entries:
        by_year[entry.date[:4]] = by_year.get(entry.date[:4], 0) + 1
        by_track[entry.track] = by_track.get(entry.track, 0) + 1

    for year in range(START_DATE.year, END_DATE.year + 1):
        for month in range(1, 13):
            label = f"{year}-{month:02d}"
            days = [day for day in month_days(year, month) if START_DATE <= day <= END_DATE]
            monthly_zero_days[label] = sum(1 for day in days if day.isoformat() not in active_dates)

    return {
        "range": f"{START_DATE.isoformat()} to {END_DATE.isoformat()}",
        "total_days": total_days,
        "active_days": len(active_dates),
        "zero_commit_days": total_days - len(active_dates),
        "planned_commits": len(entries),
        "commits_by_year": dict(sorted(by_year.items())),
        "commits_by_track": dict(sorted(by_track.items())),
        "monthly_zero_days_min": min(monthly_zero_days.values()),
        "monthly_zero_days_max": max(monthly_zero_days.values()),
    }


def content_for(entry: PlanEntry) -> str:
    title = entry.task_title.title()
    if entry.language == "python":
        return python_content(entry, title)
    if entry.language == "sql":
        return sql_content(entry, title)
    if entry.language == "rust":
        return rust_content(entry, title)
    if entry.language == "typescript":
        return typescript_content(entry, title)
    if entry.language == "go":
        return go_content(entry, title)
    return notebook_content(entry, title)


def python_content(entry: PlanEntry, title: str) -> str:
    return f'''"""Archive task: {title}.

Generated for {entry.date}. The implementation is intentionally compact so each
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
'''


def sql_content(entry: PlanEntry, title: str) -> str:
    return f"""-- Archive task: {title}
-- Generated for {entry.date}

WITH monthly_activity AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', event_date) AS activity_month,
        COUNT(*) AS event_count
    FROM product_events
    GROUP BY customer_id, DATE_TRUNC('month', event_date)
),
ranked_activity AS (
    SELECT
        customer_id,
        activity_month,
        event_count,
        LAG(event_count) OVER (
            PARTITION BY customer_id
            ORDER BY activity_month
        ) AS previous_event_count
    FROM monthly_activity
)
SELECT *
FROM ranked_activity
WHERE event_count >= COALESCE(previous_event_count, 0);
"""


def rust_content(entry: PlanEntry, title: str) -> str:
    return f"""// Archive task: {title}
// Generated for {entry.date}

pub fn bounded_sum(values: &[i64], limit: i64) -> i64 {{
    values
        .iter()
        .copied()
        .filter(|value| *value <= limit)
        .sum()
}}

#[cfg(test)]
mod tests {{
    use super::*;

    #[test]
    fn sums_values_under_limit() {{
        assert_eq!(bounded_sum(&[2, 5, 8, 13], 8), 15);
    }}
}}
"""


def typescript_content(entry: PlanEntry, title: str) -> str:
    return f"""// Archive task: {title}
// Generated for {entry.date}

type EventPayload = {{
  id: string;
  createdAt: string;
  value: number;
}};

export function normalisePayload(payload: EventPayload): EventPayload {{
  return {{
    id: payload.id.trim().toLowerCase(),
    createdAt: new Date(payload.createdAt).toISOString(),
    value: Number.isFinite(payload.value) ? payload.value : 0,
  }};
}}
"""


def go_content(entry: PlanEntry, title: str) -> str:
    return f"""// Archive task: {title}
// Generated for {entry.date}

package archive

func SumByKey(rows []map[string]int, key string) int {{
	total := 0
	for _, row := range rows {{
		total += row[key]
	}}
	return total
}}
"""


def notebook_content(entry: PlanEntry, title: str) -> str:
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"# {title}\\n",
                    f"Generated archive notebook section for {entry.date}.\\n",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import math\\n",
                    "series = [math.sin(i / 6) + i * 0.01 for i in range(120)]\\n",
                    "rolling = [sum(series[i:i+12]) / 12 for i in range(len(series) - 11)]\\n",
                    "rolling[:5]\\n",
                ],
            },
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.x"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    return json.dumps(notebook, indent=2)


def write_content(entry: PlanEntry, repo_root: Path) -> Path:
    path = repo_root / entry.path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content_for(entry), encoding="utf-8")
    return path


def commit_entry(entry: PlanEntry, repo_root: Path) -> None:
    path = write_content(entry, repo_root)
    env = {
        **os.environ,
        "GIT_AUTHOR_DATE": entry.timestamp,
        "GIT_COMMITTER_DATE": entry.timestamp,
    }
    subprocess.run(["git", "add", str(path.relative_to(repo_root))], cwd=repo_root, check=True)
    subprocess.run(["git", "commit", "-m", entry.message], cwd=repo_root, env=env, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan a generated long-range code archive.")
    parser.add_argument("--manifest", type=Path, default=Path("manifests/activity_manifest_2020_2025.csv"))
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--dry-run", action="store_true", help="Write or inspect a manifest without touching Git.")
    parser.add_argument("--summary", action="store_true", help="Print summary statistics.")
    parser.add_argument("--write-files", action="store_true", help="Write files from the plan without committing.")
    parser.add_argument("--execute", action="store_true", help="Create files and backdated commits from the plan.")
    parser.add_argument(
        "--i-understand-this-writes-git-history",
        action="store_true",
        help="Required with --execute.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    entries = plan_entries(args.seed)
    write_manifest(entries, args.manifest)

    if args.summary:
        print(json.dumps(summarize(entries), indent=2))

    if args.write_files:
        repo_root = Path.cwd()
        for entry in entries:
            write_content(entry, repo_root)

    if args.execute:
        if not args.i_understand_this_writes_git_history:
            raise SystemExit("--execute requires --i-understand-this-writes-git-history")
        repo_root = Path.cwd()
        for entry in entries:
            commit_entry(entry, repo_root)

    if args.dry_run and not args.summary:
        print(f"Wrote dry-run manifest with {len(entries)} planned commits to {args.manifest}")


if __name__ == "__main__":
    main()
