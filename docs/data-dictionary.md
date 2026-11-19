# Data dictionary

## `runs.csv`

One row per validation run, 17 rows total.

| Column | Meaning |
|---|---|
| `source_dir` | validation batch identifier |
| `run` | run number inside the batch |
| `default_score` | objective value of the best Default schedule used as the GA seed |
| `genetic_score` | objective value of the best GA result |
| `delta` | `genetic_score - default_score` |
| `percent` | improvement over the Default seed, `delta / default_score * 100` |
| `duration_seconds` | recorded run duration |
| `exit_code` | process exit code; `0` means success |

## `summaries/<batch>.csv`

The original per-run summary files copied from the internal benchmark workspace.
Columns are the same as `runs.csv` except the batch column.

`summaries/MANIFEST.json` records the source path and SHA-256 of every summary.

## `logs/`

Sanitized, gzip-compressed `run-*.log.gz` files grouped by batch directory.

`logs/MANIFEST.json` records:

- `source` — original internal log path;
- `output` — path in this repository;
- `source_sha256` — hash of the private source log;
- `output_sha256` — hash of the sanitized public file.

No student, teacher, group, course or room names are present. See
`log-sanitization.md`.

## `development/`

Curated engineering before/after snapshots. See `development/README.md` and
`development/claims.csv`. These are not validation runs and must not be combined
with `runs.csv`.

## `configs/validation-config.json`

The shared GA parameters extracted from the validation run logs. Dynamic values
such as timings, operation counters and local server addresses are excluded.
The per-run summaries are authoritative for scores; this file documents the
shared configuration.
