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

from ankaios_sdk import Workload, Ankaios, WorkloadStateEnum, WorkloadSubStateEnum, AnkaiosLogLevel, Manifest, Request, CompleteState
import paho.mqtt.client as mqtt
import json
import os
import logging
import sys
import time

logger = logging.getLogger("fleet_manager")
stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setLevel(logging.INFO)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)

# Get config over environment variables
BROKER = os.environ.get('MQTT_BROKER_ADDR', 'localhost')
PORT = int(os.environ.get('MQTT_BROKER_PORT', '1883'))
VEHICLE_ID = os.environ.get('VIN')
BASE_TOPIC = f"vehicle/{VEHICLE_ID}"

logger.info("foobar")

# Create a new Ankaios object.
# The connection to the control interface is automatically done at this step.
with Ankaios() as ankaios:

        # Callback when the client receives a CONNACK response from the MQTT server
    def on_connect(client, userdata, flags, reason_code, properties):
        client.subscribe(f"{BASE_TOPIC}/manifest/apply/req")
        client.subscribe(f"{BASE_TOPIC}/error_speed")

    # Callback when a PUBLISH message is received from the MQTT server
    def on_manifest_update(client, userdata, msg):
        try:
            logger.info(f"Received message on topic {msg.topic} with payload {msg.payload.decode()}")
            # Handle request for applying a manifest
            if msg.topic == f"{BASE_TOPIC}/manifest/apply/req":
                manifest = Manifest.from_string(str(msg.payload.decode()))
                ret = ankaios.apply_manifest(manifest)
                if ret is not None:
                    client.publish(f"{BASE_TOPIC}/manifest/apply/resp", json.dumps(ret.to_dict()))
            # Handle vehicle speed error requests
            elif msg.topic == f"{BASE_TOPIC}/error_speed":
                speed = str(msg.payload.decode())
                logger.info(f"Received error speed: {speed}")
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