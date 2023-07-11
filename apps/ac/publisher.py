from instant_mqtt_client import (
    InstantMQTTClient,
    ConnectionConfig,
    ClientConfig,
    QualityOfService,
)
import time

broker = "broker.hivemq.com"
port = 1883

client = InstantMQTTClient(
    client_config=ClientConfig(
        client_id="IOT_PUB_313357402_YY_4545", clean_session=True
    ),
    connection_config=ConnectionConfig(host=broker, port=port, keepalive=90),
)
client.connect()

# set last will
client.will_set(
    topic="iot/home_YY/sensor_7402/lwt",
    payload="I am dead",
    qos=QualityOfService.EXACTLY_ONCE,
    retain=False,
)

topic_prefix = "iot/home_YY"

some_sensor_id = "7402"

sub_topic = f"{topic_prefix}/sensor_{some_sensor_id}"

message = "my message"

client.publish(
    topic=sub_topic, payload=message, qos=QualityOfService.AT_MOST_ONCE, retain=False
)

time.sleep(1)

client.disconnect()
