# OPC UA → Cloud MQTT Pipeline

A small end-to-end demo of an industrial edge-to-cloud data pipeline: a simulated
**OPC UA** server publishes live sensor readings, a client consumes and visualizes
them in real time, and a pair of **MQTT** publisher/subscriber scripts bridge that
data to a cloud broker for downstream storage or processing.

This mirrors a common industrial IoT pattern — OPC UA on the plant floor (the
de facto standard for PLC/SCADA data access), MQTT for the lightweight
publish/subscribe hop to the cloud.

## Components

| File | Role |
|---|---|
| `opcua_server.py` | Simulated OPC UA server. Exposes a `Parameters` object with `Temperature`, `Pressure`, and `Time` variables, updated with random readings every 2 seconds — standing in for a real sensor/PLC endpoint. |
| `opcua_client.py` | OPC UA client. Connects to the server and live-plots the `Temperature` reading with matplotlib, polling every 2 seconds. |
| `publisher_cloud_final.py` | MQTT publisher. Reads a client id, topic, and message interactively and publishes them to an MQTT broker — the edge-to-cloud hop. |
| `subscriber_cloud_final.py` | MQTT subscriber. Listens on a topic and appends every message received to a local CSV, e.g. for building a training dataset from live readings. |

## Tech stack

Python, [`opcua`](https://pypi.org/project/opcua/) (OPC UA client/server), [`paho-mqtt`](https://pypi.org/project/paho-mqtt/), matplotlib.

## Running it

```bash
pip install opcua paho-mqtt matplotlib

# Terminal 1 — start the simulated OPC UA server
python opcua_server.py

# Terminal 2 — connect a client and watch the live temperature plot
python opcua_client.py
```

The MQTT scripts talk to any broker (e.g. a local [Mosquitto](https://mosquitto.org/)
instance, or a hosted broker) via environment variables — no credentials are
hardcoded in the source:

```bash
export MQTT_HOST=your-broker-host
export MQTT_PORT=1883
export MQTT_USERNAME=your-username   # omit for brokers that don't require auth
export MQTT_PASSWORD=your-password

python subscriber_cloud_final.py   # start listening first
python publisher_cloud_final.py    # then publish a few messages
```

`subscriber_cloud_final.py` writes received messages to `iot_train_file.csv` in
the current directory by default (override with `IOT_OUTPUT_FILE`).
