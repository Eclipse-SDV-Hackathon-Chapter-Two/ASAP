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

import sys, time, json, logging, os

from ankaios_sdk import Ankaios
import ecal.core.core as ecal_core
import paho.mqtt.client as mqtt
from ecal.core.subscriber import StringSubscriber

logger = logging.getLogger("vehicle_state_log")
stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setLevel(logging.INFO)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)

# Vehice dynamics handling topic
BROKER = os.environ.get('MQTT_BROKER_ADDR', 'localhost')
PORT = int(os.environ.get('MQTT_BROKER_PORT', '1883'))
VEHICLE_ID = os.environ.get('VIN')
TOPIC = f'vehicle/vehicle_dynamics'
INTERVAL = int(os.environ.get('INTERVAL', '1'))
# Create an MQTT client instance
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.connect(BROKER, PORT, 60)

# Callback for receiving messages
def callback(topic_name, msg, time):
    try:
        json_msg = json.loads(msg)
        vehicle_dynamics = json_msg

        with Ankaios() as ankaios:
            state = ankaios.get_state(field_masks=["workloadStates"])
            vehicle_dynamics["workload_states"] = state.to_dict()["workload_states"]
            vehicle_dynamics["vehicle_id"] = VEHICLE_ID

            logger.info(f"Received: {vehicle_dynamics}")
            mqtt_client.publish(TOPIC, str(vehicle_dynamics))
    except json.JSONDecodeError:
        logger.error(f"Error: Could not decode message: '{msg}'")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    logger.info("Starting vehicle state logger...")

    # Initialize eCAL
    ecal_core.initialize(sys.argv, "Vehicle State Log")

    # Create a subscriber that listens on the "traffic_sign_detection"
    sub = StringSubscriber("vehicle_dynamics")

    # Set the Callback
    sub.set_callback(callback)
    
    # Just don't exit
    while ecal_core.ok():
        time.sleep(0.5)
    
    # finalize eCAL API
    ecal_core.finalize()