import paho.mqtt.client as mqtt
from paho_basic_callbacks import bind_callbacks
import time

broker = "broker.hivemq.com"
port = 1883

# create new client instance
client = mqtt.Client(client_id="IOT_PUB_313357402_YY_4545", clean_session=True)

bind_callbacks(client=client)
# set last will
client.will_set(
    topic="iot/home_YY/sensor_7402/lwt", payload="I am dead", qos=2, retain=False
)

# connect to broker
print("Connecting to broker ", broker)
client.connect(host=broker, port=port, keepalive=90)

topic_prefix = "iot/home_YY"

some_sensor_id = "7402"

sub_topic = f"{topic_prefix}/sensor_{some_sensor_id}"

message = "my message"

client.publish(topic=sub_topic, payload=message, qos=0, retain=False)

time.sleep(1)

client.disconnect()  # disconnect
print("End publish_client run script")
