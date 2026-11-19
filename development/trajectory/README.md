# Observational development trajectory

`DEVELOPMENT-PHASES.csv` contains the aggregated 5-run batch data used for the
development-trajectory figure in the paper.

This is **observational** engineering data, not a controlled ablation:

- phase boundaries are approximate;
- later phases contain multiple code and configuration changes;
- the two very high batches have weak Default baselines;
- the CSV includes three aggregate final-validation rows for reference; they are
  not development batches and must not be aggregated with them.

The raw logs for all development batches are not published. Only the curated
before/after snapshots in `../clone/` and `../parallel/` are included.
