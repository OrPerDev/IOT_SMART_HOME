from audio import AudioDeviceController
from functools import partial
import time
from network_interface import NetworkInterface
from common.environment import (
    COLLAR_ID,
)


def play_voice_message(
    audio_controller: AudioDeviceController, voice_message: bytes | None
) -> None:
    if voice_message is None:
        print("Empty voice message received")
        return

    print("Playing voice message")
    audio_controller.play_audio(audio_data=voice_message)


if __name__ == "__main__":
    audio_controller = AudioDeviceController()
    network_interface = NetworkInterface(collar_id=COLLAR_ID)

    network_interface.on_new_voice_message = partial(
        play_voice_message, audio_controller=audio_controller
    )
    network_interface.start()

    while True:
        time.sleep(5)
