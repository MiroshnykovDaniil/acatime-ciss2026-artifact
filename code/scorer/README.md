# Scorer module

The scorer is the independent ITC 2019 cost function used as the referee for
public ITC results. The implementation is in `code/bridge/tools/score.py`; this
directory documents the entry point.

Usage:

```bash
python3 code/bridge/tools/score.py itc-data/tg-fal17_reduced.xml \
  results/tg-fal17/solution.json
```

It uses only the Python standard library. AcaTime's internal objective proxy is
never used as a reported ITC score.

The certified solutions and scorer validation records are in the companion
artifact: <https://doi.org/10.5281/zenodo.24083720>.
