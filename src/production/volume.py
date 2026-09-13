"""Rain-to-production interpolation with explicit loss terms."""
from math import ceil


def gross_volume_liters(
    rainfall_mm: float,
    catchment_area_m2: float,
    runoff_coefficient: float,
    collection_efficiency: float,
) -> float:
    if rainfall_mm < 0 or catchment_area_m2 < 0:
        raise ValueError("rainfall and catchment area must be non-negative")
    if not 0 <= runoff_coefficient <= 1:
        raise ValueError("runoff coefficient must be between 0 and 1")
    if not 0 <= collection_efficiency <= 1:
        raise ValueError("collection efficiency must be between 0 and 1")
    # 1 mm over 1 m² = 1 litre.
    return rainfall_mm * catchment_area_m2 * runoff_coefficient * collection_efficiency


def usable_volume_liters(
    gross_liters: float,
    first_flush_liters: float,
    rejected_liters: float,
    storage_losses_liters: float,
) -> float:
    values = (gross_liters, first_flush_liters, rejected_liters, storage_losses_liters)
    if any(v < 0 for v in values):
        raise ValueError("volume terms must be non-negative")
    return max(0.0, gross_liters - first_flush_liters - rejected_liters - storage_losses_liters)


def required_bags(expected_usable_liters: float, bag_capacity_liters: float, safety_factor: float = 1.10) -> int:
    if expected_usable_liters < 0 or bag_capacity_liters <= 0 or safety_factor < 1:
        raise ValueError("invalid bag planning parameters")
    return ceil(expected_usable_liters * safety_factor / bag_capacity_liters)
