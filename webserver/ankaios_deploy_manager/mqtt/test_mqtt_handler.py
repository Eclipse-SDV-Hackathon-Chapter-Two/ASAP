import unittest
from unittest.mock import MagicMock, patch
from ankaios_deploy_manager.mqtt.mqtt_handler import MqttHandler, VEHICLE_DYNAMICS_TOPIC, REMOVE_DATA_TOPIC
import json

class TestMqttHandler(unittest.TestCase):

    def setUp(self):
        # Mock the logger to avoid printing logs during tests
        self.mock_logger = MagicMock()
        MqttHandler.logger = self.mock_logger

        # Initialize the MQTTHandler
        MqttHandler.client = MagicMock()
        MqttHandler.client.on_connect = MqttHandler.on_connect
        MqttHandler.client.on_message = MqttHandler.on_message

    def test_on_update_data(self):
        # Mock the MQTT message payload
        payload = json.dumps({'vehicle_id': '123', 'speed': 100}).encode('ascii')

        # Call the on_update_data method
        MqttHandler.on_update_data(payload)

        self.assertEqual(MqttHandler.active_vehicle_dynamics['123'][0]['speed'], 100)

    def test_deploy_yaml(self):
        # Mock the YAML and vehicle IDs
        yaml = "mock_yaml"
        vehicle_ids = ['123', '456']

        # Call the deploy_yaml method
        MqttHandler.deploy_yaml(yaml, vehicle_ids)

        # Check if the publish method was called for each vehicle ID
        MqttHandler.client.publish.assert_any_call(f"vehicle/123/manifest/apply/req", yaml)
        MqttHandler.client.publish.assert_any_call(f"vehicle/456/manifest/apply/req", yaml)

if __name__ == '__main__':
    unittest.main()
