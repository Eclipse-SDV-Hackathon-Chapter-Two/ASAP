# Copyright (c) 2024 Elektrobit Automotive GmbH and others

# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# SPDX-License-Identifier: Apache-2.0

from ankaios_sdk import Ankaios, Manifest
import paho.mqtt.client as mqtt
import os
import logging
import sys

logger = logging.getLogger("fleet_manager")
stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setLevel(logging.INFO)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)

# Get config over environment variables
BROKER = os.environ.get("MQTT_BROKER_ADDR", "localhost")
PORT = int(os.environ.get("MQTT_BROKER_PORT", "1883"))
VEHICLE_ID = os.environ.get("VIN")
BASE_TOPIC = f"vehicle/{VEHICLE_ID}"

# Create a new Ankaios object.
# The connection to the control interface is automatically done at this step.
with Ankaios() as ankaios:

    def on_connect(client, userdata, flags, reason_code, properties):
        client.subscribe(f"{BASE_TOPIC}/manifest/apply/req")

    def on_manifest_update(client, userdata, msg):
        try:
            logger.info(
                f"Received message on topic {msg.topic} with payload {msg.payload.decode()}"
            )
            # Handle request for applying a manifest
            if msg.topic == f"{BASE_TOPIC}/manifest/apply/req":
                manifest = Manifest.from_string(str(msg.payload.decode()))
                ankaios.apply_manifest(manifest)
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    # Create an MQTT client instance
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    # Assign the callbacks
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_manifest_update

    # Connect to the MQTT broker
    mqtt_client.connect(BROKER, PORT, 60)

    # Blocking call that processes network traffic, dispatches callbacks,
    # and handles reconnecting.
    mqtt_client.loop_forever()
