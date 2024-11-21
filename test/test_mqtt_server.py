import pytest
import paho.mqtt.client as mqtt
from unittest import TestCase


class TestMqttBroker(TestCase):
    def setUp(self):
        self.broker_ip = "20.164.18.107"
        self.broker_port = 1883
        self.topic = "test/topic"
        self.test_message = "Hello, MQTT!"

    def test_publish_message(self):

        client = mqtt.Client()
        try:
            client.connect(self.broker_ip, self.broker_port, 60)
            result = client.publish(self.topic, self.test_message)
            client.disconnect()

            assert result.rc == mqtt.MQTT_ERR_SUCCESS
        except Exception as e:
            pytest.fail(f"Failed to connect to MQTT broker: {str(e)}")

    def test_subscribe_message(self):

        received_messages = []

        def on_message(client, userdata, msg):
            received_messages.append(msg.payload.decode())

        client = mqtt.Client()
        client.on_message = on_message

        try:
            client.connect(self.broker_ip, self.broker_port, 60)
            client.subscribe(self.topic)
            client.loop_start()

            # Publish a test message that we'll receive back
            client.publish(self.topic, self.test_message)

            # Wait briefly for message to be received
            import time

            time.sleep(2)

            client.loop_stop()
            client.disconnect()

            assert self.test_message in received_messages
        except Exception as e:
            pytest.fail(f"Failed to connect to MQTT broker: {str(e)}")
