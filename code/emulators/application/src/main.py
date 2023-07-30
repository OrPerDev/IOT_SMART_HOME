from gui import ApplicationGUI
from gps_sensor import GPSSensor
from enum import Enum
import threading
import time
import os
from environment import MODE, COLLAR_ID, USER_LOCATION_SIMULATION_ROUTE_PATH

# TODO: add control to update the gps location of the pet and the user
# based on the gps sensor emulator and based on MQTT messages

# TODO: add control to start and stop recording of audio
# anyway, the control should send MQTT messages of the recorded audio


class Mode(str, Enum):
    SIMULATION = "SIMULATION"
    AUTHENTIC = "AUTHENTIC"


def absolute_path(relative_path: str) -> str:
    return os.path.join(os.path.dirname(__file__), relative_path)


# TODO: remove this function as it will be replaced with the MQTT client messages
def simulate_pet_location_updates(gui: ApplicationGUI) -> None:
    route = [
        (32.01487634797979, 34.77458326803195),
        (32.0149811, 34.7746679),
        (32.0149265, 34.7744101),
        (32.0149538, 34.7740843),
        (32.0150098, 34.7738474),
        (32.0151482, 34.7735293),
        (32.0154941, 34.7735227),
        (32.0152926, 34.7752523),
        (32.0149419, 34.7751958),
        (32.0140609, 34.7750401),
        (32.0139772, 34.7750268),
        (32.0133498, 34.7749273),
        (32.0131406, 34.7748846),
        (32.0129575, 34.7748507),
        (32.0129424, 34.7749537),
        (32.0129288, 34.7750458),
        (32.0128716, 34.7753262),
        (32.0127684, 34.7758322),
        (32.0122001, 34.7778245),
        (32.0121043, 34.7781604),
        (32.012074, 34.7782996),
        (32.0119908, 34.7786277),
        (32.0116604, 34.7799067),
        (32.0112819, 34.7814543),
        (32.011264, 34.7815245),
        (32.0111919, 34.7818071),
        (32.0111788, 34.7818546),
        (32.0111394, 34.7820157),
        (32.0104797, 34.7847098),
        (32.0103897, 34.7850239),
        (32.0101513, 34.785),
        (32.0096797, 34.784959),
        (32.0088765, 34.7848893),
        (32.0081654, 34.7848077),
        (32.0081482, 34.7848055),
        (32.0078615, 34.7847688),
        (32.0078172, 34.7847637),
        (32.0072011, 34.7846925),
        (32.0059571, 34.7845489),
        (32.0047067, 34.7899158),
    ]
    for point in route:
        gui.update_pet_gps_location(point)
        time.sleep(1)


def simulate_user_gps_location_sensor_updates(gps_sensor: GPSSensor) -> None:
    with open(absolute_path(USER_LOCATION_SIMULATION_ROUTE_PATH), "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            # line is float,float
            location = tuple([float(val.strip()) for val in line.strip().split(",")])
            if len(location) != 2:
                raise RuntimeError(f"Invalid GPS location line: {line}")
            print(f"[Simulation]: Producing new user location: {location}")
            gps_sensor.set_location(location=location)
            time.sleep(1.2)


if __name__ == "__main__":
    gui = ApplicationGUI()

    gps_sensor = GPSSensor(interval_seconds=1)
    gps_sensor.on_new_location = gui.update_user_gps_location

    if MODE == Mode.AUTHENTIC:
        print("Authentic Mode Start")
        # let the gps sensor handle it natively
        gps_sensor.start()
    elif MODE == Mode.SIMULATION:
        # run simulation
        print("Simulation Mode Start")
        threading.Thread(
            target=simulate_user_gps_location_sensor_updates, args=(gps_sensor,)
        ).start()
        threading.Thread(target=simulate_pet_location_updates, args=(gui,)).start()
    else:
        raise EnvironmentError(f"Unsupported script mode: {MODE}")

    # run gui
    gui.run()
