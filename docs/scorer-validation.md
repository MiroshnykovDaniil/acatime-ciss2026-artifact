# Scorer validation

The independent ITC 2019 scorer is `code/bridge/tools/score.py`. It implements
the PATAT-2018 formulas for time, room, distribution and student costs and is
the referee for public ITC results.

This repository includes the scorer and bridge tools, but **not** the certified
ITC solution set or its validation table. Those remain in the companion
artifact:

<https://doi.org/10.5281/zenodo.24083720>

The production validation runs in this repository are not scored with the ITC
scorer; they use the institution's own script-defined rules.

## What the scorer emits

- hard feasibility and violation list;
- time, room, distribution and student penalties;
- total cost;
- unsupported constraint types.

For the certified ITC results and scorer parity records, use the companion
artifact.
