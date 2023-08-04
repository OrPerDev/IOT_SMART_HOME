from enum import Enum

MQTT_BROKER_HOST = "broker.hivemq.com"
MQTT_BROKER_PORT = 1883

MQTT_SMART_COLLAR_SPEAKER_CLIENT_ID_PREFIX = "IOT_SMART_COLLAR_SPEAKER"

MQTT_COLLAR_TOPIC = "iot/SHAHARozaORus/smart_collar"


class TopicDataType(str, Enum):
    VOICE_MESSAGE = "voice_message"

    def __str__(self):
        return self.value
