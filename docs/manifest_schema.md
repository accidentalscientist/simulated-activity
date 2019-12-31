# Manifest Schema

The generator writes a CSV manifest before creating files or commits. This lets the archive be reviewed before any Git history is written.

## Columns

| Column | Description |
| --- | --- |
| `date` | Calendar date for the planned work item. |
| `timestamp` | Local timestamp to use for the commit. |
| `day_commit_count` | Total commits planned for that day. |
| `sequence` | Commit sequence number within the day. |
| `track` | High-level work stream, such as `python`, `sql`, `market_forecasting`, or `notebook`. |
| `language` | Primary language or artefact type. |
| `content_type` | Template family used to create the file. |
| `path` | Planned repository path for the generated content. |
| `message` | Planned commit message. |
| `task_title` | Human-readable task title. |

## Planning Rules

- Range: 2020-01-01 through 2025-12-31.
- Each month receives 1 or 2 zero-commit days.
- Active days receive 1 to 6 commits.
- Commit counts are weighted toward 3 and 4.
- The generator uses a fixed seed by default so a manifest can be reproduced.

## Review Checklist

Before execution, check:

- total commit count by year
- zero-commit days per month
- language and project mix
- repeated file paths
- commit messages for tone and variety
- disclosure language in the README

## Pilot Windows

Use `--start-date` and `--end-date` to generate a smaller review window before writing the full archive. The full plan is generated first and then filtered, which keeps the pilot consistent with the larger 2020-2025 sequence.
