from gui import ApplicationGUI
from gps_sensor import new_gps_sensor, GPSMode
from audio import AudioDeviceController
from functools import partial
import os
from environment import (
    APPLICATION_GPS_SENSOR_CONFIG,
    PET_GPS_SENSOR_CONFIG,
    COLLAR_ID,
)


def absolute_path(relative_path: str) -> str:
    return os.path.join(os.path.dirname(__file__), relative_path)


def simulate_pet_location(gui: ApplicationGUI) -> None:
    if PET_GPS_SENSOR_CONFIG["mode"] != GPSMode.SIMULATION:
        return
    pet_gps_sensor = new_gps_sensor(**PET_GPS_SENSOR_CONFIG)
    pet_gps_sensor.on_new_location = gui.update_pet_gps_location

    pet_gps_sensor.start()


def send_audio_to_server(audio_controller: AudioDeviceController) -> None:
    audio: bytes = audio_controller.get_audio()
    print(audio)
    # TODO: send audio to server
    print("audio sent to server")


if __name__ == "__main__":
    gui = ApplicationGUI()

    # audio
    audio_controller = AudioDeviceController()
    # bind audio controller to gui events
    gui.on_start_recording_callback = audio_controller.start_recording
    gui.on_stop_recording_callback = audio_controller.stop_recording
    gui.on_send_record_command = partial(
        send_audio_to_server, audio_controller=audio_controller
    )
    gui.on_cancel_record_command = audio_controller.clear_frames

    # gps
    user_gps_sensor = new_gps_sensor(**APPLICATION_GPS_SENSOR_CONFIG)
    # bind gui to gps events
    user_gps_sensor.on_new_location = gui.update_user_gps_location
    # start gps sensor
    user_gps_sensor.start()

    # TODO: remove simulation of pet location
    simulate_pet_location(gui=gui)

    # run gui
    gui.run()
