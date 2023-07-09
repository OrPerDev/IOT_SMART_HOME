import paho.mqtt.client as mqtt  # import the client1
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
    print("message received: ", m_decode)


# create new client instance
client = mqtt.Client(client_id="IOT_PUB_313357402_YY_4545", clean_session=True)

# bind call back functions
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_log = on_log
client.on_message = on_message
# # set last will
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
