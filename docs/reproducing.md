# Reproducing and verifying the artifact

This document covers three separate things:

1. checking the published 17-run aggregates and log hashes;
2. building and testing the exact GA source;
3. running the GA on public ITC 2019 data.

It does **not** provide a replay of the 17 production runs: the input faculty
dataset and rules are private.

## 1. Aggregate and log verification

No .NET installation is needed:

```bash
make verify
```

This runs `scripts/verify_aggregates.py` and
`scripts/verify_development.py`. It checks:

- exactly 17 rows in `runs.csv`;
- every `percent` equals `delta / default_score * 100`;
- the reported 22.41–80.79% range, median 43.30% and mean 47.51%;
- SHA-256 checksums of the per-run summaries;
- the sanitized validation-log manifest and hashes;
- the curated `development/` manifest and file counts.

Expected output includes:

```text
rows: 17
min: 22.4114
max: 80.7947
median: 43.2971
all checks passed
```

Inspect a sanitized log:

```bash
gzip -dc logs/20260902-012136/run-1.log.gz | less
```

## 2. Build and test the GA

Requirements:

- .NET SDK **9.0.201** (`global.json`);
- Python 3.10+ for the Python tools.

```bash
make build
make test
```

`make build` builds `code/AcaTime.GA.sln`; `make test` runs the GA unit tests.

## 3. Run the GA on public ITC 2019 data

The public ITC files are the competition-reduced DTU versions, not the raw
competition XML:

```bash
make itc-data
make check-itc-data
```

Convert one instance:

```bash
python3 code/bridge/tools/convert.py itc-data/tg-fal17_reduced.xml build
```

This writes:

```text
build/out/tg-fal17/api-scheduledata.json
```

Run the GA:

```bash
dotnet run --project code/runner/AcaTime.ItcRunner.csproj -c Release -- \
  build/out/tg-fal17/api-scheduledata.json build/runs genetic TimeoutInSeconds=60
```

The runner writes a JSON file containing the selected slots, objective value and
run statistics. Converting that output to an official ITC solution requires the
post-processing tools in `code/bridge/` before scoring with
`code/bridge/tools/score.py`. The certified commands and curated solutions are
in the companion artifact:

<https://doi.org/10.5281/zenodo.24083720>

## Environment and provenance

- Source snapshot: `AcaTime.Common` commit `8669726` (2026-11-09).
- Public import: `acatime-itc2019`, `src/ga` and `src/runner`.
- Python: standard library for the scorer and aggregate verifier; `numpy` for
  the optional local-search/room pipeline.
- Hardware and OS for the original production runs are not recorded in this
  package; do not make new wall-clock claims from a different machine without
  measuring again.

## What remains private

The following are withheld:

- raw faculty schedules and rules;
- student, teacher, group, course and room data;
- raw production logs and server paths;
- the AcaTime production backend and database.

See `privacy.md`, `log-sanitization.md` and `provenance.md`.
