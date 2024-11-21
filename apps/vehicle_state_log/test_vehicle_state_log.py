import unittest
import paho.mqtt.client as mqtt
import json
import time
import os
from unittest.mock import patch, MagicMock
from vehicle_state_log import callback, logger

# Mock the Ankaios class
# Mock the Ankaios class
class MockAnkaios:
    def __init__(self):
        self.state = {
            "workload_states": [
                {"workload_id": "1", "state": "RUNNING"},
                {"workload_id": "2", "state": "STOPPED"}
            ]
        }

    def get_state(self, field_masks=None):
        return MagicMock(to_dict=lambda: self.state)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

# Mock the MQTT client
class MockMQTTClient:
    def __init__(self):
        self.published_messages = []

    def publish(self, topic, payload):
        self.published_messages.append((topic, payload))

    def connect(self, broker, port, keepalive):
        pass  # No real connection is made

    def loop_forever(self):
        pass

class TestVehicleStateLog(unittest.TestCase):
    def setUp(self):
        # Set environment variables
        os.environ['MQTT_BROKER_ADDR'] = 'localhost'
        os.environ['MQTT_BROKER_PORT'] = '1883'
        os.environ['VIN'] = 'test_vin'
        os.environ['INTERVAL'] = '1'

        # Mock the Ankaios class
        self.ankaios_mock = MockAnkaios()

        # Mock the MQTT client
        self.mqtt_client_mock = MockMQTTClient()

        # Patch the Ankaios     and MQTT client
        self.ankaios_patch = patch('vehicle_state_log.Ankaios', return_value=self.ankaios_mock)
        self.mqtt_client_patch = patch('vehicle_state_log.mqtt.Client', return_value=self.mqtt_client_mock)

        self.ankaios_patch.start()
        self.mqtt_client_patch.start()

    def tearDown(self):
        self.ankaios_patch.stop()
        self.mqtt_client_patch.stop()

    def test_callback(self):
        # Test data
        topic_name = "vehicle_dynamics"
        msg = '{"speed": 60, "direction": "north"}'
        timestamp = time.time()

        # Call the callback function
        callback(topic_name, msg, timestamp)

        # Check if the message was published correctly
        expected_payload = {
            "speed": 60,
            "direction": "north",
            "workload_states": [
                {"workload_id": "1", "state": "RUNNING"},
                {"workload_id": "2", "state": "STOPPED"}
            ],
            "vehicle_id": "test_vin"
        }

        # Verify the published message
        self.assertEqual(len(self.mqtt_client_mock.published_messages), 1)
        topic, payload = self.mqtt_client_mock.published_messages[0]
        self.assertEqual(topic, "vehicle/vehicle_dynamics")
        self.assertEqual(json.loads(payload), expected_payload)

if __name__ == '__main__':
    unittest.main()
