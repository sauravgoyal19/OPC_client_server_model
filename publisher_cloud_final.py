# MQTT publisher: bridges data from the OPC UA edge (server/client above)
# to a cloud MQTT broker, e.g. so a subscriber elsewhere can pick it up
# (see subscriber_cloud_final.py). Broker host/port/credentials are read
# from the environment rather than hardcoded, so this is safe to keep in
# a public repo and works against any broker without editing the code.
import paho.mqtt.client as mqtt
import os

def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_publish(client, obj, mid):
    print("mid: " + str(mid))

def on_log(client, obj, level, string):
    print(string)

MQTT_HOST = os.environ.get('MQTT_HOST', 'localhost')
MQTT_PORT = int(os.environ.get('MQTT_PORT', 1883))
MQTT_USERNAME = os.environ.get('MQTT_USERNAME')
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD')

qos = 1
for i in range(3):
    client_id = input("Enter client_id---")
    topic = input("Enter topic--")
    msg = input("Enter msg--")
    mqttc = mqtt.Client(client_id=client_id)
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    if MQTT_USERNAME:
        mqttc.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    mqttc.connect(MQTT_HOST, MQTT_PORT)
    mqttc.publish(topic, msg, qos=qos)
    mqttc.disconnect()
