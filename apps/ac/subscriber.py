import paho.mqtt.client as mqtt  # import the client1
from paho_message_router import MessageRouter
from typing import Any
from paho.mqtt.client import MQTTMessage
import time

broker = "broker.hivemq.com"
port = 1883


def on_log(client, userdata, level, buf):
    print("log: " + buf)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print("DisConnected result code " + str(rc))


def on_message(client, userdata, msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    print("Now message received: ", m_decode)
    print("It was topic: ", topic)


# create new client instance
client = mqtt.Client(client_id="IOT_SUB_313357402_YY_4545", clean_session=False)

mqtt_router = MessageRouter()

# bind call back function
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_log = on_log
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
