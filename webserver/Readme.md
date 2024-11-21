
# Introduction
This is the Ankaios Management Server. It is build on Django and displays a dashboard of all connected Ankaios Fleet Manager, displayed as vehicles. It is also able to push deployment configurations to all connectors, effectively changing agents and workloads running on a connected target vehicle.

# Requirements
The "shift2sdv" devcontainer is already setup for the server. So starting and connecting to the instance is all that is required to run the server.

# Starting the server
After connecting to the devcontainer, start the server by running.
`cd webserver`
`python manage.py runserver`
The server is now running and can be accessed by
`localhost:8000`
in your browser. If you have issues accessing it, forward the port in your devcontainer to your pc if it has not already been done.
Beware that this project is using the Django dev server and is not fit for production use!

# Usage
After starting the server and opening the local address in your browser, you should now see the dashboard.
There, all connected vehicles and their VIN are displayed. Each vehicle (being a connected Ankaios Fleet Manager) is made up of agents running workloads. It is also showing general vehicle data for monitoring like speed, and showing the state of each workload.

At the bottom, there is a file upload form where a Ankaios YAML infrastructure file can be uploaded and pushed to a certain vehicle, selected by the VIN in the form. After pushing the submit button, the YAML is pushed to the corresponding Ankaios Fleet Manager, which is processing the YAML via the Ankaios API.

# How it works
The Ankaios Management Server is based upon Django, an Open Source Framework for building server applications in python. It has two tasks: 
1. Providing the visualizations in the browser as a dashboard
2. Communicating with the Ankaios Fleet Manager, fetching vehicle data and pushing YAMLs to update workloads
The visualization is done via a template that uses the python data to generate an html website. For stylization it is using Bootstrap 4.
For the connection between the Ankaios  Server and the Ankaios Fleet Manager, it is using MQTT. Each connector is publishing vehicle dynamics data as json string on a common MQTT channel. The server is listening on this channel, deserializing and displaying received vehicle data. It is saving the last 50 received data points in RAM, the vehicle data is currently not stored persistently in a database and will be closed if the server is shut down.