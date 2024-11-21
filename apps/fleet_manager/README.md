# Fleet Manager

The fleet_manager.py connects to the "vehicle/{VIN}/manifest/apply/req" MQTT topic to receive a manifest .yaml and apply it to the ankaios instance. MQTT broker IP and port are parsed from the environment.

## Development 

The `restart-shift2sdv` script provides a very quick and convenient way to develop the application is short cycle.
[!Note] Before running the application, the MQTT broker has to be up and running under the IP specified in the env var inside "shift2sdv_manifest.yaml"!

```shell
restart-shift2sdv
ank-logs "fleet_manager"
```