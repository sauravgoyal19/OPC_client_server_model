import paho.mqtt.client as mqtt
import os
import csv

def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    with open('iot_train_file.csv', mode='a') as file_to_write:
        writerm= csv.writer(file_to_write, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,lineterminator='\r')
        writerm.writerow([msg.topic,msg.payload.decode('ascii')])

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)


qoss=1
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_log = on_log
url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://localhost:13102')
topic=input("Enter topic--")
print("LISTNING--------\n")
mqttc.username_pw_set('eblqeput','XnFJqB1PlfPv')
mqttc.connect('postman.cloudmqtt.com',16666)
mqttc.subscribe(topic,qoss)
rc = 0
while rc == 0:
    rc = mqttc.loop()
print("rc: " + str(rc))
