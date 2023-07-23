from __future__ import annotations
from typing import Protocol, TypeAlias, Optional

GpsLocation: TypeAlias = tuple[float, float]


class OnNewLocationFn(Protocol):
    def __call__(self, location: GpsLocation) -> None:
        """Called when a new location is available"""


class GPSSensor:
    def __init__(self):
        self.location = None
        self._on_new_location = lambda location: None

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
