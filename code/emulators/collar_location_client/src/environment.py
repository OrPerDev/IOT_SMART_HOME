from gps_sensor import GPSMode

# Just for demo purposes
COLLAR_ID = "12345"

COLLAR_GPS_SENSOR_CONFIG = {
    "mode": GPSMode.SIMULATION,
    "interval_seconds": 1,
    "simulation_file_path": "./simulation_files/location_route.txt",
}
