# Code snapshot

This directory contains the exact GA source used for the CISS-2026 paper. It
was imported from `AcaTime.Common` at commit `8669726` (2026-11-09) through the
public `acatime-itc2019` artifact.

## Projects

| Project | Purpose |
|---|---|
| `ga/AcaTime.Algorithm.Genetic` | AcaTime GA optimizer, rule-aware evaluation and state management |
| `ga/AcaTime.Algorithm.Default` | constructives/default solver used to seed the GA |
| `ga/AcaTime.ScheduleCommon` | schedule model, script execution and mapping utilities |
| `ga/AcaTime.ScriptModels` | public interfaces for faculty seasons, slots and rules |
| `ga/AcaTime.Algorithm.Genetic.Tests` | GA unit tests |
| `runner/` | local host for converted AcaTime/ITC input |
| `bridge/` | ITC 2019 XML conversion and post-processing tools |
| `scorer/` | scorer documentation and entry point |

The production AcaTime backend, database, API, UI and faculty data are not
included. The production defaults are unchanged; the ITC adaptation is opt-in
through runner parameters.

## Build and test

```bash
dotnet build code/AcaTime.GA.sln -c Release
dotnet test code/ga/AcaTime.Algorithm.Genetic.Tests/AcaTime.Algorithm.Genetic.Tests.csproj -c Release
```

The solution uses .NET SDK 9.0.201 (see `global.json`).

## Run

The runner accepts a converted `api-scheduledata.json` file:

```bash
dotnet run --project code/runner/AcaTime.ItcRunner.csproj -c Release -- \
  <api-scheduledata.json> <outDir> genetic TimeoutInSeconds=60
```

The output JSON contains the selected schedule slots, the objective value and
run statistics. See `runner/README.md` for the runner contract.

For public ITC 2019 data, see `bridge/README.md`, `docs/reproducing.md` and the
companion artifact <https://doi.org/10.5281/zenodo.24083720>.

## Source provenance

- Internal source: `AcaTime.Common`, branch `genetic-enhancement`, commit
  `8669726`.
- Public import: `acatime-itc2019`, `src/ga` and `src/runner`.
- No source changes were made for this artifact beyond excluding build outputs
  and adapting documentation paths.
