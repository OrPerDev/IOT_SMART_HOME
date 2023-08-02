from gps_sensor import GPSMode

# Just for demo purposes
COLLAR_ID = "12345"

APPLICATION_GPS_SENSOR_CONFIG = {
    "mode": GPSMode.SIMULATION,
    "interval_seconds": 1.2,
    "simulation_file_path": "./simulation_files/user_location_route.txt",
}

PET_GPS_SENSOR_CONFIG = {
    "mode": GPSMode.SIMULATION,
    "interval_seconds": 1,
    "simulation_file_path": "./simulation_files/pet_location_route.txt",
}
