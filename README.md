# ASAP - Shift to SDV

The ASAP shift to SDV project consists of 3 new Ankaios workloads and a webserver component to interact with via MQTT. The workloads fulfill the following use-cases:

1. [fleet_manager](apps/fleet_manager): Applies manifests .yaml files, that it receives via MQTT to the Ankaios instance e.g. to start new workloads.
2. [vehicle_state_log](apps/vehicle_state_log): Retrieves eCal information about the vehicles' dynamics, enriches the information with Ankaios execution state logs and publishes them to the MQTT broker
3. [speed_limit_assist](apps/speed_limit_assist): The speed_limit_assist provides new functionality to the Ankaios runtime, evaluating whether the maximum speed is exceeded, and logs violations to the info log.

To orchestrate the workloads, we implemented a simple [webserver](webserver). A user can upload a manifest .yaml file through the web UI. Simultaneously, while eCal is providing data, the UI displays the vehicle information and Ankaios execution state.

## Technologies used
- [Ankaios](https://projects.eclipse.org/projects/automotive.ankaios)
- [eCal](https://projects.eclipse.org/projects/automotive.ecal)
- [Mosquitto](https://mosquitto.org/)
- [MQTT Protocol](https://mqtt.org/)
- [Django](https://www.djangoproject.com/)
- [Azure Cloud](https://azure.microsoft.com/)

## Architecture
![Architecture](./project_architecture.drawio.svg)