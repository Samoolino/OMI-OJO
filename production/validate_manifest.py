#!/usr/bin/env python3
"""Validate the Blue-Ether production manifest without external dependencies."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
manifest = ROOT / "production-manifest.json"

try:
    data = json.loads(manifest.read_text(encoding="utf-8"))
except Exception as exc:
    print(f"MANIFEST_INVALID: {exc}")
    sys.exit(2)

expected = [f"P{i}" for i in range(1, 18)]
gates = data.get("gates", {})
missing = [g for g in expected if g not in gates]
if missing:
    print("MISSING_GATES:" + ",".join(missing))
    sys.exit(2)

pending = [g for g in expected if gates[g] != "PASS"]
if pending:
    print("READINESS_BLOCKED:" + ",".join(pending))
    sys.exit(1)

controls = data.get("release_controls", {})
if controls.get("deploy_requires_readiness") is not True:
    print("READINESS_CONTROL_INVALID")
    sys.exit(2)
if controls.get("makefile_is_final_commit") is not True:
    print("FINAL_COMMIT_CONTROL_INVALID")
    sys.exit(2)

if data.get("production_state") != "RELEASED":
    print("RELEASE_NOT_ATTESTED")
    sys.exit(1)

print("PRODUCTION_READY")
