# Vehicle State Log

The vehicle state log parses eCal messages from the "vehicle_dynamics" topic, aggregates them with the Ankaios workload states information as well as vehicle ID and publishes them together via an MQTT "vehicle/vehicle_dynamics" topic.

For this workload to publish messages, you need either live eCal data or feed it via ecal_play. Example: "ecal_play -m measurements/2024-11-19_15-45-14.870_measurement"

Example of one message at a given timeframe:

```json
{
   "header":{
      "timestamp":"1732027561098925"
   },
   "errs":{
      "speed":"STATE_FAULT",
      "speedDisplayed":"STATE_FAULT",
      "longAcc":"STATE_FAULT",
      "latAcc":"STATE_FAULT",
      "yawrate":"STATE_FAULT",
      "steeringWheelAngle":"STATE_FAULT",
      "steeringWheelAngleSpeed":"STATE_FAULT",
      "drvSteerTorque":"STATE_FAULT",
      "timeSinceLastClick":"STATE_FAULT",
      "wheelSteeringAngleFront":"STATE_FAULT",
      "wheelSteeringAngleRear":"STATE_FAULT"
   },
   "signals":{
      "speed":19.372236,
      "speedDisplayed":20.000015,
      "speedPerWheel":[
         19.366682,
         19.360432,
         19.283348,
         19.272932
      ],
      "longAcc":0.21875,
      "latAcc":-0.01,
      "yawrate":-0.00261795,
      "steeringWheelAngle":-0.0069812,
      "steeringWheelAngleSpeed":0.0,
      "drvSteerTorque":0.0,
      "timeSinceLastClick":0.0,
      "wheelSteeringAngleFront":0.0,
      "wheelSteeringAngleRear":0.0
   },
   "variances":{
      "speed":0.0,
      "speedDisplayed":0.0,
      "longAcc":0.0,
      "latAcc":0.0,
      "yawrate":0.0,
      "steeringWheelAngle":0.0,
      "steeringWheelAngleSpeed":0.0,
      "drvSteerTorque":0.0,
      "timeSinceLastClick":0.0,
      "wheelSteeringAngleFront":0.0,
      "wheelSteeringAngleRear":0.0
   },
   "timestamps":{
      "speed":"0",
      "speedDisplayed":"0",
      "longAcc":"0",
      "latAcc":"0",
      "yawrate":"0",
      "steeringWheelAngle":"0",
      "steeringWheelAngleSpeed":"0",
      "drvSteerTorque":"0",
      "timeSinceLastClick":"0",
      "wheelSteeringAngleFront":"0",
      "wheelSteeringAngleRear":"0"
   },
   "workload_states":{
      "dashboard":{
         "Ankaios_Dashboard":{
            "0ba32254b65c5077bfb7149fdc9960f5af3fedcf4622684c812bc69fa7acafc2":{
               "state":"RUNNING",
               "substate":"RUNNING_OK",
               "additional_info":""
            }
         }
      },
      "hpc2":{
         "speed_limit_assist":{
            "1e600376e674d26d31edec1c65da3e730538ca8d2e7b38812412462f585c233e":{
               "state":"RUNNING",
               "substate":"RUNNING_OK",
               "additional_info":""
            }
         },
         "web_ivi":{
            "ef0a5f7acc914f9b5bdc73b43abf6722f89c50c08f6c4c1ebd0c5f172fa22fee":{
               "state":"RUNNING",
               "substate":"RUNNING_OK",
               "additional_info":""
            }
         },
         "vehicle_state_log":{
            "5d6a239725d411297393133ffdd27ea4d6f61c843b1187c71e7faebfdcfe0595":{
               "state":"RUNNING",
               "substate":"RUNNING_OK",
               "additional_info":""
            }
         }
      },
      "hpc1":{
         "fleet_manager":{
            "db410849ad59246596becd09690543254a57ba333e7262af8a3b6fa3d8f440ee":{
               "state":"RUNNING",
               "substate":"RUNNING_OK",
               "additional_info":""
            }
         }
      }
   },
   "vehicle_id":"1"
}
```

## Development 

The `restart-shift2sdv` script provides a very quick and convenient way to develop the application is short cycle.
[!Note] Before running the application, the MQTT broker has to be up and running under the IP specified in the env var inside "shift2sdv_manifest.yaml"!

```shell
restart-shift2sdv
ecal_play -m measurements/2024-11-19_15-45-14.870_measurement
ank-logs "vehicle_state_log"
```