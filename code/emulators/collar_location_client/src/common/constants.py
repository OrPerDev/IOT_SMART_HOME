from enum import Enum

MQTT_BROKER_HOST = "broker.hivemq.com"
MQTT_BROKER_PORT = 1883

MQTT_COLLAR_TOPIC = "iot/SHAHARozaORus/smart_collar"

MQTT_COLLAR_LOCATION_CLIENT_ID_PREFIX = "IOT_SMART_COLLAR_LOCATION"


class TopicDataType(str, Enum):
    LOCATION = "location"

    def __str__(self):
        return self.value
