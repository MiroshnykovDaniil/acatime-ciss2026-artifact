#!/usr/bin/env python3
"""Create sanitized development logs for the engineering claims.

The raw logs are in the internal AcaTime workspace and are not part of this
repository. Set ACATIME_BENCHMARK_RESULTS to that workspace's benchmark-results
directory before running this script.

Only the named before/after snapshots are included. The 183-run tuning corpus is
not copied; see development/README.md.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path(os.environ["ACATIME_BENCHMARK_RESULTS"])
OUT = ROOT / "development"
MANIFEST = OUT / "MANIFEST.json"

GROUPS = {
    "clone": [
        "20260830-212640",  # clone elision only
        "20260830-213228",  # + copy-on-write
        "20260830-215343",  # clone-consistency fix
    ],
    "parallel": [
        "20260831-131812",  # parallel lineage batch
        "20260831-120250",  # candidate sequential baseline
        "20260831-121008",  # candidate sequential baseline
    ],
}


def sanitize(text: str) -> str:
    text = text.replace("http://localhost:5129/", "[server]")
    text = re.sub(r"https?://\S+", "[url]", text)
    text = re.sub(r"/Users/\S+", "[path]", text)

    rule_names = dict(
        re.findall(r"CheapEval: правило (\d+) '([^']+)'", text)
    )
    for rule_id, name in rule_names.items():
        text = text.replace(name, f"rule_{rule_id}")

    text = re.sub(
        r"(\[0\]\s+)[^-\n]+?(\s+-\s+(\d+)\s+-)",
        lambda m: m.group(1) + f"rule_{m.group(3)}" + m.group(2),
        text,
    )
    text = text.replace("2025-2026 1й сем.", "[semester]")
    return text


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    OUT.mkdir(exist_ok=True)
    manifest = []
    for group, sources in GROUPS.items():
        for source in sources:
            src_dir = SOURCE_ROOT / source
            dst_dir = OUT / group / source
            dst_dir.mkdir(parents=True, exist_ok=True)

            summary_src = src_dir / "summary.csv"
            summary_dst = dst_dir / "summary.csv"
            if summary_src.exists():
                shutil.copy2(summary_src, summary_dst)

            for src in sorted(src_dir.glob("run-*.log")):
                clean = sanitize(src.read_text(errors="ignore"))
                dst = dst_dir / f"{src.stem}.log.gz"
                with gzip.open(dst, "wt", encoding="utf-8") as f:
                    f.write(clean)
                manifest.append(
                    {
                        "group": group,
                        "source_dir": source,
                        "source": str(src.relative_to(SOURCE_ROOT)),
                        "output": str(dst.relative_to(ROOT)),
                        "source_sha256": sha256(src),
                        "output_sha256": sha256(dst),
                        "summary": str(summary_dst.relative_to(ROOT)) if summary_src.exists() else None,
                        "summary_sha256": sha256(summary_dst) if summary_src.exists() else None,
                    }
                )

    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"wrote {len(manifest)} sanitized development logs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
