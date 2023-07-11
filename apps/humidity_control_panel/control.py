from instant_mqtt_client import (
    InstantMQTTClient,
    MQTTClientBehaviorConfig,
    MQTTClientConfig,
    MQTTConnectionConfig,
    MQTTProperties,
    QualityOfService,
)
from typing import Protocol, Callable
import uuid

broker = "broker.hivemq.com"
port = 1883
sensor_topics_prefix = "iot/home/313357402/YY"


class GUI(Protocol):
    def update_humidity_level(self, level: float) -> None:
        ...

    @property
    def on_adjust_humidiy_call(self) -> Callable:
        ...

    @on_adjust_humidiy_call.setter
    def on_adjust_humidiy_call(self, callback: Callable):
        ...


class HumidityController:
    def __init__(self, gui: GUI, humidity_sensor_id: str, pump_id: str):
        self.gui = gui
        self.gui.on_adjust_humidiy_call = self.on_adjust_humidity_call

        self.humidity_sensor_id = humidity_sensor_id
        self.pump_id = pump_id

        client_id = f"IOT_313357402_YY_{str(uuid.uuid4())}"

        self.client = InstantMQTTClient(
            client_config=MQTTClientConfig(client_id=client_id, clean_session=True),
            connection_config=MQTTConnectionConfig(
                host=broker, port=port, keepalive=90
            ),
            behavior_config=MQTTClientBehaviorConfig(listen_automatically=True,),
        )

        self.humidity_sensor_status_topic = (
            f"{sensor_topics_prefix}/humidity_sensor_{self.humidity_sensor_id}/status"
        )

        self.pump_control_topic = f"{sensor_topics_prefix}/pump_{self.pump_id}/control"

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def __del__(self):
        self.stop()

    def start(self):
        self.client.connect()
        self.client.subscribe(
            topic=self.humidity_sensor_status_topic,
            qos=QualityOfService.AT_MOST_ONCE,
            on_message=self.on_sensor_status_update,
        )

    def stop(self):
        self.client.unsubscribe(self.humidity_sensor_status_topic)
        self.client.disconnect()

    def on_adjust_humidity_call(self):
        message = "1"
        self.client.publish(
            topic=self.pump_control_topic,
            payload=message,
            qos=QualityOfService.AT_LEAST_ONCE,
            retain=False,
        )

    def on_sensor_status_update(
        self,
        topic: str,
        payload: bytes,
        qos: int,
        properties: MQTTProperties | None = None,
    ):
        print("Sensor topic handler")
        # payload is a byte array, convert it to string
        decoded_message = str(payload.decode("utf-8", "ignore"))
        # data is just the humidity level
        humidity_level = float(decoded_message)
        self.gui.update_humidity_level(humidity_level)
