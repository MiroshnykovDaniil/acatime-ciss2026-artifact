# Bridge module

Tools for running AcaTime on public ITC 2019 instances:

- `tools/convert.py` — ITC XML to AcaTime input;
- `tools/scripts_gen.py` — generated rule/constraint scripts;
- `tools/post.py` — candidate pinning and room consolidation;
- `tools/run_from_solution.py` — scored solution to runner seed;
- local-search and room-search scripts used by the experimental pipeline.

The scorer is `tools/score.py`; `code/scorer/README.md` documents its usage.

## Convert and run

```bash
make itc-data
python3 code/bridge/tools/convert.py itc-data/tg-fal17_reduced.xml build
dotnet run --project code/runner/AcaTime.ItcRunner.csproj -c Release -- \
  build/out/tg-fal17/api-scheduledata.json build/runs genetic TimeoutInSeconds=60
```

The runner output is not yet an official ITC solution. The post-processing and
scoring steps are described in `docs/reproducing.md` and `docs/bridge.md`.

The ITC dataset is the competition-reduced DTU version; see
`itc-data/README.md`. It is not the raw competition XML and not the
post-competition reduction.

Full certified results and curated commands remain in the companion artifact:
<https://doi.org/10.5281/zenodo.24083720>.
