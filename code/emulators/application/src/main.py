from typing import Optional
from common.structs import AudioRecord
from gui import ApplicationGUI
from gps_sensor import new_gps_sensor
from audio import AudioDeviceController
from dal.audio import AudioRecordRepository
from network_interface import NetworkInterface
from functools import partial
from common.environment import (
    APPLICATION_GPS_SENSOR_CONFIG,
    COLLAR_ID,
)


def send_audio_to_server(
    audio_record_repository: AudioRecordRepository,
    audio_controller: AudioDeviceController,
    network_interface: NetworkInterface,
    record: Optional[AudioRecord] = None,
):
    if record is None:
        audio: bytes = audio_controller.get_audio()
    else:
        if record.id is None:
            raise ValueError("Record id is None, cannot send to server")
        record = audio_record_repository.get_record(record_id=record.id)
        audio = record.audio_data

    print("Sending audio to server")
    network_interface.on_send_voice_message(audio)


def save_audio_record(
    audio_record_repository: AudioRecordRepository,
    audio_controller: AudioDeviceController,
    record: Optional[AudioRecord] = None,
):
    if record is None:
        audio: bytes = audio_controller.get_audio()
        record = AudioRecord(audio_data=audio)
    else:
        if record.id is None:
            raise ValueError("Record id is None, cannot send to server")
        record = audio_record_repository.get_record(record_id=record.id)
        audio = record.audio_data

    print(f"Saving audio record {record.name} to database")

    audio_record_repository.store_record(record=record)


def delete_audio_record(
    audio_record_repository: AudioRecordRepository,
    record: AudioRecord,
):
    print(f"Deleting audio record {record.name} from database")

    audio_record_repository.delete_record(record=record)


if __name__ == "__main__":
    gui = ApplicationGUI()

    # network interface (mqtt)
    network_interface = NetworkInterface(collar_id=COLLAR_ID)
    network_interface.on_new_gps_location = gui.update_pet_gps_location
    network_interface.start()

    # dal
    audio_record_repository = AudioRecordRepository()

    # audio
    audio_controller = AudioDeviceController()

    # bind dal to gui events
    gui.on_save_audio_record_callback = partial(
        save_audio_record,
        audio_record_repository=audio_record_repository,
        audio_controller=audio_controller,
    )
    gui.on_delete_audio_record_callback = audio_record_repository.delete_record
    gui.on_send_existing_audio_record_callback = partial(
        send_audio_to_server,
        audio_record_repository=audio_record_repository,
        audio_controller=audio_controller,
        network_interface=network_interface,
    )
    gui.on_update_audio_record_name_callback = (
        audio_record_repository.update_record_name
    )
    gui.on_fetch_audio_records_callback = audio_record_repository.get_records

    # bind audio controller to gui events
    gui.on_start_recording_callback = audio_controller.start_recording
    gui.on_stop_recording_callback = audio_controller.stop_recording
    gui.on_send_record_command = partial(
        send_audio_to_server,
        audio_record_repository=audio_record_repository,
        audio_controller=audio_controller,
        network_interface=network_interface,
    )
    gui.on_delete_record_command = partial(
        delete_audio_record,
        audio_record_repository=audio_record_repository,
    )

    # gps
    user_gps_sensor = new_gps_sensor(**APPLICATION_GPS_SENSOR_CONFIG)
    # bind gui to gps events
    user_gps_sensor.on_new_location = gui.update_user_gps_location
    # start gps sensor
    user_gps_sensor.start()

    # run gui
    gui.run()

    network_interface.stop()
