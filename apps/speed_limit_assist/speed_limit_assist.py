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

import json
import logging
import sys
import time

import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber
from ecal.core.publisher import StringPublisher

logger = logging.getLogger("speed_limit_assist")
stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setLevel(logging.INFO)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)


class SpeedLimitAssist:
    # Initialize SpeedLimitAssist
    def __init__(self, limit, limit_confidence, vel_mps):
        self.limit = limit
        self.limit_confidence = limit_confidence
        self.vel_mps = vel_mps

    # Checks if the driver is exceeding the speed limit and prints warning
    def check_speed_limit(self):
        if self.vel_mps > 0.0 and self.limit > 0.0:
            exceeded_speed = self.vel_mps - self.limit
            if exceeded_speed > 0.99:
                warning = (
                    "You are exceeding the current speed limit: "
                    + str(int(mps2kmh(self.limit)))
                    + " km/h by "
                    + str(int(mps2kmh(exceeded_speed)))
                    + " km/h"
                )
                logger.warning(warning)
                return exceeded_speed
        else:
            return 0.0


def kmh2mps(vel_kmh):
    vel_mps = vel_kmh / 3.6
    return vel_mps


def mps2kmh(vel_mps):
    vel_kmh = vel_mps * 3.6
    return vel_kmh


# Callback for receiving vehicle dynamic messages
def vehicle_dynamics_callback(topic_name, msg, time):
    try:
        json_msg = json.loads(msg)
        speed = json_msg["signals"]["speed"]
        speedLimitAssist.vel_mps = speed
    except json.JSONDecodeError:
        logger.error(f"Error: Could not decode message: '{msg}'")
    except Exception as e:
        logger.error(f"Error: {e}")


# Callback for receiving traffic sign detection messages
def traffic_sign_detection_callback(topic_name, msg, time):
    try:
        json_msg = json.loads(msg)
        class_ids = json_msg["class_ids"]
        confidences = json_msg["confidences"]

        if speedLimitAssist.limit != 0.0:
            current_speed_limit = speedLimitAssist.limit
        else:
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

                # Just store Speed Limits with high confidence
                if confidence > 0.6:
                    speedLimitAssist.limit = current_speed_limit
                    speedLimitAssist.limit_confidence = confidence
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

    # Create subscribers that listens on the "traffic_sign_detection" and "vehicle_dynamics"
    tsd_sub = StringSubscriber("traffic_sign_detection")
    vd_sub = StringSubscriber("vehicle_dynamics")

    # Set the Callbacks
    tsd_sub.set_callback(traffic_sign_detection_callback)
    vd_sub.set_callback(vehicle_dynamics_callback)


    sla_pub = StringPublisher("sla")
    
    if speedLimitAssist.limit > 0.0:
        exceededSpeed = speedLimitAssist.check_speed_limit()

    # Just don't exit
    while ecal_core.ok():
        if exceededSpeed > 0:
            sla_pub("Warning: Too fast!")
        else:
            sla_pub("")
        time.sleep(0.5)

    # finalize eCAL API
    ecal_core.finalize()
