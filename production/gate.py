"""Fail-closed production gate evaluator for Blue-Ether."""
import json
from pathlib import Path

MANIFEST = Path(__file__).with_name("production-manifest.json")


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    blockers = [key for key, value in data["gates"].items() if value.startswith("PENDING")]
    if blockers:
        print("READINESS=BLOCKED")
        print("BLOCKERS=" + ",".join(blockers))
        return 2
    print("READINESS=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
