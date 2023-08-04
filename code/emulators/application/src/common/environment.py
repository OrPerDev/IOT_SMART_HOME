from gps_sensor import GPSMode
from common.utils import absolute_path

# Just for demo purposes
COLLAR_ID = "12345"

APPLICATION_GPS_SENSOR_CONFIG = {
    "mode": GPSMode.SIMULATION,
    "interval_seconds": 1.2,
    "simulation_file_path": absolute_path("./simulation_files/user_location_route.txt"),
}
