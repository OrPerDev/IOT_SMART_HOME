from typing import Protocol, Optional
from instant_mqtt_client import (
    InstantMQTTClient,
    MQTTClientBehaviorConfig,
    MQTTClientConfig,
    MQTTConnectionConfig,
    QualityOfService,
    MQTTProperties,
)
import struct
import uuid
from common.constants import (
    MQTT_BROKER_HOST,
    MQTT_BROKER_PORT,
    MQTT_COLLAR_TOPIC,
    MQTT_SMART_COLLAR_APP_CLIENT_ID_PREFIX,
    TopicDataType,
)


class OnNewGPSLocationCallback(Protocol):
    def __call__(self, location: tuple[float, float] | None) -> None:
        ...


def unpack_mqtt_message_location(payload: bytes):
    location_len = len((0.0, 0.0))
    # restore structure
    unpacked_location = struct.unpack("%sf" % location_len, payload)
    # as tuple
    original_location = tuple(unpacked_location)
    return original_location


class NetworkInterface:
    def __init__(self, collar_id: str):
        self.collar_id = collar_id

        client_id = f"{MQTT_SMART_COLLAR_APP_CLIENT_ID_PREFIX}_{str(uuid.uuid4())}"

        self.client = InstantMQTTClient(
            client_config=MQTTClientConfig(client_id=client_id, clean_session=True),
            connection_config=MQTTConnectionConfig(
                host=MQTT_BROKER_HOST, port=MQTT_BROKER_PORT, keepalive=90
            ),
            behavior_config=MQTTClientBehaviorConfig(
                listen_automatically=True,
            ),
        )

        self.collar_location_topic = (
            f"{MQTT_COLLAR_TOPIC}/{self.collar_id}/{TopicDataType.LOCATION}"
        )

        self.collar_voice_message_topic = (
            f"{MQTT_COLLAR_TOPIC}/{self.collar_id}/{TopicDataType.VOICE_MESSAGE}"
        )

        self._on_new_gps_location = lambda location: print(
            f"New GPS location: {location}"
        )

    @property
    def on_new_gps_location(self) -> OnNewGPSLocationCallback:
        return self._on_new_gps_location

    @on_new_gps_location.setter
    def on_new_gps_location(self, callback: OnNewGPSLocationCallback):
        self._on_new_gps_location = callback

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        self.client.connect()
        self.client.subscribe(
            topic=self.collar_location_topic,
            qos=QualityOfService.AT_LEAST_ONCE,
            on_message=self.on_gps_location_update,
        )

    def stop(self):
        self.client.disconnect()

    def on_gps_location_update(
        self,
        topic: str,
        payload: bytes,
        qos: QualityOfService,
        properties: Optional[MQTTProperties | None] = None,
    ):
        if payload is None:
            return

        self._on_new_gps_location(
            location=unpack_mqtt_message_location(payload=payload)
        )

    def on_send_voice_message(self, voice_message: bytes) -> None:
        self.client.publish(
            topic=self.collar_voice_message_topic,
            payload=voice_message,
            qos=QualityOfService.EXACTLY_ONCE,
            retain=False,
        )
