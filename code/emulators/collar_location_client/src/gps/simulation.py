from gps_sensor import GPSSensor
from typing import Optional
import time
import threading


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
