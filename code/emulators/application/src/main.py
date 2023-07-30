from gui import ApplicationGUI
from gps_sensor import new_gps_sensor
import os
from environment import (
    GPS_SENSOR_MODE,
    COLLAR_ID,
    USER_LOCATION_SIMULATION_ROUTE_PATH,
    PET_LOCATION_SIMULATION_ROUTE_PATH,
)

# TODO: add control to update the gps location of the pet and the user
# based on the gps sensor emulator and based on MQTT messages

# TODO: add control to start and stop recording of audio
# anyway, the control should send MQTT messages of the recorded audio


def absolute_path(relative_path: str) -> str:
    return os.path.join(os.path.dirname(__file__), relative_path)


def simulate_pet_location(gui: ApplicationGUI):
    pet_gps_sensor = new_gps_sensor(
        mode=GPS_SENSOR_MODE,
        interval_seconds=1,
        simulation_file_path=absolute_path(PET_LOCATION_SIMULATION_ROUTE_PATH),
    )
    pet_gps_sensor.on_new_location = gui.update_pet_gps_location

    pet_gps_sensor.start()


if __name__ == "__main__":
    gui = ApplicationGUI()

    user_gps_sensor = new_gps_sensor(
        mode=GPS_SENSOR_MODE,
        interval_seconds=1.2,
        simulation_file_path=absolute_path(USER_LOCATION_SIMULATION_ROUTE_PATH),
    )
    user_gps_sensor.on_new_location = gui.update_user_gps_location

    user_gps_sensor.start()

    # TODO: remove simulation of pet location
    if GPS_SENSOR_MODE == "SIMULATION":
        simulate_pet_location(gui=gui)

    # run gui
    gui.run()
