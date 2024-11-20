import paho.mqtt.client as mqtt
import settings
import json

active_clusters = 0
BASE_TOPIC = f"vehicle/1"

MANIFEST_APPLY_TOPIC = f"{BASE_TOPIC}/manifest/apply/req"
UPDATE_DATA_TOPIC = 'ankaios_deploy_manager/mqtt/update_cluster'
REMOVE_DATA_TOPIC = 'ankaios_deploy_manager/mqtt/remove_cluster'

def on_connect(mqtt_client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(MANIFEST_APPLY_TOPIC)
       mqtt_client.subscribe(UPDATE_DATA_TOPIC)
       mqtt_client.subscribe(REMOVE_DATA_TOPIC)
   else:
       print('Bad connection. Code:', rc)

def on_message(mqtt_client, userdata, msg):
    if msg.topic == UPDATE_DATA_TOPIC:
       on_update_data(msg)
    if msg.topic == REMOVE_DATA_TOPIC:
       on_remove_data(msg)

def on_update_data(data):
    print("on_update_data")
    print(data)
    cluster_data = json.loads(data)[0]
    for i in len(active_clusters):
        active_cluster = active_clusters[i]
        if active_cluster['id'] == cluster_data['id']:
            active_cluster[i] = cluster_data
            print(f"Updated id: {active_cluster['id']}")
    
def on_remove_data(data):
    print("on_remove_data")
    print(data)
    cluster_data = json.loads(data)[0]
    found_index = -1
    for i in len(active_clusters):
        active_cluster = active_clusters[i]
        if active_cluster['id'] == cluster_data['id']:
            found_index = i

    if i != -1:
        active_clusters.pop(i)
        print(f"Removed id: {active_cluster['id']}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE
)
client.loop_start()

def deploy_yaml(yaml):
    client.publish(MANIFEST_APPLY_TOPIC, yaml)