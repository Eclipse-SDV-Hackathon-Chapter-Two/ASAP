import paho.mqtt.client as mqtt
import os
import sys
import logging
import threading

logger = logging.getLogger("vehcile-data-sender")
stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setLevel(logging.INFO)
logger.addHandler(stdout)
logger.setLevel(logging.INFO)

# Configuration for MQTT  broker and topics
BROKER = os.environ.get('MQTT_BROKER_ADDR', 'localhost')
PORT = int(os.environ.get('MQTT_BROKER_PORT', '1883'))
TOPIC = 'vehicle/42/manifest/apply/req'
INTERVAL = int(os.environ.get('INTERVAL', '1'))

current_speed = 0
diff = 1

def send_manifest(client):
    with open("test.yaml", "rb") as f:
        file = f.read()
        client.publish(TOPIC, file)

    threading.Timer(INTERVAL, lambda: send_manifest(client)).start()

# Callback when the client receives a CONNACK response from the MQTT server
def on_connect(client, userdata, flags, reason_code, properties):
    logger.info("Connected to MQTT broker")
    logger.info(f"Topic:{TOPIC}")
    send_manifest(client)

# Create an MQTT client instance
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Assign the callbacks
mqtt_client.on_connect = on_connect

# Connect to the MQTT broker
mqtt_client.connect(BROKER, PORT, 60)

# Blocking call that processes network traffic, dispatches callbacks,
# and handles reconnecting.
mqtt_client.loop_forever()