from typing import Protocol, Optional
from instant_mqtt_client import (
    InstantMQTTClient,
    MQTTClientBehaviorConfig,
    MQTTClientConfig,
    MQTTConnectionConfig,
    QualityOfService,
    MQTTProperties,
)
import uuid
from common.constants import (
    MQTT_BROKER_HOST,
    MQTT_BROKER_PORT,
    MQTT_COLLAR_TOPIC,
    MQTT_SMART_COLLAR_SPEAKER_CLIENT_ID_PREFIX,
    TopicDataType,
)


class OnNewVoiceMessageCallback(Protocol):
    def __call__(self, voice_message: bytes | None) -> None:
        ...


class NetworkInterface:
    def __init__(self, collar_id: str):
        self.collar_id = collar_id

        client_id = f"{MQTT_SMART_COLLAR_SPEAKER_CLIENT_ID_PREFIX}_{str(uuid.uuid4())}"

        self.client = InstantMQTTClient(
            client_config=MQTTClientConfig(client_id=client_id, clean_session=True),
            connection_config=MQTTConnectionConfig(
                host=MQTT_BROKER_HOST, port=MQTT_BROKER_PORT, keepalive=90
            ),
            behavior_config=MQTTClientBehaviorConfig(
                listen_automatically=True,
            ),
        )

        self.collar_voice_message_topic = (
            f"{MQTT_COLLAR_TOPIC}/{self.collar_id}/{TopicDataType.VOICE_MESSAGE}"
        )

        self._on_new_voice_mesage = lambda voice_message: print(
            f"New voice message: {voice_message}"
        )

    @property
    def on_new_voice_message(self) -> OnNewVoiceMessageCallback:
        return self._on_new_voice_mesage

    @on_new_voice_message.setter
    def on_new_voice_message(self, callback: OnNewVoiceMessageCallback):
        self._on_new_voice_mesage = callback

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        self.client.connect()
        self.client.subscribe(
            topic=self.collar_voice_message_topic,
            qos=QualityOfService.EXACTLY_ONCE,
            on_message=self.on_voice_message,
        )

    def stop(self):
        self.client.disconnect()

    def on_voice_message(
        self,
        topic: str,
        payload: bytes,
        qos: QualityOfService,
        properties: Optional[MQTTProperties | None] = None,
    ):
        if payload is None:
            return

        self._on_new_voice_mesage(voice_message=payload)
