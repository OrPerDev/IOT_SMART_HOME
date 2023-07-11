from instant_mqtt_client import (
    InstantMQTTClient,
    ConnectionConfig,
    ClientConfig,
    MQTTProperties,
)
import time

broker = "broker.hivemq.com"
port = 1883

client = InstantMQTTClient(
    client_config=ClientConfig(
        client_id="IOT_SUB_313357402_YY_4545", clean_session=False
    ),
    connection_config=ConnectionConfig(host=broker, port=port, keepalive=90),
    listen_automatically=True,
)

topic_prefix = "iot/home_YY"

some_sensor_id = "7402"

sub_topic = f"{topic_prefix}/sensor_{some_sensor_id}"


def sensor_topic_handler(
    topic: str, payload: bytes, qos: int, properties: MQTTProperties | None = None
):
    print("Sensor topic handler")
    print(topic)
    # payload is a byte array
    # convert it to string
    decoded_message = str(payload.decode("utf-8", "ignore"))
    print(decoded_message)


client.subscribe(topic=sub_topic, qos=1, on_message=sensor_topic_handler)

time.sleep(5.0)

client.disconnect()
