import pytest
import mock
import paho.mqtt.client as mqtt
import uuid
import time
from paho_message_router import MessageRouter
from enum import Enum


class ClientType(str, Enum):
    SUB = "SUB"
    PUB = "PUB"


test_guid = uuid.uuid4()
test_ts = time.time_ns()

test_broker_url = "broker.hivemq.com"
test_broker_port = 1883
unique_test_sub_topic = f"paho_message_router/test/{test_guid}/{test_ts}"

client = mqtt.Client()


def sleep_until_call_count_is(func: mock.Mock, call_count: int, timeout: float = 3.0):
    # wait timeout seconds for the call count to be reached
    # if the call count is not reached, raise an exception
    start_time = time.time()
    while time.time() - start_time < timeout:
        if func.call_count == call_count:
            return
        time.sleep(0.1)


def get_client(c_type: ClientType) -> mqtt.Client:
    return mqtt.Client(
        # additional client id to avoid "mqtt's client take over"
        client_id=f"PAHO_MESSAGE_ROUTER_TEST_{c_type}_{test_guid}_{test_ts}_{uuid.uuid4()}",
        clean_session=True,
    )


def test_get_router():
    router = MessageRouter()
    assert isinstance(router, MessageRouter)


def test_register_throw_exception_when_callback_is_not_callable():
    router = MessageRouter()
    with pytest.raises(ValueError):
        router.register(topic="some_topic", callback="not_callable")  # type: ignore


def test_registered_callback_is_called_once():
    topic = f"{unique_test_sub_topic}/test_registered_callback_is_called_once"
    some_message = uuid.uuid1().bytes

    func = mock.Mock()

    # setup
    client_sub = get_client(ClientType.SUB)
    client_pub = get_client(ClientType.PUB)
    router = MessageRouter()

    client_sub.on_message = router.on_message
    client_sub.connect(test_broker_url, test_broker_port)
    client_sub.loop_start()
    client_sub.subscribe(topic=topic, qos=1)
    router.register(topic=topic, callback=func)

    client_pub.connect(test_broker_url, test_broker_port)
    client_pub.publish(topic=topic, payload=some_message, qos=1)

    # Here spefically we will use regular sleep, because we want to test
    # if the callback is called once and only once.
    time.sleep(3.0)

    # teardown
    client_sub.loop_stop()
    client_sub.disconnect()
    client_pub.disconnect()

    assert func.call_count == 1
    call_index = 0
    assert func.call_args[call_index][0] == client_sub
    msg_arg: mqtt.MQTTMessage = func.call_args[call_index][2]
    assert msg_arg.payload == some_message


def test_registered_callback_is_called_when_has_multiple():
    topic_1 = f"{unique_test_sub_topic}/test_registered_callback_is_called_when_has_multiple/1"
    topic_2 = f"{unique_test_sub_topic}/test_registered_callback_is_called_when_has_multiple/2"

    some_message_1 = uuid.uuid1().bytes
    some_message_2 = uuid.uuid1().bytes

    func_1 = mock.Mock()
    func_2 = mock.Mock()

    # setup
    client_sub = get_client(ClientType.SUB)
    client_pub = get_client(ClientType.PUB)
    router = MessageRouter()

    client_sub.on_message = router.on_message
    client_sub.connect(test_broker_url, test_broker_port)
    client_sub.loop_start()
    client_sub.subscribe(topic=topic_1, qos=1)
    router.register(topic=topic_1, callback=func_1)
    client_sub.subscribe(topic=topic_2, qos=1)
    router.register(topic=topic_2, callback=func_2)

    client_pub.connect(test_broker_url, test_broker_port)
    client_pub.publish(topic=topic_1, payload=some_message_1, qos=1)
    client_pub.publish(topic=topic_2, payload=some_message_2, qos=1)

    sleep_until_call_count_is(func=func_1, call_count=1)
    sleep_until_call_count_is(func=func_2, call_count=1)

    # teardown
    client_sub.loop_stop()
    client_sub.disconnect()
    client_pub.disconnect()

    assert func_1.call_count == 1
    call_index = 0
    assert func_1.call_args[call_index][0] == client_sub
    msg_arg: mqtt.MQTTMessage = func_1.call_args[call_index][2]
    assert msg_arg.payload == some_message_1

    assert func_2.call_count == 1
    call_index = 0
    assert func_2.call_args[call_index][0] == client_sub
    msg_arg: mqtt.MQTTMessage = func_2.call_args[call_index][2]
    assert msg_arg.payload == some_message_2


def test_registered_callback_is_called_when_has_hashtag_wildcard():
    base_topic = f"{unique_test_sub_topic}/test_registered_callback_is_called_when_has_hashtag_wildcard"
    pub_topic = f"{base_topic}/1/2/3/4/5/6/7/8/9/10"
    sub_topic = f"{base_topic}/#"
    some_message = uuid.uuid1().bytes

    func = mock.Mock()

    # setup
    client_sub = get_client(ClientType.SUB)
    client_pub = get_client(ClientType.PUB)
    router = MessageRouter()

    client_sub.on_message = router.on_message
    client_sub.connect(test_broker_url, test_broker_port)
    client_sub.loop_start()
    client_sub.subscribe(topic=sub_topic, qos=1)
    router.register(topic=sub_topic, callback=func)

    client_pub.connect(test_broker_url, test_broker_port)
    client_pub.publish(topic=pub_topic, payload=some_message, qos=1)

    sleep_until_call_count_is(func=func, call_count=1)

    # teardown
    client_sub.loop_stop()
    client_sub.disconnect()
    client_pub.disconnect()

    assert func.call_count == 1
    call_index = 0
    assert func.call_args[call_index][0] == client_sub
    msg_arg: mqtt.MQTTMessage = func.call_args[call_index][2]
    assert msg_arg.payload == some_message


def test_registered_callback_is_called_when_has_plus_wildcard():
    base_topic = f"{unique_test_sub_topic}/test_registered_callback_is_called_when_has_plus_wildcard"
    guid = uuid.uuid1()
    pub_topic = f"{base_topic}/bulbs/{guid}"
    sub_topic = f"{base_topic}/+/{guid}"
    some_message = uuid.uuid1().bytes

    func = mock.Mock()

    # setup
    client_sub = get_client(ClientType.SUB)
    client_pub = get_client(ClientType.PUB)
    router = MessageRouter()

    client_sub.on_message = router.on_message
    client_sub.connect(test_broker_url, test_broker_port)
    client_sub.loop_start()
    client_sub.subscribe(topic=sub_topic, qos=1)
    router.register(topic=sub_topic, callback=func)

    client_pub.connect(test_broker_url, test_broker_port)
    client_pub.publish(topic=pub_topic, payload=some_message, qos=1)

    sleep_until_call_count_is(func=func, call_count=1)

    # teardown
    client_sub.loop_stop()
    client_sub.disconnect()
    client_pub.disconnect()

    assert func.call_count == 1
    call_index = 0
    assert func.call_args[call_index][0] == client_sub
    msg_arg: mqtt.MQTTMessage = func.call_args[call_index][2]
    assert msg_arg.payload == some_message


def test_registered_callback_is_called_when_has_trailing_plus_wildcard():
    base_topic = f"{unique_test_sub_topic}/test_registered_callback_is_called_when_has_trailing_plus_wildcard"
    guid = uuid.uuid1()
    pub_topic = f"{base_topic}/bulbs/{guid}/{guid}"
    sub_topic = f"{base_topic}/bulbs/+/+"
    some_message = uuid.uuid1().bytes

    func = mock.Mock()

    # setup
    client_sub = get_client(ClientType.SUB)
    client_pub = get_client(ClientType.PUB)
    router = MessageRouter()

    client_sub.on_message = router.on_message
    client_sub.connect(test_broker_url, test_broker_port)
    client_sub.loop_start()
    client_sub.subscribe(topic=sub_topic, qos=1)
    router.register(topic=sub_topic, callback=func)

    client_pub.connect(test_broker_url, test_broker_port)
    client_pub.publish(topic=pub_topic, payload=some_message, qos=1)

    sleep_until_call_count_is(func=func, call_count=1)

    # teardown
    client_sub.loop_stop()
    client_sub.disconnect()
    client_pub.disconnect()

    assert func.call_count == 1
    call_index = 0
    assert func.call_args[call_index][0] == client_sub
    msg_arg: mqtt.MQTTMessage = func.call_args[call_index][2]
    assert msg_arg.payload == some_message


def test_registered_callback_is_called_when_has_plus_and_hashtag_wildcard():
    base_topic = f"{unique_test_sub_topic}/test_registered_callback_is_called_when_has_plus_and_hashtag_wildcard"
    guid = uuid.uuid1()
    pub_topic = f"{base_topic}/bulbs/{guid}/{guid}/{guid}/status"
    sub_topic = f"{base_topic}/+/+/+/#"
    some_message = uuid.uuid1().bytes

    func = mock.Mock()

    # setup
    client_sub = get_client(ClientType.SUB)
    client_pub = get_client(ClientType.PUB)
    router = MessageRouter()

    client_sub.on_message = router.on_message
    client_sub.connect(test_broker_url, test_broker_port)
    client_sub.loop_start()
    client_sub.subscribe(topic=sub_topic, qos=1)
    router.register(topic=sub_topic, callback=func)

    client_pub.connect(test_broker_url, test_broker_port)
    client_pub.publish(topic=pub_topic, payload=some_message, qos=1)

    sleep_until_call_count_is(func=func, call_count=1)

    # teardown
    client_sub.loop_stop()
    client_sub.disconnect()
    client_pub.disconnect()

    assert func.call_count == 1
    call_index = 0
    assert func.call_args[call_index][0] == client_sub
    msg_arg: mqtt.MQTTMessage = func.call_args[call_index][2]
    assert msg_arg.payload == some_message
    assert msg_arg.topic == pub_topic


def test_default_on_message_is_called_when_no_callback_is_registered():
    base_topic = f"{unique_test_sub_topic}/test_default_on_message_is_called_when_no_callback_is_registered"
    guid = uuid.uuid1()
    pub_topic = f"{base_topic}/bulbs/{guid}"
    sub_topic = f"{base_topic}/bulbs/{guid}"
    some_message = uuid.uuid1().bytes

    # here we use fallback func to know when the message was received
    fallback_func = mock.Mock()

    # setup
    client_sub = get_client(ClientType.SUB)
    client_pub = get_client(ClientType.PUB)
    router = MessageRouter()
    router.fallback_message_handler = fallback_func

    client_sub.on_message = router.on_message
    client_sub.connect(test_broker_url, test_broker_port)
    client_sub.loop_start()
    client_sub.subscribe(topic=sub_topic, qos=1)

    client_pub.connect(test_broker_url, test_broker_port)
    client_pub.publish(topic=pub_topic, payload=some_message, qos=1)

    sleep_until_call_count_is(func=fallback_func, call_count=1)

    # teardown
    client_sub.loop_stop()
    client_sub.disconnect()
    client_pub.disconnect()

    assert fallback_func.call_count == 1
    call_index = 0
    assert fallback_func.call_args[call_index][0] == client_sub
    msg_arg: mqtt.MQTTMessage = fallback_func.call_args[call_index][2]
    assert msg_arg.payload == some_message


def test_able_to_unregister_callback_and_no_longer_receive_messages():
    base_topic = f"{unique_test_sub_topic}/test_able_to_disable_callback"
    guid = uuid.uuid1()
    pub_topic = f"{base_topic}/bulbs/{guid}"
    sub_topic = f"{base_topic}/bulbs/{guid}"
    some_message = uuid.uuid1().bytes

    func = mock.Mock()
    fallback_func = mock.Mock()

    # setup
    client_sub = get_client(ClientType.SUB)
    client_pub = get_client(ClientType.PUB)
    router = MessageRouter()
    router.fallback_message_handler = fallback_func

    client_sub.on_message = router.on_message
    client_sub.connect(test_broker_url, test_broker_port)
    client_sub.loop_start()
    client_sub.subscribe(topic=sub_topic, qos=1)
    router.register(topic=sub_topic, callback=func)

    # unregister
    router.unregister(topic=sub_topic)

    client_pub.connect(test_broker_url, test_broker_port)
    client_pub.publish(topic=pub_topic, payload=some_message, qos=1)

    sleep_until_call_count_is(func=fallback_func, call_count=1)

    # teardown
    client_sub.loop_stop()
    client_sub.disconnect()
    client_pub.disconnect()

    assert func.call_count == 0
    assert fallback_func.call_count == 1
    call_index = 0
    assert fallback_func.call_args[call_index][0] == client_sub
    msg_arg: mqtt.MQTTMessage = fallback_func.call_args[call_index][2]
    assert msg_arg.payload == some_message
    assert msg_arg.topic == pub_topic


def test_clear_method_prevents_callback_from_being_called():
    base_topic = (
        f"{unique_test_sub_topic}/test_clear_method_prevents_callback_from_being_called"
    )
    guid = uuid.uuid1()
    pub_topic = f"{base_topic}/bulbs/{guid}"
    sub_topic = f"{base_topic}/bulbs/{guid}"
    some_message = uuid.uuid1().bytes

    # here we use fallback func to know when the message was received
    fallback_func = mock.Mock()
    func = mock.Mock()

    # setup
    client_sub = get_client(ClientType.SUB)
    client_pub = get_client(ClientType.PUB)
    router = MessageRouter()
    router.fallback_message_handler = fallback_func

    client_sub.on_message = router.on_message
    client_sub.connect(test_broker_url, test_broker_port)
    client_sub.loop_start()
    client_sub.subscribe(topic=sub_topic, qos=1)
    router.register(topic=sub_topic, callback=func)

    # clear the router
    router.clear()

    client_pub.connect(test_broker_url, test_broker_port)
    client_pub.publish(topic=pub_topic, payload=some_message, qos=1)

    sleep_until_call_count_is(func=fallback_func, call_count=1)

    # teardown
    client_sub.loop_stop()
    client_sub.disconnect()
    client_pub.disconnect()

    assert func.call_count == 0
