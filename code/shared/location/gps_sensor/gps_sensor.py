from __future__ import annotations
from typing import Protocol, TypeAlias, Optional
import threading
import time
import gpsd

GpsLocation: TypeAlias = tuple[float, float]

class OnNewLocationFn(Protocol):
    def __call__(self, location: GpsLocation) -> None:
        """Called when a new location is available"""


def _get_gps_location() -> GpsLocation | None:
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
    def __init__(self, interval_seconds: int = 1):
        self.location = None
        self._on_new_location = lambda location: None

        self._interval_seconds = interval_seconds

        self._thread: Optional[threading.Thread] = None

        self._running = False

    def _run(self):
        self._running = True
        while self._running:
            time.sleep(self._interval_seconds)
            self.location = _get_gps_location()
            if self.location is not None:
                self._on_new_location(self.location)

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

    def set_location(self, location: GpsLocation) -> None:
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
