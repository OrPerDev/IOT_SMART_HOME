from gui import ApplicationGUI
from gps_sensor import new_gps_sensor
from audio import AudioDeviceController
from network_interface import NetworkInterface
from functools import partial
from common.environment import (
    APPLICATION_GPS_SENSOR_CONFIG,
    COLLAR_ID,
)


def send_audio_to_server(
    audio_controller: AudioDeviceController, network_interface: NetworkInterface
):
    audio: bytes = audio_controller.get_audio()
    print("Sending audio to server")
    network_interface.on_send_voice_message(audio)


if __name__ == "__main__":
    gui = ApplicationGUI()

    # network interface (mqtt)
    network_interface = NetworkInterface(collar_id=COLLAR_ID)
    network_interface.on_new_gps_location = gui.update_pet_gps_location
    network_interface.start()

    # audio
    audio_controller = AudioDeviceController()
    # bind audio controller to gui events
    gui.on_start_recording_callback = audio_controller.start_recording
    gui.on_stop_recording_callback = audio_controller.stop_recording
    gui.on_send_record_command = partial(
        send_audio_to_server,
        audio_controller=audio_controller,
        network_interface=network_interface,
    )
    gui.on_cancel_record_command = audio_controller.clear_frames

    # gps
    user_gps_sensor = new_gps_sensor(**APPLICATION_GPS_SENSOR_CONFIG)
    # bind gui to gps events
    user_gps_sensor.on_new_location = gui.update_user_gps_location
    # start gps sensor
    user_gps_sensor.start()

    # run gui
    gui.run()

    network_interface.stop()
