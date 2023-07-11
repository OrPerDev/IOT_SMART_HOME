import paho.mqtt.client as mqtt
from typing import Any
import logging

formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger('MQTT Client')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def transform_mqtt_log_level_to_logging_log_level(level: int) -> int:
    if level == mqtt.MQTT_LOG_INFO:
        return logging.INFO
    elif level == mqtt.MQTT_LOG_NOTICE:
        return logging.INFO
    elif level == mqtt.MQTT_LOG_WARNING:
        return logging.WARNING
    elif level == mqtt.MQTT_LOG_ERR:
        return logging.ERROR
    elif level == mqtt.MQTT_LOG_DEBUG:
        return logging.DEBUG
    else:
        return logging.INFO


def on_log(
    client: mqtt.Client, userdata: Any, level: int, buf: str
) -> None:
    level = transform_mqtt_log_level_to_logging_log_level(level=level)
    logger.log(level, buf)


def on_connect(
    client: mqtt.Client, userdata: Any, flags: dict, rc: int
) -> None:
    if rc == mqtt.MQTT_ERR_SUCCESS:
        logger.info("connected OK")
    else:
        logger.error("Bad connection Returned code=", rc)


def on_disconnect(
    client: mqtt.Client, userdata: Any, rc: int = mqtt.MQTT_ERR_SUCCESS
) -> None:
    if rc == mqtt.MQTT_ERR_SUCCESS:
        logger.info("Gracefully disconnected")
    else:
        logger.error("Unexpected disconnection. Returned code=", rc)


def on_message(
    client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage
) -> None:
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    logger.info("Now message received: %s", m_decode)
    logger.info("It was topic: %s", topic)
