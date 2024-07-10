# WebSocket and MQTT channel Integration with ThingsBoard to analyze and publish data

This Python script demonstrates how to subscribe to telemetry data from a device using WebSockets and publish processed data back to ThingsBoard using MQTT. It continuously listens for telemetry data, calculates the average temperature every 5 received values, and publishes the average temperature to ThingsBoard.

## Prerequisites

Before running the script, ensure you have the following:

- Python 3.x installed
- Required Python packages (`asyncio`, `websockets`, `paho-mqtt`)
- Access to a ThingsBoard instance with credentials and device details

## Setup

1. **Install Dependencies:**

   Install the required Python packages using pip:
   ```
   pip install asyncio websockets paho-mqtt
   ```

2. **Obtain JWT Token:**

   Use the following curl command to fetch the JWT Token required for authentication. Replace `username` and `password` with your ThingsBoard credentials.
   ```
   curl -X POST -d "{\"username\":\"tenant@thingsboard.org\", \"password\":\"tenant\"}" http://24.98.212.253:8080/api/auth/login --header "Content-Type:application/json"
   ```

   Replace the `JWT_TOKEN` variable in the script (`task2.py`) with the token obtained from this command.

3. **Update Script Variables:**

   - `THINGSBOARD_HOST`: Hostname or IP address of your ThingsBoard instance.
   - `DEVICE_ID`: ID of the device whose telemetry data you want to subscribe to.
   - `PUBLISH_DEVICE_ACCESS_TOKEN`: Access token for the device to publish telemetry data via MQTT.

## Script Explanation

The script performs the following actions:

- **WebSocket Connection:**
  - Connects to ThingsBoard WebSocket API to subscribe to telemetry data for a specific device (`DEVICE_ID`).

- **Telemetry Subscription:**
  - Subscribes to the latest telemetry data (`LATEST_TELEMETRY`) for the specified device.

- **Data Processing:**
  - Collects temperature data from received telemetry.
  - Calculates the average temperature every 5 received values.

- **MQTT Publishing:**
  - Uses MQTT to publish the calculated average temperature back to ThingsBoard under `v1/devices/me/telemetry`.

## Running the Script

Run the script (`task2.py`) using Python:
```
python task2.py
```

The script will continuously listen for telemetry data from ThingsBoard, calculate the average temperature every 5 received values, and publish it back using MQTT.

---
