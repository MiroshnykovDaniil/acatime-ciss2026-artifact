# Runner module

The runner hosts the GA locally and does not require the AcaTime web API,
database or production configuration. It reads a converted AcaTime schedule
JSON and writes the selected slots plus run statistics.

## Build

```bash
dotnet build code/AcaTime.GA.sln -c Release
```

## Run

```bash
dotnet run --project code/runner/AcaTime.ItcRunner.csproj -c Release -- \
  <api-scheduledata.json> <outDir> [algorithm] [key=value ...]
```

- `algorithm`: `default` or `genetic`;
- parameters include `TimeoutInSeconds`, `GeneticIterations`, `SlotsTopK`,
  `DomainsTopK`, `SlotsTemperature`, `DomainsTemperature` and
  `IgnoreClassrooms`;
- output: `run-<algorithm>-<timestamp>.json` in `<outDir>`.

Example:

```bash
dotnet run --project code/runner/AcaTime.ItcRunner.csproj -c Release -- \
  build/out/tg-fal17/api-scheduledata.json build/runs genetic TimeoutInSeconds=60
```

The production faculty data is private. The runner can be used on any converted
AcaTime input; the public ITC 2019 bridge is in `code/bridge/`.

For the ITC 2019 end-to-end pipeline, see `code/bridge/README.md` and
`docs/reproducing.md`. Certified ITC results are in the companion artifact:
<https://doi.org/10.5281/zenodo.24083720>.
