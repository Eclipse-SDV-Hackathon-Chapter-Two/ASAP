## Cloud MQTT Broker

To create MQTT connection an MQTT Broker was set on Azure cloud.

To access MQTT Broker following IP address and port should be used:
- Public IP Address: 20.164.18.107
- MQTT Broker Port: 1883


### Connection Testing

```bash
# install   mosquitto_pub cli
sudo apt-get install mosquitto-clients
```

```bash
# Publish Topic 
mosquitto_pub -h 20.164.18.107 -p 1883 -t "test/topic" -m "Hello, MQTT!"
```

```bash
# Listen published topic
mosquitto_sub -h 20.164.18.107 -p 1883 -t "test/topic"

# Expected output
>>> Hello, MQTT!
```
