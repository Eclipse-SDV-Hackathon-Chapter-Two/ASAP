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

import sys, time, json, logging

import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber

class SpeedLimitAssist:
    def __init__(self, limit, limit_confidence, vel_mps):
        self.limit = limit
        self.limit_confidence = limit_confidence
        self.vel_mps = vel_mps
    
    
    def check_speed_limit(self):
        
        if self.vel_mps > 0.0 and self.limit > 0.0:
            exceeded_speed = self.vel_mps - self.limit
            if exceeded_speed > 0.0 and self.limit_confidence > 0.5:
                warning = "You are exceeding the current speed limit= " + str(self.limit*3.6) + " by " + str(exceeded_speed*3.6) +  "km/h with a confidence of " + str(self.limit_confidence)
                logger.warning(warning)

logger = logging.getLogger("speed_limit_assist")
stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setLevel(logging.INFO)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)


def kmh2mps(vel_kmh):
    vel_mps = vel_kmh/3.6
    return vel_mps


def ego_callback(topic_name, msg, time):
    try:
        json_msg = json.loads(msg)
        speed = json_msg["signals"]["speed"]
        speedLimitAssist.vel_mps = speed
        if speedLimitAssist.limit > 0.0:
            speedLimitAssist.check_speed_limit()
            
    except json.JSONDecodeError:
        logger.error(f"Error: Could not decode message: '{msg}'")
    except Exception as e:
        logger.error(f"Error: {e}")


# Callback for receiving messages
def speed_limit_callback(topic_name, msg, time):
    try:
        json_msg = json.loads(msg)
        class_ids = json_msg["class_ids"]
        confidences = json_msg["confidences"]
        current_speed_limit = 0.0
        if len(class_ids) == len(confidences):
            for i in range(0, len(class_ids)):
                class_id = class_ids[i]
                confidence = confidences[i]

                if class_id == 4:
                    current_speed_limit = kmh2mps(10)
                elif class_id == 5:
                    current_speed_limit = kmh2mps(100)
                elif class_id == 6:
                    current_speed_limit = kmh2mps(130)
                elif class_id == 7:
                    current_speed_limit = kmh2mps(20)
                elif class_id == 8:
                    current_speed_limit = kmh2mps(30)
                elif class_id == 9:
                    current_speed_limit = kmh2mps(40)
                elif class_id == 10:
                    current_speed_limit = kmh2mps(5)
                elif class_id == 11:
                    current_speed_limit = kmh2mps(50)
                elif class_id == 12:
                    current_speed_limit = kmh2mps(60)
                elif class_id == 13:
                    current_speed_limit = kmh2mps(70)
                elif class_id == 14:
                    current_speed_limit = kmh2mps(80)
                elif class_id == 15:
                    current_speed_limit = kmh2mps(90)
                speedLimitAssist.limit = current_speed_limit
                speedLimitAssist.limit_confidence = confidence
        #print(f"Received speed_limit: {current_speed_limit}")
    except json.JSONDecodeError:
        logger.error(f"Error: Could not decode message: '{msg}'")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    logger.info("Starting speed_limit_assist...")

    # Initialize eCAL
    ecal_core.initialize(sys.argv, "Speed Limit Assist")

    # Initialize SpeedLimitAssist
    speedLimitAssist = SpeedLimitAssist(0.0, 0.0, 0.0)

    # Create a subscriber that listens on the "traffic_sign_detection"
    tsd_sub = StringSubscriber("traffic_sign_detection")
    ego_sub = StringSubscriber("vehicle_dynamics")

    # Set the Callback
    tsd_sub.set_callback(speed_limit_callback)
    ego_sub.set_callback(ego_callback)
    
    # Just don't exit
    while ecal_core.ok():
        time.sleep(0.5)
    
    # finalize eCAL API
    ecal_core.finalize()