# Development reference runs

This directory contains a **small, curated set of before/after snapshots** for
the engineering claims in the CISS-2026 paper. It is not part of the 17-run
validation set and must not be aggregated with it.

## Why these runs are here

The validation result (22–81%, median 43.3%) uses only the 17 final runs in
`../logs/`. The paper also reports engineering measurements: cheap delta
evaluation, copy-on-write cloning, the clone-consistency fix and parallel
lineages. These development snapshots document where those numbers came from.

They are **observational**, not controlled ablations:

- the clone/COW/clone-fix points are **single runs** (`n = 1`);
- later code and configuration changes are mixed in;
- the parallel baseline mapping is a candidate mapping and is **not confirmed**;
- the cheap-evaluation numbers come from a benchmark program, not run logs.

## Structure

```text
clone/
  20260830-212640/   clone elision only; 198 iterations; clone ~52.1 s
  20260830-213228/   + copy-on-write; 894 iterations; clone ~13.6 s
  20260830-215343/   clone-consistency fix; 1,361 iterations
parallel/
  20260831-131812/   5 parallel-lineage runs
  20260831-120250/   candidate sequential baseline (5 runs)
  20260831-121008/   candidate sequential baseline (5 runs)
cheap-eval/
  per-rule.csv       per-rule speedup measurements
  README.md          measurement caveats
trajectory/
  DEVELOPMENT-PHASES.csv  aggregated 5-run development batches
  README.md               trajectory caveats
MANIFEST.json        SHA-256 of every sanitized log and summary
claims.csv           claim-to-run mapping and caveats
```

## Sanitization

Development logs use the same transformations as the validation logs:

- local server addresses and URLs removed;
- `/Users/...` paths replaced with `[path]`;
- institution-specific rule names replaced with `rule_<id>`;
- semester label replaced with `[semester]`.

No student, teacher, group or course names are present. See
`../docs/log-sanitization.md`.

## Claims and caveats

See `claims.csv`. In particular:

- do not present the clone snapshots as a controlled 10–15-run ablation;
- do not cite **+17%** for parallel lineages until the sequential baseline
  mapping is confirmed;
- cite the cheap-evaluation table as a benchmark measurement, not as run logs.

`make verify-development` checks the manifest hashes and file counts.
