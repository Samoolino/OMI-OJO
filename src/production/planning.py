"""Operational collection planning from predicted usable yield."""
from .models import CollectionPlan
from .volume import required_bags


def make_collection_plan(
    event_id: str,
    predicted_rainfall_mm: float,
    catchment_area_m2: float,
    runoff_coefficient: float,
    collection_efficiency: float,
    first_flush_liters: float,
    rejected_liters: float,
    storage_losses_liters: float,
    bag_capacity_liters: float,
    safety_factor: float = 1.10,
) -> CollectionPlan:
    from .volume import gross_volume_liters, usable_volume_liters
    gross = gross_volume_liters(
        predicted_rainfall_mm, catchment_area_m2, runoff_coefficient, collection_efficiency
    )
    usable = usable_volume_liters(gross, first_flush_liters, rejected_liters, storage_losses_liters)
    bags = required_bags(usable, bag_capacity_liters, safety_factor)
    return CollectionPlan(
        event_id=event_id,
        expected_gross_liters=gross,
        expected_usable_liters=usable,
        bag_capacity_liters=bag_capacity_liters,
        safety_factor=safety_factor,
        required_bags=bags,
        reserve_bags=max(1, int(bags * 0.10)) if bags else 0,
    )
