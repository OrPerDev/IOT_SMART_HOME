from instant_mqtt_client import (
    InstantMQTTClient,
    MQTTClientBehaviorConfig,
    MQTTClientConfig,
    MQTTConnectionConfig,
    QualityOfService,
)
import time
import struct
import uuid
from constants import (
    MQTT_BROKER_HOST,
    MQTT_BROKER_PORT,
    MQTT_COLLAR_TOPIC,
    MQTT_COLLAR_LOCATION_CLIENT_ID_PREFIX,
)

client_id = f"{MQTT_COLLAR_LOCATION_CLIENT_ID_PREFIX}_{str(uuid.uuid4())}"

client = InstantMQTTClient(
    client_config=MQTTClientConfig(client_id=client_id, clean_session=True),
    connection_config=MQTTConnectionConfig(
        host=MQTT_BROKER_HOST, port=MQTT_BROKER_PORT, keepalive=90
    ),
    behavior_config=MQTTClientBehaviorConfig(
        listen_automatically=True,
    ),
)
collar_location_topic = f"{MQTT_COLLAR_TOPIC}/#"

client.connect()


def read_location(topic, payload, qos):
    location_len = len((0.0, 0.0))
    # restore structure
    unpacked_location = struct.unpack("%sf" % location_len, payload)
    # as tuple
    original_location = tuple(unpacked_location)
    print(original_location)


client.subscribe(topic=collar_location_topic, qos=1, on_message=read_location)

time.sleep(60)

client.disconnect()
