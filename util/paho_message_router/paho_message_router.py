from __future__ import annotations
from typing import Any
import paho.mqtt.client as mqtt
from typing import Protocol


class OnMessageCallback(Protocol):
    def __call__(
        self, client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage
    ) -> None:
        pass


def default_fallback_message_handler(
    client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage
) -> None:
    print(
        f"Received message on unregistered topic subscription: {msg.topic} - {msg.payload}"
    )


class MessageRouter:
    def __init__(self) -> None:
        self.callback_by_topic = {}
        self._fallback_message_handler = default_fallback_message_handler

    def register(self, topic: str, callback: OnMessageCallback) -> None:
        if not callable(callback):
            raise ValueError("callback must be callable")
        self.callback_by_topic[topic] = callback

    def unregister(self, topic: str) -> None:
        if topic in self.callback_by_topic:
            del self.callback_by_topic[topic]

    def clear(self) -> None:
        self.callback_by_topic = {}

    @property
    def fallback_message_handler(self) -> OnMessageCallback:
        return self._fallback_message_handler

    @fallback_message_handler.setter
    def fallback_message_handler(self, callback: OnMessageCallback) -> None:
        self._fallback_message_handler = callback

    def on_message(
        self, client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage
    ) -> None:
        callback = self._route_topic_to_callback(msg.topic)
        callback(client, userdata, msg)

    def _route_topic_to_callback(self, topic: str) -> OnMessageCallback:
        # explicit
        if topic in self.callback_by_topic:
            return self.callback_by_topic[topic]

        # wildcard
        for candiate_topic in self.callback_by_topic:
            if mqtt.topic_matches_sub(candiate_topic, topic):
                return self.callback_by_topic[candiate_topic]

        # fallback
        return self.fallback_message_handler
