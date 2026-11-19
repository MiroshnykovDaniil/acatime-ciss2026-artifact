# Cheap-evaluation per-rule measurements

`per-rule.csv` is transcribed from `ALGORITHM-NOTES-20260830-CHEAP-EVAL.md`
(section 3, "Results", 40 random moves per rule).

These are **benchmark-program measurements**, not run logs. The bench loads the
real API payload, compiles the real rules, and compares the incremental move
delta with a full rule evaluation. The measured average was **9.2× per candidate**
for season 13 and **10.1×** for season 3.

Important caveats:

- these are per-rule measurements from a development benchmark;
- they are not a controlled multi-institution ablation;
- the engine keeps a running total, so the in-engine speedup is expected to be
  higher than the bench value;
- season 3 contains one probe-escape case (24/40 exact); the runtime layer keeps
  that rule on full evaluation, which is the intended fallback behaviour.

The source benchmark program and rule files remain in the private AcaTime
workspace. This CSV is the public summary needed to check the reported range and
average.
