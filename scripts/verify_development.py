#!/usr/bin/env python3
"""Verify development log manifest hashes and file counts."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEV = ROOT / "development"
MANIFEST = DEV / "MANIFEST.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    entries = json.loads(MANIFEST.read_text())
    groups = Counter(e["group"] for e in entries)
    source_dirs = Counter((e["group"], e["source_dir"]) for e in entries)

    expected_logs = {"clone": 3, "parallel": 15}
    expected_dirs = {"clone": 3, "parallel": 3}
    assert dict(groups) == expected_logs, groups
    assert len({d for (g, d) in source_dirs if g == "clone"}) == expected_dirs["clone"]
    assert len({d for (g, d) in source_dirs if g == "parallel"}) == expected_dirs["parallel"]

    for entry in entries:
        out = ROOT / entry["output"]
        assert out.exists(), f"missing {out}"
        assert sha256(out) == entry["output_sha256"], f"hash mismatch {out}"
        if entry.get("summary"):
            summary = ROOT / entry["summary"]
            assert summary.exists(), f"missing {summary}"
            assert sha256(summary) == entry["summary_sha256"], f"summary hash mismatch {summary}"

    per_rule = DEV / "cheap-eval" / "per-rule.csv"
    with per_rule.open() as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 7, f"expected 7 per-rule rows, got {len(rows)}"

    trajectory = DEV / "trajectory" / "DEVELOPMENT-PHASES.csv"
    with trajectory.open() as fh:
        trajectory_rows = list(csv.DictReader(fh))
    assert len(trajectory_rows) == 50, f"expected 50 trajectory rows, got {len(trajectory_rows)}"

    print(f"development logs: {len(entries)}")
    print(f"clone snapshots: {groups['clone']}")
    print(f"parallel logs: {groups['parallel']}")
    print(f"per-rule rows: {len(rows)}")
    print(f"trajectory batches: {len(trajectory_rows)}")
    print("development checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
