import paho.mqtt.client as mqtt
from ankaios_deploy_manager import settings
import json

VEHICLE_DYNAMICS_TOPIC = 'vehicle/vehicle_dynamics/update_cluster'
REMOVE_DATA_TOPIC = 'ankaios_deploy_manager/mqtt/remove_cluster'

class MqttHandler():
    active_clusters = []
    client = None

    def on_connect(mqtt_client, userdata, flags, rc):
        if rc == 0:
            print('Connected successfully')
            mqtt_client.subscribe(VEHICLE_DYNAMICS_TOPIC)
            mqtt_client.subscribe(REMOVE_DATA_TOPIC)
        else:
            print('Bad connection. Code:', rc)

    def on_message(mqtt_client, userdata, msg):
        if msg.topic == VEHICLE_DYNAMICS_TOPIC:
            MqttHandler.on_update_data(msg)
        if msg.topic == REMOVE_DATA_TOPIC:
            MqttHandler.on_remove_data(msg)

    def on_update_data(data):
        print("on_update_data")
        print(data)
        cluster_data = json.loads(data)[0]

        for i in len(MqttHandler.active_clusters):
            active_cluster = MqttHandler.active_clusters[i]
            if active_cluster['id'] == cluster_data['id']:
                active_cluster[i] = cluster_data
                print(f"Updated id: {active_cluster['id']}")
        
    def on_remove_data(data):
        print("on_remove_data")
        print(data)
        cluster_data = json.loads(data)[0]
        found_index = -1
        for i in len(MqttHandler.active_clusters):
            active_cluster = MqttHandler.active_clusters[i]
            if active_cluster['id'] == cluster_data['id']:
                found_index = i

        if found_index != -1:
            MqttHandler.active_clusters.pop(i)
            print(f"Removed id: {active_cluster['id']}")

    def run_client():
        MqttHandler.client = mqtt.Client()
        MqttHandler.client.on_connect = MqttHandler.on_connect
        MqttHandler.client.on_message = MqttHandler.on_message
        MqttHandler.client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
        MqttHandler.client.connect(
            host=settings.MQTT_SERVER,
            port=settings.MQTT_PORT,
            keepalive=settings.MQTT_KEEPALIVE
        )
        MqttHandler.client.loop_start()
    def deploy_yaml(yaml, vehicle_ids):
        for vehicle_id in vehicle_ids:
            MqttHandler.client.publish(f"vehicle/{vehicle_id}/manifest/apply/req", yaml)