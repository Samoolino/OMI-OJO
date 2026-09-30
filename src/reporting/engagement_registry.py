"""Canonical engagement/work-package control plane.

The registry is configuration-first: it validates engagement scope and binds
reporting work to explicit grant/institutional work packages without changing
source, evidence, or release semantics.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WorkPackageBinding:
    engagement_id: str
    project_id: str
    work_package_ids: tuple[str, ...]
    release_policy: str
    anchor_required: bool


class EngagementRegistry:
    def __init__(
        self,
        *,
        engagement_path: str | Path = "config/reporting-engagement-registry.json",
        binding_path: str | Path = "config/engagement-work-package-bindings.json",
    ) -> None:
        self.engagements = json.loads(Path(engagement_path).read_text(encoding="utf-8")).get("engagements", [])
        payload = json.loads(Path(binding_path).read_text(encoding="utf-8"))
        self.bindings = {
            item["engagement_id"]: WorkPackageBinding(
                engagement_id=item["engagement_id"],
                project_id=item["project_id"],
                work_package_ids=tuple(item["work_package_ids"]),
                release_policy=item["release_policy"],
                anchor_required=bool(item["anchor_required"]),
            )
            for item in payload.get("bindings", [])
        }

    def get(self, engagement_id: str) -> dict:
        for engagement in self.engagements:
            if engagement["engagement_id"] == engagement_id:
                return engagement
        raise KeyError(f"unknown engagement: {engagement_id}")

    def binding(self, engagement_id: str) -> WorkPackageBinding:
        try:
            return self.bindings[engagement_id]
        except KeyError as exc:
            raise KeyError(f"no work-package binding for engagement: {engagement_id}") from exc

    def validate(self, engagement_id: str, project_id: str) -> WorkPackageBinding:
        engagement = self.get(engagement_id)
        binding = self.binding(engagement_id)
        if project_id not in engagement["project_ids"]:
            raise ValueError("project is outside engagement scope")
        if binding.project_id != project_id:
            raise ValueError("work-package binding project does not match engagement")
        if not binding.work_package_ids:
            raise ValueError("engagement has no work packages")
        return binding
