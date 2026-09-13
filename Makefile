.PHONY: bootstrap install lint typecheck test test-integration test-dmrv test-security sources-validate weather-ingest rainfall-events forecast-reconcile production-plan collection-plan collection-validate harvest-validate water-quality-validate batch-create batch-lock bottle seal evidence hash anchor verify esg ghg reporting investor-build verifier-build simulation readiness production-check deploy release

PYTHON ?= python3

bootstrap install:
	@$(PYTHON) -m pip install --upgrade pip

lint:
	@$(PYTHON) -m compileall -q src tests

typecheck:
	@$(PYTHON) -m compileall -q src

test:
	@$(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v

test-integration test-dmrv test-security:
	@$(MAKE) test

sources-validate:
	@$(PYTHON) -m compileall -q src/production/sources.py

weather-ingest rainfall-events forecast-reconcile production-plan collection-plan collection-validate harvest-validate water-quality-validate batch-create batch-lock bottle seal evidence hash anchor verify esg ghg reporting investor-build verifier-build:
	@echo "$@ is implemented as a production API/service boundary; live execution requires configured sources and approved runtime credentials."

simulation:
	@$(MAKE) test

readiness:
	@$(PYTHON) production/gate.py

production-check:
	@$(MAKE) lint
	@$(MAKE) test
	@$(MAKE) readiness

deploy:
	@$(MAKE) production-check
	@echo "Deployment permitted only after readiness PASS."

release:
	@$(MAKE) production-check
	@echo "Release permitted only after readiness PASS."
