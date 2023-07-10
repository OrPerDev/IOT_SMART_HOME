import paho.mqtt.client as mqtt
from paho_message_router import MessageRouter
from paho_basic_callbacks import bind_callbacks, _on_message
from typing import Any
from paho.mqtt.client import MQTTMessage
import time

broker = "broker.hivemq.com"
port = 1883

# create new client instance
client = mqtt.Client(client_id="IOT_SUB_313357402_YY_4545", clean_session=False)

mqtt_router = MessageRouter()

bind_callbacks(client=client)
client.on_message = mqtt_router.on_message
# connect to broker
print("Connecting to broker ", broker)
client.connect(host=broker, port=port, keepalive=90)

topic_prefix = "iot/home_YY"

some_sensor_id = "7402"

sub_topic = f"{topic_prefix}/sensor_{some_sensor_id}"


def sensor_topic_handler(client: Any, userdata: Any, msg: MQTTMessage):
    print("Sensor topic handler")
    print(msg.topic)
    # payload is a byte array
    # convert it to string
    decoded_message = str(msg.payload.decode("utf-8", "ignore"))
    print(decoded_message)


# Start loop
client.loop_start()

# subscribe to topic

# regular option:
client.subscribe(topic=sub_topic, qos=1)
mqtt_router.register(topic=sub_topic, callback=sensor_topic_handler)

time.sleep(5.0)
# Stop loop
client.loop_stop()
client.disconnect()
