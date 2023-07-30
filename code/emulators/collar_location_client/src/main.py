from gps import new_gps_sensor
from updates_controller import UpdatesController
import os
from environment import COLLAR_ID, GPS_SENSOR_MODE, SIMULATION_ROUTE_PATH


def absolute_path(relative_path: str) -> str:
    return os.path.join(os.path.dirname(__file__), relative_path)


if __name__ == "__main__":
    producer = UpdatesController(collar_id=COLLAR_ID)

    gps_sensor = new_gps_sensor(
        mode=GPS_SENSOR_MODE,
        interval_seconds=1,
        simulation_file_path=absolute_path(SIMULATION_ROUTE_PATH),
    )

    gps_sensor.on_new_location = producer.on_gps_location_update

    gps_sensor.start()
