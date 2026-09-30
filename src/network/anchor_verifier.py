from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .anchor_registry import AnchorRecord


class VerificationState(str, Enum):
    MATCHED = "MATCHED"
    MISMATCHED = "MISMATCHED"
    NOT_FOUND = "NOT_FOUND"


@dataclass(frozen=True)
class VerificationResult:
    state: VerificationState
    anchor_id: str | None
    expected_root: str
    anchored_root: str | None
    network_id: str | None
    transaction_id: str | None


def verify_anchor_root(
    *,
    anchor: AnchorRecord | None,
    expected_root: str,
) -> VerificationResult:
    if anchor is None:
        return VerificationResult(
            state=VerificationState.NOT_FOUND,
            anchor_id=None,
            expected_root=expected_root,
            anchored_root=None,
            network_id=None,
            transaction_id=None,
        )
    state = VerificationState.MATCHED if anchor.root_hash == expected_root else VerificationState.MISMATCHED
    return VerificationResult(
        state=state,
        anchor_id=anchor.anchor_id,
        expected_root=expected_root,
        anchored_root=anchor.root_hash,
        network_id=anchor.network_id,
        transaction_id=anchor.transaction_id,
    )
