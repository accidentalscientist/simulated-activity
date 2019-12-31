# Applied Code Archive

This repository contains a generated long-range archive of small programming tasks, data notes, algorithm exercises, and analytical project artefacts. The archive is designed to make a commit history readable as a technical story rather than as a pile of disconnected files.

## What Is In The Archive

The planned archive spans several streams:

- Python problem solving, data cleaning, and modelling utilities
- SQL analysis, schemas, CTEs, and reporting queries
- Rust algorithm and command-line exercises
- TypeScript validation, API, and transformation helpers
- Go parsers, services, and concurrency examples
- Long-running notebooks and market-style modelling experiments

The larger project arcs include a market forecasting study for Evera Lithium, Aussie Broadband, and Origin Energy, plus a long-range notebook with synthetic data analysis, visual summaries, and modelling notes.

## Archive Note

This repository is intentionally generated. Commit dates, file paths, and task content are produced by a planning tool so the project can explore how activity graphs, code archives, and technical narratives are interpreted. The material is not presented as organic historical work. The point is to reward careful reading over surface-level interpretation.

The forecasting material is educational and synthetic. It is not financial advice, and it should not be used to make investment decisions.

## How It Works

The generator creates a manifest first. The manifest describes what would be committed before any Git history is written.

Each manifest row contains:

- date
- timestamp
- commit count for that day
- language or project track
- file path
- commit message
- content type
- task title

Current planning rules:

- date range: 2020-01-01 to 2025-12-31 inclusive
- each month has 1 or 2 zero-commit days
- every other day has 1 to 6 commits
- most active days have 3 or 4 commits
- timestamps are spread through normal working and evening hours

## Dry Run

Generate a manifest without touching Git:

```bash
python tools/planned_activity_generator.py --dry-run --manifest manifests/activity_manifest_2020_2025.csv
```

Print summary statistics:

```bash
python tools/planned_activity_generator.py --dry-run --summary
```

Generate a one-month pilot manifest:

```bash
python tools/planned_activity_generator.py --dry-run --summary --start-date 2020-01-01 --end-date 2020-01-31 --manifest manifests/pilot_january_2020.csv
```

## Execution

The tool is deliberately cautious. Writing files and commits is separate from planning. Review the manifest before running anything that writes history.

```bash
python tools/planned_activity_generator.py --dry-run --manifest manifests/activity_manifest_2020_2025.csv
```

The execution mode should be run only on a disposable branch after reviewing the manifest.

The full 2020-2025 archive plan currently contains:

- 7,291 planned commits
- 2,082 active days
- 110 zero-commit days
- 1 or 2 zero-commit days in every month
- a code mix across Python, SQL, Rust, TypeScript, Go, notebooks, and synthetic market-forecasting artefacts

The recommended full-run branch is:

```text
codex/full-archive-2020-2025
```

For a pilot branch:

```bash
python tools/planned_activity_generator.py --execute --i-understand-this-writes-git-history --start-date 2020-01-01 --end-date 2020-01-31 --manifest manifests/pilot_january_2020.csv
```

For the full archive branch:

```bash
python tools/planned_activity_generator.py --execute --i-understand-this-writes-git-history --manifest manifests/activity_manifest_2020_2025.csv
```
