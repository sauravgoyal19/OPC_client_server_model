# MQTT subscriber: the other end of the cloud bridge — listens on a topic
# and appends every message received to a local CSV, e.g. for building a
# training dataset from live sensor readings. Broker host/port/credentials
# and the output file path are read from the environment/cwd rather than
# hardcoded, so this is safe to keep in a public repo and portable across
# machines.
import paho.mqtt.client as mqtt
import os
import csv

OUTPUT_FILE = os.environ.get('IOT_OUTPUT_FILE', 'iot_train_file.csv')

def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    with open(OUTPUT_FILE, mode='a', newline='') as file_to_write:
        writerm = csv.writer(file_to_write, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writerm.writerow([msg.topic, msg.payload.decode('ascii')])

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)


qoss = 1
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_log = on_log

MQTT_HOST = os.environ.get('MQTT_HOST', 'localhost')
MQTT_PORT = int(os.environ.get('MQTT_PORT', 1883))
MQTT_USERNAME = os.environ.get('MQTT_USERNAME')
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD')

topic = input("Enter topic--")
print("LISTENING--------\n")
if MQTT_USERNAME:
    mqttc.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttc.connect(MQTT_HOST, MQTT_PORT)
mqttc.subscribe(topic, qoss)
rc = 0
while rc == 0:
    rc = mqttc.loop()
print("rc: " + str(rc))
