"""Source registry and provenance rules for environmental observations."""
from dataclasses import dataclass
from typing import Literal

SourceKind = Literal["FORECAST", "HISTORICAL", "STATION", "IOT", "LAB", "CALCULATED"]


@dataclass(frozen=True)
class DataSource:
    source_id: str
    provider: str
    kind: SourceKind
    trust_tier: int
    variables: tuple[str, ...]
    enabled: bool = True


class SourceRegistry:
    def __init__(self) -> None:
        self._sources: dict[str, DataSource] = {}

    def register(self, source: DataSource) -> None:
        if source.trust_tier not in (1, 2, 3, 4):
            raise ValueError("trust_tier must be 1..4")
        if source.source_id in self._sources:
            raise ValueError(f"source already registered: {source.source_id}")
        self._sources[source.source_id] = source

    def get(self, source_id: str) -> DataSource:
        return self._sources[source_id]

    def enabled_for(self, variable: str) -> list[DataSource]:
        return [s for s in self._sources.values() if s.enabled and variable in s.variables]

    def as_dict(self) -> dict[str, dict]:
        return {
            key: {
                "provider": value.provider,
                "kind": value.kind,
                "trust_tier": value.trust_tier,
                "variables": list(value.variables),
                "enabled": value.enabled,
            }
            for key, value in self._sources.items()
        }
