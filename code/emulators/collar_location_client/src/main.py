from gps_sensor import new_gps_sensor
from network_interface import NetworkInterface
from common.environment import COLLAR_ID, PET_GPS_SENSOR_CONFIG


if __name__ == "__main__":
    network_interface = NetworkInterface(collar_id=COLLAR_ID)

    gps_sensor = new_gps_sensor(**PET_GPS_SENSOR_CONFIG)
    # bind producer to gps events
    gps_sensor.on_new_location = network_interface.on_gps_location_update

    gps_sensor.start()
