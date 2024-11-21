# ASAP - Shift to SDV

The ASAP shift to SDV project consists of 3 new Ankaios workloads and a webserver component to interact with via MQTT. The workloads fulfill the following use-cases:

1. [fleet_manager](apps/fleet_manager): Applies manifests .yaml files, that it receives via MQTT to the Ankaios instance e.g. to start new workloads.
2. [vehicle_state_log](apps/vehicle_state_log): Retrieves eCal information about the vehicles' dynamics, enriches the information with Ankaios execution state logs and publishes them to the MQTT broker
3. [speed_limit_assist](apps/speed_limit_assist): The speed_limit_assist provides new functionality to the Ankaios runtime, evaluating whether the maximum speed is exceeded, and logs violations to the info log.

To orchestrate the workloads, we implemented a simple [webserver](webserver). A user can upload a manifest .yaml file through the web UI. Simultaneously, while eCal is providing data, the UI displays the vehicle information and Ankaios execution state.

## How to get this to run

1. start dev container
2. in separate terminal instances inside your devcontainer, run the following:
   1. ``restart-shift2sdv``
   2. ``cd webserver && python3 manage.py runserver`` 
   3. ``ecal_play -m measurements/2024-11-19_15-45-14.870_measurement/``
      1. or wherever you have demo measurement data to play with eCal..
3. Open the webserver on localhost:8000

## Technologies used
- [Ankaios](https://projects.eclipse.org/projects/automotive.ankaios)
- [eCal](https://projects.eclipse.org/projects/automotive.ecal)
- [Mosquitto](https://mosquitto.org/)
- [MQTT Protocol](https://mqtt.org/)
- [Podman](https://podman.io/)
- [Django](https://www.djangoproject.com/)
- [Azure Cloud](https://azure.microsoft.com/)

## Architecture
![Architecture](./project_architecture.drawio.svg)