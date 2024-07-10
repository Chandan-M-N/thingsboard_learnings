import asyncio
import websockets
import json
import time
import paho.mqtt.client as mqtt

THINGSBOARD_HOST = '24.98.212.253'
JWT_TOKEN = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZW5hbnRAdGhpbmdzYm9hcmQub3JnIiwidXNlcklkIjoiMmUyNGUzMDAtM2RlMS0xMWVmLWJmN2UtNTViYWRhYmJlZGI1Iiwic2NvcGVzIjpbIlRFTkFOVF9BRE1JTiJdLCJzZXNzaW9uSWQiOiJhNGE3YzljNC05ZTA2LTQwZjEtYTg2My0xNzU4MjczYWM0MjYiLCJleHAiOjE3MjA2MzQwOTYsImlzcyI6InRoaW5nc2JvYXJkLmlvIiwiaWF0IjoxNzIwNjI1MDk2LCJlbmFibGVkIjp0cnVlLCJpc1B1YmxpYyI6ZmFsc2UsInRlbmFudElkIjoiMmQ3M2UyODAtM2RlMS0xMWVmLWJmN2UtNTViYWRhYmJlZGI1IiwiY3VzdG9tZXJJZCI6IjEzODE0MDAwLTFkZDItMTFiMi04MDgwLTgwODA4MDgwODA4MCJ9.KAsZGOiUopJmQl0-oMdN-gjUWv96X44DnBc9wmcmL47L6ZHyuqp1CYT0-ugH-sJzxdS0Gz2hv3zq2r5_FbsJDQ'
MQTT_TOPIC = 'v1/devices/me/telemetry'
DEVICE_ID = '91c3d2f0-3e8f-11ef-acf7-5ffa715571f5'
PUBLISH_DEVICE_ACCESS_TOKEN = 'pSnqIvMGkaBqjbURy54U'
MQTT_CLIENT_ID = 'mqtt_client'

# MQTT setup
mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
mqtt_client.username_pw_set(PUBLISH_DEVICE_ACCESS_TOKEN)
mqtt_client.connect(THINGSBOARD_HOST, 1883, 60)
mqtt_client.loop_start()

async def subscribe_to_telemetry():
    url = f"ws://{THINGSBOARD_HOST}:8080/api/ws/plugins/telemetry?token={JWT_TOKEN}"
    async with websockets.connect(url) as websocket:
        # Subscribe to telemetry data for a specific device
        subscribe_message = {
            "tsSubCmds": [{
                "entityType": "DEVICE",
                "entityId": DEVICE_ID,
                "scope": "LATEST_TELEMETRY",
                "cmdId": 10,
                "type": "TIMESERIES"
            }],
            "historyCmds": [],
            "attrSubCmds": []
        }
        await websocket.send(json.dumps(subscribe_message))
        
        temperature_values = []
        while True:  # Infinite loop to continuously listen for data
            response = await websocket.recv()
            data = json.loads(response)
            if data['data'] is not None:
                temp_entry = data["data"]["temperature"]
                if temp_entry:
                    temperature = temp_entry[0][1]
                    temperature_values.append(int(temperature))
                    print(f"Received temperature: {temperature}")

            if len(temperature_values) >= 5:  # Check every 5 received temperatures
                average_temperature = sum(temperature_values) / len(temperature_values)
                print(f"Average temperature: {average_temperature}")
                await publish_average_temperature(average_temperature)
                temperature_values = []  # Reset the list after publishing

async def publish_average_temperature(average_temperature):
    payload = json.dumps({"averageTemperature": average_temperature})
    mqtt_client.publish(f'v1/devices/me/telemetry', payload)
    print(f"Published average temperature: {average_temperature} to topic: {MQTT_TOPIC}")

# Run the asyncio event loop to start the WebSocket client
asyncio.get_event_loop().run_until_complete(subscribe_to_telemetry())
