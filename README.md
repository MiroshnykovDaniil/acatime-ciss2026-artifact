# AcaTime CISS-2026 artifact

**Rule-aware incremental evaluation in a hybrid genetic algorithm for university timetabling**

This repository combines the exact AcaTime GA source snapshot, a local runner,
the 17 anonymized faculty-scale validation logs, and the scripts needed to check
the published aggregates.

It accompanies the CISS-2026 short paper:

> Daniil Miroshnykov, Liudmyla Omelchuk. *Rule-aware incremental evaluation in a
> hybrid genetic algorithm for university timetabling.* CISS-2026.

**Status:** artifact prepared for CISS-2026. A Zenodo DOI is to be reserved for
this repository. The companion ITC 2019 artifact is archived at
[10.5281/zenodo.24083720](https://doi.org/10.5281/zenodo.24083720).

## What is included

- **Algorithm:** exact snapshot of the GA projects used for the paper:
  `AcaTime.Algorithm.Genetic`, `AcaTime.Algorithm.Default`,
  `AcaTime.ScheduleCommon`, `AcaTime.ScriptModels`, and unit tests.
- **Runner:** local host that runs the GA without the AcaTime web API, database
  or production configuration.
- **ITC bridge and scorer:** tools for converting public ITC 2019 instances,
  running the GA, and scoring solutions with the independent ITC scorer.
- **Validation evidence:** 17 faculty-scale runs, aggregate CSV, per-run
  summaries, and gzip-compressed sanitized logs.
- **Development reference runs:** a small curated `development/` set for the
  engineering claims (clone/COW/clone-fix, parallel candidate comparison and
  cheap-evaluation per-rule table). These are not validation runs.
- **Checks:** SHA-256 manifests and scripts that recompute the range, median and
  per-run percentages.

## What is not included

The production AcaTime backend, faculty schedules, students, teachers, rooms,
institution-specific rules, and raw server logs are **not** public. The 17 logs
are sanitized evidence, not replayable inputs.

The 17 production runs cannot be reproduced from this repository alone. The
public code can be built and tested, and the GA can be run on public ITC 2019
data through the included bridge.

## Quick start

Requirements:

- .NET SDK **9.0.201** (`global.json`, roll-forward enabled);
- Python **3.10+**;
- `numpy` only for the optional ITC local-search/room pipeline.

```bash
make verify       # check the 17-run aggregates, summaries and log hashes
make build        # build the GA and runner
make test         # run the GA unit tests
```

`make verify` does not need .NET and does not rerun the production scheduler.

## Repository layout

```text
code/
  ga/             exact GA source snapshot
  runner/         local runner for converted AcaTime/ITC data
  bridge/         ITC XML -> AcaTime conversion and post-processing tools
  scorer/         scorer entry point and documentation
  AcaTime.GA.sln  build solution
configs/          shared validation parameters
summaries/        per-run source summaries + SHA-256 manifest
logs/             sanitized gzip logs + manifest
development/      curated engineering before/after snapshots
runs.csv          consolidated 17-run results
scripts/          aggregate verifier and log sanitizer
docs/             privacy, provenance, sanitization, claims, reproduction
itc-data/         public ITC 2019 downloader and checksums (XML files not committed)
```

## Running the GA

Build:

```bash
make build
```

Run the local runner on a converted AcaTime input:

```bash
dotnet run --project code/runner/AcaTime.ItcRunner.csproj -c Release -- \
  <api-scheduledata.json> <outDir> genetic TimeoutInSeconds=60
```

The runner writes a JSON file with the selected slots and run statistics. See
`code/runner/README.md` for the input/output contract and parameters.

For public ITC 2019 data:

```bash
make itc-data
python3 code/bridge/tools/convert.py itc-data/tg-fal17_reduced.xml build
dotnet run --project code/runner/AcaTime.ItcRunner.csproj -c Release -- \
  build/out/tg-fal17/api-scheduledata.json build/runs genetic TimeoutInSeconds=60
```

The conversion and post-processing details are in `code/bridge/README.md` and
`docs/reproducing.md`. Certified ITC results and the full experiment
configuration remain in the companion artifact:
<https://doi.org/10.5281/zenodo.24083720>.

## Validation evidence

The 17 runs are from 2026-09-02:

- 830 student groups and 7,485 lesson slots;
- all 17 runs improved the Default schedule;
- improvement range: **22.41%–80.79%**;
- median: **43.30%**; mean: **47.51%**.

Files:

- `runs.csv` — consolidated table;
- `summaries/` — per-run source summaries;
- `logs/` — sanitized, gzip-compressed logs;
- `docs/claims.md` — claim-to-evidence map;
- `docs/privacy.md` — what is withheld and why;
- `docs/log-sanitization.md` — exact sanitization rules.

## Development reference runs

`development/` contains a deliberately small set of before/after snapshots for
the engineering measurements in the paper. It is not part of the 17-run
validation result and must not be aggregated with it.

- `development/clone/` — three single-run clone/COW/clone-fix snapshots;
- `development/parallel/` — the 5-run parallel batch plus two 5-run candidate
  sequential baselines (mapping unconfirmed);
- `development/cheap-eval/` — per-rule speedup table.

See `development/README.md` and `development/claims.csv` for the caveats.

## Verify

```bash
make verify
```

Expected output includes:

```text
rows: 17
min: 22.4114
max: 80.7947
median: 43.2971
all checks passed
development logs: 18
clone snapshots: 3
parallel logs: 15
per-rule rows: 7
trajectory batches: 50
development checks passed
```

## Licensing

- Code in `code/`: **Apache-2.0** (`LICENSE-APACHE`).
- Data, logs, summaries and documentation: **CC BY 4.0** (`LICENSE`).
- Public ITC 2019 data: the DTU dataset's own license and citation terms; see
  `itc-data/README.md`.

See `LICENSES.md` and `THIRD_PARTY_NOTICES.md`.

## Citation

Citation metadata is in `CITATION.cff`. Until a Zenodo DOI is reserved, cite
this repository URL and the exact commit or tag.
