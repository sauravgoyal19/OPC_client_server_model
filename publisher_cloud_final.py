import paho.mqtt.client as mqtt
import os

def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_publish(client, obj, mid):
    print("mid: " + str(mid))

def on_log(client, obj, level, string):
    print("hererere")
    print(string)

url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://localhost:13102')

qos=1
for i in range(3):
    id = input("Enter client_id---")
    topic = input("Enter topic--")
    msg = input("Enter msg--")
    mqttc = mqtt.Client(client_id="id")
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    # mqttc.on_log = on_log
    mqttc.username_pw_set('eblqeput','XnFJqB1PlfPv')
    mqttc.connect('postman.cloudmqtt.com',13102)
    mqttc.publish(topic, msg,qos=qos)
    mqttc.disconnect()
