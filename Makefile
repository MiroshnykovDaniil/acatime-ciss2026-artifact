.PHONY: help verify build test clean itc-data check-itc-data

help:
	@echo "Targets:"
	@echo "  verify         Check 17-run aggregates, summary hashes and log hashes"
	@echo "  build          Build the GA and local runner"
	@echo "  test           Run the GA unit tests"
	@echo "  itc-data       Download and verify public ITC 2019 reduced instances"
	@echo "  check-itc-data Verify an existing ITC data directory"
	@echo "  clean          Remove build outputs"

verify:
	python3 scripts/verify_aggregates.py

build:
	dotnet build code/AcaTime.GA.sln -c Release

test:
	dotnet test code/ga/AcaTime.Algorithm.Genetic.Tests/AcaTime.Algorithm.Genetic.Tests.csproj -c Release

itc-data:
	./itc-data/download.sh

check-itc-data:
	./scripts/check_data.sh

clean:
	rm -rf build
	find code -type d \( -name bin -o -name obj \) -prune -exec rm -rf {} +
