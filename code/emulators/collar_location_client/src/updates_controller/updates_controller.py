from instant_mqtt_client import (
    InstantMQTTClient,
    MQTTClientBehaviorConfig,
    MQTTClientConfig,
    MQTTConnectionConfig,
    QualityOfService,
)
import struct
import uuid
from constants import (
    MQTT_BROKER_HOST,
    MQTT_BROKER_PORT,
    MQTT_COLLAR_TOPIC,
    MQTT_COLLAR_LOCATION_CLIENT_ID_PREFIX,
)


class UpdatesController:
    def __init__(self, collar_id: str):
        self.collar_id = collar_id

        client_id = f"{MQTT_COLLAR_LOCATION_CLIENT_ID_PREFIX}_{str(uuid.uuid4())}"

        self.client = InstantMQTTClient(
            client_config=MQTTClientConfig(client_id=client_id, clean_session=True),
            connection_config=MQTTConnectionConfig(
                host=MQTT_BROKER_HOST, port=MQTT_BROKER_PORT, keepalive=90
            ),
            behavior_config=MQTTClientBehaviorConfig(
                listen_automatically=False,
            ),
        )

        self.collar_location_topic = f"{MQTT_COLLAR_TOPIC}/{self.collar_id}/location"

        self.client.connect()

    def on_gps_location_update(self, location: tuple[float, float] | None) -> None:
        if location is None:
            return
        buf = struct.pack("%sf" % len(location), *location)
        self.client.publish(
            topic=self.collar_location_topic,
            payload=buf,
            qos=QualityOfService.AT_LEAST_ONCE,
            # Remember the last location in case the client missed it
            retain=True,
        )
