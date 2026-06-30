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


def parse_date(value: str) -> date:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Expected YYYY-MM-DD, got {value!r}") from exc
    if parsed < START_DATE or parsed > END_DATE:
        raise argparse.ArgumentTypeError(
            f"Date must be between {START_DATE.isoformat()} and {END_DATE.isoformat()}"
        )
    return parsed


def filter_entries(entries: list[PlanEntry], start_date: date, end_date: date) -> list[PlanEntry]:
    if start_date > end_date:
        raise SystemExit("--start-date cannot be later than --end-date")
    return [
        entry
        for entry in entries
        if start_date <= date.fromisoformat(entry.date) <= end_date
    ]


def summarize(entries: list[PlanEntry], start_date: date, end_date: date) -> dict[str, object]:
    active_dates = {entry.date for entry in entries}
    total_days = sum(1 for _ in iter_days(start_date, end_date))
    by_year: dict[str, int] = {}
    by_track: dict[str, int] = {}
    monthly_zero_days: dict[str, int] = {}

    for entry in entries:
        by_year[entry.date[:4]] = by_year.get(entry.date[:4], 0) + 1
        by_track[entry.track] = by_track.get(entry.track, 0) + 1

    for year in range(start_date.year, end_date.year + 1):
        for month in range(1, 13):
            label = f"{year}-{month:02d}"
            days = [day for day in month_days(year, month) if start_date <= day <= end_date]
            if not days:
                continue
            monthly_zero_days[label] = sum(1 for day in days if day.isoformat() not in active_dates)

    return {
        "range": f"{start_date.isoformat()} to {end_date.isoformat()}",
        "total_days": total_days,
        "active_days": len(active_dates),
        "zero_commit_days": total_days - len(active_dates),
        "planned_commits": len(entries),
        "commits_by_year": dict(sorted(by_year.items())),
        "commits_by_track": dict(sorted(by_track.items())),
        "monthly_zero_days_min": min(monthly_zero_days.values()) if monthly_zero_days else 0,
        "monthly_zero_days_max": max(monthly_zero_days.values()) if monthly_zero_days else 0,
    }


def content_for(entry: PlanEntry) -> str:
    title = entry.task_title.title()
    if entry.track == "market_forecasting" and entry.content_type == "report":
        return market_report_content(entry, title)
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
    if entry.track == "market_forecasting":
        return market_python_content(entry, title)
    if entry.task_title == "csv deduplication helper":
        body = '''from collections.abc import Iterable


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
'''
    elif entry.task_title == "log parser summary":
        body = '''from collections import Counter


def summarise_status_codes(lines: list[str]) -> dict[str, int]:
    counts = Counter()
    for line in lines:
        parts = line.split()
        if len(parts) >= 2:
            counts[parts[-1]] += 1
    return dict(counts)
'''
    elif entry.task_title == "feature scaling utility":
        body = '''def min_max_scale(values: list[float]) -> list[float]:
    if not values:
        return []
    low, high = min(values), max(values)
    if high == low:
        return [0.0 for _ in values]
    return [(value - low) / (high - low) for value in values]
'''
    elif entry.task_title == "unit tests for edge cases":
        body = '''import unittest


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


class EdgeCaseTests(unittest.TestCase):
    def test_clamps_below_range(self):
        self.assertEqual(clamp(-4, 0, 10), 0)

    def test_clamps_above_range(self):
        self.assertEqual(clamp(18, 0, 10), 10)


if __name__ == "__main__":
    unittest.main()
'''
    else:
        body = '''from statistics import median


def rolling_median(values: list[float], window: int) -> list[float]:
    if window <= 0:
        raise ValueError("window must be positive")
    return [median(values[index:index + window]) for index in range(len(values) - window + 1)]
'''
    return f'''"""Archive task: {title}.

Generated for {entry.date}. The implementation is intentionally compact so each
commit can stand alone as a small learning artefact.
"""

{body}'''


def market_python_content(entry: PlanEntry, title: str) -> str:
    if "Evera Lithium" in entry.task_title:
        body = '''def build_lithium_factor_set(prices, volumes, benchmark):
    return {
        "momentum_20": prices[-1] / prices[-20] - 1,
        "volume_ratio": volumes[-5] / max(sum(volumes[-20:]) / 20, 1),
        "benchmark_spread": prices[-1] / benchmark[-1] - 1,
    }
'''
    elif "Aussie Broadband" in entry.task_title:
        body = '''def fit_baseline_forecast(history: list[float], horizon: int = 5) -> list[float]:
    slope = (history[-1] - history[0]) / max(len(history) - 1, 1)
    return [history[-1] + slope * step for step in range(1, horizon + 1)]
'''
    elif "Origin Energy" in entry.task_title:
        body = '''def rolling_volatility(values: list[float], window: int = 20) -> list[float]:
    returns = [(values[i] / values[i - 1]) - 1 for i in range(1, len(values))]
    output = []
    for index in range(len(returns) - window + 1):
        sample = returns[index:index + window]
        mean = sum(sample) / window
        output.append((sum((value - mean) ** 2 for value in sample) / window) ** 0.5)
    return output
'''
    else:
        body = '''def compare_forecasts(actual, baselines: dict[str, list[float]]) -> dict[str, float]:
    scores = {}
    for name, prediction in baselines.items():
        error = sum(abs(a - p) for a, p in zip(actual, prediction)) / len(actual)
        scores[name] = error
    return dict(sorted(scores.items(), key=lambda item: item[1]))
'''
    return f'''"""Archive task: {title}.

Generated for {entry.date}. This synthetic market research code is educational
only and is not financial advice.
"""

{body}'''


def market_report_content(entry: PlanEntry, title: str) -> str:
    return f"""# {title}

Generated for {entry.date}.

This note records assumptions for a synthetic market-forecasting exercise. It
does not provide financial advice and should not be used for investment
decisions.

## Assumptions

- Inputs are treated as historical observations, not live prices.
- Forecasts are compared against simple momentum and mean-reversion baselines.
- Model quality is judged with backtesting error rather than narrative appeal.
- Evera Lithium, Aussie Broadband, and Origin Energy are handled as separate
  series before any cross-asset comparison.
"""


def sql_content(entry: PlanEntry, title: str) -> str:
    if entry.content_type == "schema":
        return f"""-- Archive task: {title}
-- Generated for {entry.date}

CREATE TABLE experiment_metrics (
    experiment_id TEXT NOT NULL,
    variant TEXT NOT NULL,
    metric_date DATE NOT NULL,
    visitors INTEGER NOT NULL,
    conversions INTEGER NOT NULL,
    revenue NUMERIC(12, 2),
    PRIMARY KEY (experiment_id, variant, metric_date)
);
"""
    if entry.task_title == "monthly revenue rollup":
        query = """SELECT
    DATE_TRUNC('month', invoice_date) AS revenue_month,
    SUM(amount) AS gross_revenue,
    COUNT(DISTINCT customer_id) AS paying_customers
FROM invoices
GROUP BY DATE_TRUNC('month', invoice_date)
ORDER BY revenue_month;"""
    elif entry.task_title == "customer cohort retention":
        query = """WITH first_seen AS (
    SELECT customer_id, MIN(DATE_TRUNC('month', event_date)) AS cohort_month
    FROM product_events
    GROUP BY customer_id
),
activity AS (
    SELECT customer_id, DATE_TRUNC('month', event_date) AS activity_month
    FROM product_events
    GROUP BY customer_id, DATE_TRUNC('month', event_date)
)
SELECT
    first_seen.cohort_month,
    activity.activity_month,
    COUNT(*) AS retained_customers
FROM first_seen
JOIN activity USING (customer_id)
GROUP BY first_seen.cohort_month, activity.activity_month;"""
    elif entry.task_title == "windowed churn analysis":
        query = """SELECT
    customer_id,
    activity_month,
    active_days,
    LAG(active_days) OVER (
        PARTITION BY customer_id
        ORDER BY activity_month
    ) AS previous_active_days
FROM monthly_customer_activity
WHERE active_days = 0;"""
    else:
        query = """WITH ranked_orders AS (
    SELECT
        customer_id,
        order_id,
        order_total,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY order_total DESC
        ) AS order_rank
    FROM orders
)
SELECT customer_id, order_id, order_total
FROM ranked_orders
WHERE order_rank <= 3;"""
    return f"""-- Archive task: {title}
-- Generated for {entry.date}

{query}
"""


def rust_content(entry: PlanEntry, title: str) -> str:
    if entry.task_title == "fast line counter":
        body = '''pub fn count_lines(input: &str) -> usize {
    input.lines().count()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn counts_lines() {
        assert_eq!(count_lines("a\\nb\\nc"), 3);
    }
}
'''
    elif entry.task_title == "graph traversal":
        body = '''use std::collections::{HashMap, HashSet, VecDeque};

pub fn reachable(graph: &HashMap<&str, Vec<&str>>, start: &str) -> HashSet<String> {
    let mut seen = HashSet::new();
    let mut queue = VecDeque::from([start]);
    while let Some(node) = queue.pop_front() {
        if seen.insert(node.to_string()) {
            if let Some(neighbours) = graph.get(node) {
                queue.extend(neighbours.iter().copied());
            }
        }
    }
    seen
}
'''
    elif entry.task_title == "config parser":
        body = '''pub fn parse_pairs(input: &str) -> Vec<(&str, &str)> {
    input
        .lines()
        .filter_map(|line| line.split_once('='))
        .map(|(key, value)| (key.trim(), value.trim()))
        .collect()
}
'''
    else:
        body = '''use std::collections::VecDeque;

pub struct BoundedQueue<T> {
    limit: usize,
    values: VecDeque<T>,
}

impl<T> BoundedQueue<T> {
    pub fn new(limit: usize) -> Self {
        Self { limit, values: VecDeque::new() }
    }

    pub fn push(&mut self, value: T) {
        if self.values.len() == self.limit {
            self.values.pop_front();
        }
        self.values.push_back(value);
    }
}
'''
    return f"""// Archive task: {title}
// Generated for {entry.date}

{body}"""


def typescript_content(entry: PlanEntry, title: str) -> str:
    if entry.task_title == "request validator":
        body = '''type RequestBody = { email?: string; amount?: number };

export function validateRequest(body: RequestBody): string[] {
  const errors: string[] = [];
  if (!body.email?.includes("@")) errors.push("email is invalid");
  if (body.amount === undefined || body.amount <= 0) errors.push("amount must be positive");
  return errors;
}
'''
    elif entry.task_title == "typed api client":
        body = '''type ApiResponse<T> = { data: T; status: number };

export async function getJson<T>(url: string): Promise<ApiResponse<T>> {
  const response = await fetch(url);
  return { data: await response.json() as T, status: response.status };
}
'''
    elif entry.task_title == "date range guard":
        body = '''export function isWithinRange(value: Date, start: Date, end: Date): boolean {
  return value.getTime() >= start.getTime() && value.getTime() <= end.getTime();
}
'''
    else:
        body = '''type EventPayload = {
  id: string;
  createdAt: string;
  value: number;
};

export function normalisePayload(payload: EventPayload): EventPayload {
  return {
    id: payload.id.trim().toLowerCase(),
    createdAt: new Date(payload.createdAt).toISOString(),
    value: Number.isFinite(payload.value) ? payload.value : 0,
  };
}
'''
    return f"""// Archive task: {title}
// Generated for {entry.date}

{body}"""


def go_content(entry: PlanEntry, title: str) -> str:
    if entry.task_title == "worker pool":
        body = '''func RunJobs(jobs []func() int) []int {
	results := make([]int, 0, len(jobs))
	for _, job := range jobs {
		results = append(results, job())
	}
	return results
}
'''
    elif entry.task_title == "json stream parser":
        body = '''import "encoding/json"

func DecodeObjects(data []byte, target any) error {
	return json.Unmarshal(data, target)
}
'''
    elif entry.task_title == "health check service":
        body = '''type HealthCheck struct {
	Name string
	OK   bool
}

func OverallStatus(checks []HealthCheck) bool {
	for _, check := range checks {
		if !check.OK {
			return false
		}
	}
	return true
}
'''
    else:
        body = '''func SumByKey(rows []map[string]int, key string) int {
	total := 0
	for _, row := range rows {
		total += row[key]
	}
	return total
}
'''
    return f"""// Archive task: {title}
// Generated for {entry.date}

package archive

{body}"""


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
    parser.add_argument("--start-date", type=parse_date, default=START_DATE)
    parser.add_argument("--end-date", type=parse_date, default=END_DATE)
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
    entries = filter_entries(plan_entries(args.seed), args.start_date, args.end_date)
    write_manifest(entries, args.manifest)

    if args.summary:
        print(json.dumps(summarize(entries, args.start_date, args.end_date), indent=2))

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
