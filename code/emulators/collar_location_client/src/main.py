from gps_sensor import new_gps_sensor
from updates_controller import UpdatesController
import os
from environment import COLLAR_ID, COLLAR_GPS_SENSOR_CONFIG


def absolute_path(relative_path: str) -> str:
    return os.path.join(os.path.dirname(__file__), relative_path)


if __name__ == "__main__":
    producer = UpdatesController(collar_id=COLLAR_ID)

    gps_sensor = new_gps_sensor(**COLLAR_GPS_SENSOR_CONFIG)
    # bind producer to gps events
    gps_sensor.on_new_location = producer.on_gps_location_update

    gps_sensor.start()
