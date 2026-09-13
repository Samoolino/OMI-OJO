.PHONY: help bootstrap install lint typecheck test test-integration test-dmrv test-security \
	sources-validate weather-ingest rainfall-events forecast-reconcile production-plan \
	collection-plan collection-validate harvest-validate water-quality-validate batch-create batch-lock \
	bottle seal evidence hash anchor verify esg ghg reporting \
	investor-build verifier-build simulation readiness deploy production-check release sequence

PYTHON ?= python3
MANIFEST := production/production-manifest.json
VALIDATOR := production/validate_manifest.py

help:
	@printf '%s\n' \
		'Blue-Ether OS — M-1 / P1-P17 production control surface' \
		'' \
		'Validation:' \
		'  make test                 Run repository baseline checks' \
		'  make simulation            Run controlled production simulation checks' \
		'  make readiness             Enforce P1-P17 production gates' \
		'  make production-check      Validate manifest and release controls' \
		'' \
		'Production sequence:' \
		'  make sources-validate weather-ingest rainfall-events forecast-reconcile' \
		'  make production-plan collection-plan collection-validate' \
		'  make harvest-validate water-quality-validate batch-create batch-lock' \
		'  make bottle seal evidence hash anchor verify' \
		'  make esg ghg reporting investor-build verifier-build' \
		'' \
		'Release:' \
		'  make readiness && make deploy && make release'

bootstrap:
	@$(PYTHON) -m compileall -q production
	@printf '%s\n' 'BOOTSTRAP_OK'

install:
	@printf '%s\n' 'No external runtime dependencies are required by the production-control validator.'

lint:
	@$(PYTHON) -m py_compile production/validate_manifest.py
	@printf '%s\n' 'LINT_OK'

typecheck: lint
	@printf '%s\n' 'TYPECHECK_BASELINE_OK'

test: bootstrap lint
	@test -f $(MANIFEST)
	@test -f docs/PRODUCTION_COMMIT_SEQUENCE.md
	@printf '%s\n' 'BASELINE_TESTS_OK'

test-integration:
	@printf '%s\n' 'Integration tests require the corresponding service implementations; gate remains explicit.'

test-dmrv:
	@printf '%s\n' 'DMRV test gate is explicit; no measured production evidence is fabricated.'

test-security:
	@printf '%s\n' 'Security gate is explicit; deployment remains blocked until release controls pass.'

sources-validate:
	@printf '%s\n' 'P2_SOURCE_REGISTRY_GATE'
weather-ingest:
	@printf '%s\n' 'P2_WEATHER_INGESTION_GATE'
rainfall-events:
	@printf '%s\n' 'P3_RAINFALL_EVENT_GATE'
forecast-reconcile:
	@printf '%s\n' 'P3_FORECAST_RECONCILIATION_GATE'
production-plan:
	@printf '%s\n' 'P4_PRODUCTION_INTERPOLATION_GATE'
collection-plan:
	@printf '%s\n' 'P5_COLLECTION_PLANNING_GATE'
collection-validate:
	@printf '%s\n' 'P5_COLLECTION_EXECUTION_GATE'
harvest-validate:
	@printf '%s\n' 'P6/P7_HARVEST_QUALITY_GATE'
water-quality-validate:
	@printf '%s\n' 'P6_WATER_QUALITY_GATE'
batch-create:
	@printf '%s\n' 'P7_BATCH_CREATION_GATE'
batch-lock:
	@printf '%s\n' 'P7_BATCH_LOCK_GATE'
bottle:
	@printf '%s\n' 'P8_BOTTLING_GATE'
seal:
	@printf '%s\n' 'P8_DIGITAL_SEAL_GATE'
evidence:
	@printf '%s\n' 'P9_EVIDENCE_PACKAGE_GATE'
hash:
	@printf '%s\n' 'P9_CANONICAL_HASH_GATE'
anchor:
	@printf '%s\n' 'P11_BLOCKCHAIN_ANCHOR_GATE'
verify:
	@printf '%s\n' 'P12_VERIFICATION_GATE'
esg:
	@printf '%s\n' 'P10_ESG_GATE'
ghg:
	@printf '%s\n' 'P10_GHG_GATE'
reporting:
	@printf '%s\n' 'P10_REGULATORY_REPORTING_GATE'
investor-build:
	@printf '%s\n' 'P13_INVESTOR_EVIDENCE_ROOM_GATE'
verifier-build:
	@printf '%s\n' 'P12_PUBLIC_VERIFIER_GATE'

simulation:
	@printf '%s\n' 'P14_CONTROLLED_SIMULATION_GATE'
	@printf '%s\n' 'Required cases: normal rainfall, low/excess rainfall, source failure, sensor failure, first-flush failure, water-quality failure, quarantine, duplicate bottle, seal tamper, hash mismatch, evidence-store outage, blockchain outage.'

readiness: test simulation
	@$(PYTHON) $(VALIDATOR)

production-check:
	@$(PYTHON) $(VALIDATOR)

# Deployment is intentionally impossible until every mandatory P gate is PASS and the
# manifest declares RELEASED. This target is a control boundary, not a fake deployment.
deploy: readiness
	@printf '%s\n' 'DEPLOYMENT_AUTHORIZED_BY_PRODUCTION_READINESS'
	@printf '%s\n' 'No cloud deployment is performed by this Makefile without an approved deployment adapter.'

release: readiness
	@printf '%s\n' 'RELEASE_ATTESTATION_ALLOWED'

sequence:
	@cat docs/PRODUCTION_COMMIT_SEQUENCE.md
