from __future__ import annotations
from typing import Protocol, TypeAlias, Optional
from helpers import get_gps_location
import time
import threading

GpsLocation: TypeAlias = tuple[float, float]


class OnNewLocationFn(Protocol):
    def __call__(self, location: GpsLocation) -> None:
        """Called when a new location is available"""


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
            self.location = get_gps_location()
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
