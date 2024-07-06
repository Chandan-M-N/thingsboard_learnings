## Detailed README for Simple Analysis Program with MQTT and ThingsBoard

### Overview
This project demonstrates how to read telemetry data from a ThingsBoard MQTT server, process it, and then publish the results to another local MQTT broker. The telemetry data (temperature) is analyzed to generate notifications based on specified conditions.

### Prerequisites
1. **ThingsBoard**: An open-source IoT platform for data collection, processing, and visualization.
2. **Mosquitto**: An open-source MQTT broker.
3. **Python**: Programming language.
4. **paho-mqtt**: Python client library for MQTT.
5. **websockets**: Python library for WebSocket.

### Setup and Execution

#### 1. Publish Telemetry Data to ThingsBoard MQTT Server
Use the following command to publish temperature data to the ThingsBoard MQTT server.

```sh
mosquitto_pub -d -q 1 -h "localhost" -p "1883" -t "v1/devices/me/telemetry" -u "device_access_token" -m '{"temperature": 45}'
```

Replace `device_access_token` with your actual device access token.

#### 2. ThingsBoard Rule Chain
The telemetry data goes through a ThingsBoard rule chain. The rule chain performs the following tasks:
1. **Script Validation**: Validates the temperature data.
2. **Save Timeseries**: Stores valid telemetry data.
3. **Conditional Notifications**: Generates notifications based on temperature conditions.

##### Script Validation
```javascript
return msg.temperature == null || (msg.temperature >= -40 && msg.temperature <= 80);
```

##### Conditional Notifications
1. **High Temperature**:
```javascript
if (msg.temperature > 40) {
    return true;
}
return false;
```
Creates a notification: "High temperature alert! Please stay indoors."

2. **Low Temperature**:
```javascript
if (msg.temperature < 0) {
    return true;
}
return false;
```
Creates a notification: "Low temperature alert! Please stay indoors."

#### 3. WebSocket API to Subscribe to Telemetry Data
Use the following Python code to subscribe to telemetry data from ThingsBoard:

```python
import asyncio
import websockets
import json
import paho.mqtt.client as mqtt

def publish(msg, temp):
    MQTT_HOST = 'localhost'
    MQTT_PORT = 1885
    MQTT_TOPIC = 'test/topic'
    MQTT_MESSAGE = f'{temp}, {msg}'
    MQTT_USERNAME = 'test_user'
    MQTT_PASSWORD = 'test'

    client = mqtt.Client(client_id='unique_client_id')
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    try:
        client.connect(MQTT_HOST, MQTT_PORT, 60)
    except Exception as e:
        print(f"Could not connect to MQTT broker: {e}")
        return

    client.loop_start()
    result = client.publish(MQTT_TOPIC, MQTT_MESSAGE)
    result.wait_for_publish()
    client.loop_stop()
    client.disconnect()
    print("Message published successfully")

THINGSBOARD_HOST = 'localhost'
JWT_TOKEN = 'your_jwt_token'

async def subscribe_to_telemetry():
    url = f"ws://{THINGSBOARD_HOST}:8080/api/ws/plugins/telemetry?token={JWT_TOKEN}"
    async with websockets.connect(url) as websocket:
        subscribe_message = {
            "tsSubCmds": [{
                "entityType": "DEVICE",
                "entityId": "your_device_id",
                "scope": "LATEST_TELEMETRY",
                "cmdId": 10,
                "type": "TIMESERIES"
            }],
            "historyCmds": [],
            "attrSubCmds": []
        }
        await websocket.send(json.dumps(subscribe_message))
        
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            lt = list(data["data"]["temperature"])
            print("Received telemetry data:", lt[0][1])
            
            if int(lt[0][1]) > 40:
                publish('High Temperature Alert! Please Stay Indoors.', lt[0][1])
            elif int(lt[0][1]) < 0:
                publish('Low Temperature Alert! Please Stay Indoors.', lt[0][1])

asyncio.get_event_loop().run_until_complete(subscribe_to_telemetry())
```

Replace `your_jwt_token` and `your_device_id` with your actual JWT token and device ID.

#### 4. Start a Second Local MQTT Broker
Start the second MQTT broker on port 1885 using the following command:

```sh
mosquitto -c mosquitto.conf -v
```

Ensure the `mosquitto.conf` file contains:

```conf
listener 1885
allow_anonymous false
password_file E:\sensorweb\passwd
```

#### 5. Subscribe to the Second MQTT Broker
Use the following command to subscribe to the MQTT topic on the second broker:

```sh
mosquitto_sub -h localhost -p 1885 -t "test/topic" -u test_user -P test
```

### Workflow Summary
1. Publish telemetry data to ThingsBoard MQTT server.
2. Data goes through a ThingsBoard rule chain:
    - Validates the data.
    - Saves timeseries data.
    - Generates notifications based on conditions.
3. WebSocket API subscribes to telemetry data.
4. Analyzes the data and publishes results to the second local MQTT broker.
5. Second broker handles the received data for further processing or notifications.

This setup ensures real-time data processing and alert generation based on temperature conditions, demonstrating a comprehensive AI/data analytics workflow using MQTT and ThingsBoard.
