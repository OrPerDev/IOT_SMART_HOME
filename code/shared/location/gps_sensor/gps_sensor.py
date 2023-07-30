from __future__ import annotations
from typing import Protocol, TypeAlias, Optional
from enum import Enum
import threading
import time
import gpsd

GpsLocation: TypeAlias = tuple[float, float]


class OnNewLocationFn(Protocol):
    def __call__(self, location: Optional[GpsLocation]) -> None:
        """Called when a new location is available"""


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
        return LocationSimulator(
            interval_seconds=interval_seconds, simulation_file_path=simulation_file_path
        )
    else:
        raise RuntimeError(f"Invalid GPS mode: {mode}")


def _get_gps_location() -> Optional[GpsLocation]:
    try:
        gpsd.connect()
        packet = gpsd.get_current()

        if packet.mode >= 2 and packet.mode <= 3:
            latitude, longitude = packet.position()
            return latitude, longitude
        else:
            print("Unable to get a fix on GPS signal of device.")
            return None

    except Exception as e:
        print("Error occurred while fetching GPS location:", str(e))
        return None


class GPSSensor:
    def __init__(self, interval_seconds: float = 1.0):
        self.location = None
        self._on_new_location = lambda location: None

        self._interval_seconds = interval_seconds

        self._thread: Optional[threading.Thread] = None

        self._running = False

    def _run(self):
        self._running = True
        while self._running:
            self.set_location(_get_gps_location())
            time.sleep(self._interval_seconds)

    def stop(self):
        self._running = False
        if self._thread is not None:
            self._thread.join()
            self._thread = None

    def start(self):
        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def get_location(self) -> Optional[GpsLocation]:
        return self.location

    def set_location(self, location: Optional[GpsLocation]) -> None:
        if location == self.location:
            # no change - do nothing
            return
        self.location = location
        self._on_new_location(location)

    @property
    def on_new_location(self) -> Optional[OnNewLocationFn]:
        return self._on_new_location

    @on_new_location.setter
    def on_new_location(self, on_new_location: OnNewLocationFn) -> None:
        if not callable(on_new_location):
            raise ValueError("on_new_location must be callable")
        self._on_new_location = on_new_location


class LocationSimulator(GPSSensor):
    def __init__(
        self, interval_seconds: float = 1.0, simulation_file_path: Optional[str] = None
    ):
        super().__init__(interval_seconds=interval_seconds)
        self.simulation_file_path = simulation_file_path

        self._thread: Optional[threading.Thread] = None

        self._running = False

    def start(self) -> None:
        print("[Simulation]: Starting location simulation")
        if self.simulation_file_path is None:
            raise RuntimeError("Simulation file path not provided")

        print("[Simulation]: Reading simulation file")
        self._thread = threading.Thread(target=self._read_simulation_file)
        self._running = True
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread is not None:
            self._thread.join()
            self._thread = None

    def _read_simulation_file(self):
        if self.simulation_file_path is None:
            raise RuntimeError("Simulation file path not provided")

        with open(self.simulation_file_path, "r") as f:
            while self._running:
                line = f.readline()
                if not line:
                    break
                # line is float,float
                location = tuple(
                    [float(val.strip()) for val in line.strip().split(",")]
                )
                if len(location) != 2:
                    raise RuntimeError(f"Invalid GPS location line: {line}")
                print(f"[Simulation]: Producing new user location: {location}")
                self.set_location(location=location)
                time.sleep(self._interval_seconds)

        if self._running:
            self.stop()
