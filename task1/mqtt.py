"""Demonstrate MQTT and its security and token access control mechanism with TB"""

import paho.mqtt.client as mqtt
import json
import time

# Configuration
THINGSBOARD_HOST = 'localhost'
THINGSBOARD_PORT = 1883
ACCESS_TOKEN = '1laorp8nd61tx6le2pqw'  # Replace with your device's access token

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

# Callback when a message is published
def on_publish(client, userdata, mid):
    print("Message published")

client_id = f"my_client_{int(time.time())}"  # Generate a unique client ID
client = mqtt.Client(client_id=client_id)

# Set access token for the client
client.username_pw_set(ACCESS_TOKEN)

# Assign callback functions
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to ThingsBoard MQTT broker
client.connect(THINGSBOARD_HOST, THINGSBOARD_PORT, 70)

# Start the loop
client.loop_start()

try:
    while True:
        # Prepare the telemetry data
        telemetry_data = {"temperature": 25}
        telemetry_json = json.dumps(telemetry_data)

        # Publish telemetry data to ThingsBoard
        result = client.publish('v1/devices/me/telemetry', telemetry_json, qos=1)
        result.wait_for_publish()
        print(f"Published: {telemetry_json}")

        # Wait for 10 seconds before publishing next data
        time.sleep(10)
except KeyboardInterrupt:
    print("Exiting...")

# Stop the loop and disconnect
client.loop_stop()
client.disconnect()
