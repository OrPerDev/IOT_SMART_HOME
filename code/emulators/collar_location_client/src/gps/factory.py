from enum import Enum
from typing import Optional
from gps_sensor import GPSSensor


class GPSMode(str, Enum):
    SENSOR = "SENSOR"
    SIMULATION = "SIMULATION"


def new_gps_sensor(
    mode: GPSMode,
    interval_seconds: float = 1,
    simulation_file_path: Optional[str] = None,
) -> GPSSensor:
    if mode == GPSMode.SENSOR:
        return GPSSensor(interval_seconds=interval_seconds)
    elif mode == GPSMode.SIMULATION:
        from .simulation import LocationSimulator

        return LocationSimulator(
            interval_seconds=interval_seconds, simulation_file_path=simulation_file_path
        )
    else:
        raise RuntimeError(f"Invalid GPS mode: {mode}")
