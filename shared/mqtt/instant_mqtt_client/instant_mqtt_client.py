from __future__ import annotations
from typing import Callable, Any, Protocol
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties as MQTTProperties
from threading import Thread, Lock
from enum import Enum
from dataclasses import dataclass, asdict
import paho_basic_callbacks
from paho_message_router import (
    MessageRouter,
    OnMessageCallback as RouterOnMessageCallback,
)


class OnMessageCallback(Protocol):
    def __call__(
        self,
        topic: str,
        payload: bytes,
        qos: QualityOfService,
        properties: MQTTProperties | None,
    ) -> None:
        pass


class QualityOfService(int, Enum):
    AT_MOST_ONCE = 0
    AT_LEAST_ONCE = 1
    EXACTLY_ONCE = 2


@dataclass(frozen=True)
class ConnectionConfig:
    host: str
    port: int = 1883
    keepalive: int = 60
    bind_address: str = ""
    bind_port: int = 0
    clean_start: int = 3
    properties: MQTTProperties | None = None


@dataclass(frozen=True)
class ClientConfig:
    client_id: str | None = ""
    clean_session: bool | None = None
    userdata: Any = None
    protocol: int = mqtt.MQTTv311
    transport: str = "tcp"


class InstantMQTTClient(mqtt.Client):
    def __init__(
        self,
        connection_config: ConnectionConfig,
        client_config: ClientConfig,
        listen_automatically: bool = False,
    ) -> None:
        super().__init__(**asdict(client_config))
        # set callbacks
        self.on_log = paho_basic_callbacks.on_log
        self.on_connect = paho_basic_callbacks.on_connect
        self.on_disconnect = paho_basic_callbacks.on_disconnect
        self.router = MessageRouter()
        self.on_message = self.router.on_message

        # connect
        self.connect(**asdict(connection_config))

        # listen
        self.loop_thread = None
        self.loop_is_running = False
        self.loop_lock = Lock()
        if listen_automatically:
            self.start_listen()

    def start_listen(self) -> None:
        with self.loop_lock:
            if self.loop_is_running:
                return
            self.loop_thread = Thread(target=super().loop_start)
            self.loop_thread.start()
            self.loop_is_running = True

    def stop_listen(self) -> None:
        with self.loop_lock:
            if not self.loop_is_running:
                return
            super().loop_stop()
            if self.loop_thread is not None:
                self.loop_thread.join()
            self.loop_is_running = False

    def _transform_on_message(
        self, on_message: OnMessageCallback
    ) -> RouterOnMessageCallback:
        def callback(client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage) -> None:
            kwargs = {
                "topic": msg.topic,
                "payload": msg.payload,
                "qos": msg.qos,
            }
            if hasattr(msg, "properties"):
                kwargs["properties"] = msg.properties
            on_message(**kwargs)

        return callback

    def subscribe(
        self,
        topic: str,
        qos: QualityOfService,
        on_message: OnMessageCallback,
        options: mqtt.SubscribeOptions | None = None,
        properties: MQTTProperties | None = None,
    ) -> tuple[int, int]:
        result: tuple[int, int] = super().subscribe(
            topic=topic, qos=qos, options=options, properties=properties,
        )
        if result[0] != mqtt.MQTT_ERR_SUCCESS:
            return result
        self.router.register(
            topic=topic, callback=self._transform_on_message(on_message)
        )
        return result

    def unsubscribe(
        self, topic: str, properties: MQTTProperties | None = None,
    ) -> tuple[int, int]:
        result: tuple[int, int] = super().unsubscribe(
            topic=topic, properties=properties,
        )
        if result[0] != mqtt.MQTT_ERR_SUCCESS:
            return result
        self.router.unregister(topic=topic)
        return result

    def disconnect(self) -> int:
        self.stop_listen()
        return super().disconnect()
