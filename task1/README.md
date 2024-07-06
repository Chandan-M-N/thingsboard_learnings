## Task 1 - MQTT with ThingsBoard: Security and Token Access Control Mechanism

This task demonstrates how to use MQTT to send telemetry data to ThingsBoard with a focus on security and token access control. I used the `paho.mqtt.client` library to connect to the ThingsBoard MQTT broker and publish telemetry data.

### Configuration

Update the `THINGSBOARD_HOST`, `THINGSBOARD_PORT`, and `ACCESS_TOKEN` variables in the script with ThingsBoard server details and device access token.

```python
THINGSBOARD_HOST = 'localhost'
THINGSBOARD_PORT = 1883
ACCESS_TOKEN = 'access token'  # Replace with device's access token
```

### Script Explanation

1. **Client Configuration:**
   - I generated a unique client ID using the current timestamp to ensure that each client has a unique identifier.
   - I set the access token for the client to authenticate with the ThingsBoard server.

2. **Callback Functions:**
   - `on_connect`: This function is called when the client successfully connects to the MQTT broker.
   - `on_publish`: This function is called when a message is successfully published to the MQTT broker.

3. **Connecting to the Broker:**
   - The client connects to the ThingsBoard MQTT broker using the provided host, port, and access token.

4. **Publishing Telemetry Data:**
   - In a loop, we prepare and publish telemetry data (e.g., temperature) to ThingsBoard every 10 seconds.

### Script

```python
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
```

### Security and Token Access Control

- **Access Token:** The access token is used to authenticate the client with ThingsBoard.
- **Unique Client ID:** Generating a unique client ID ensures that each client connection is unique, reducing the risk of connection conflicts.
