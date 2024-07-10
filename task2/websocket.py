import asyncio
import websockets
import json

import paho.mqtt.client as mqtt

def publish(msg, temp):
    # Configuration
    MQTT_HOST = 'localhost'
    MQTT_PORT = 1885
    MQTT_TOPIC = 'test/topic'
    MQTT_MESSAGE = f'{temp}, {msg}'
    MQTT_USERNAME = 'test_user'
    MQTT_PASSWORD = 'test'

    # Create an MQTT client instance with a unique client ID
    client = mqtt.Client(client_id='unique_client_id')

    # Set username and password for the client
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    # Connect to the MQTT broker
    try:
        client.connect(MQTT_HOST, MQTT_PORT, 60)
    except Exception as e:
        print(f"Could not connect to MQTT broker: {e}")
        return

    # Start the loop
    client.loop_start()

    # Publish the message to the specified topic
    result = client.publish(MQTT_TOPIC, MQTT_MESSAGE)
    result.wait_for_publish()

    # Stop the loop and disconnect from the MQTT broker
    client.loop_stop()
    client.disconnect()

    print("Message published successfully")



THINGSBOARD_HOST = '24.98.212.253'
JWT_TOKEN = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZW5hbnRAdGhpbmdzYm9hcmQub3JnIiwidXNlcklkIjoiMmUyNGUzMDAtM2RlMS0xMWVmLWJmN2UtNTViYWRhYmJlZGI1Iiwic2NvcGVzIjpbIlRFTkFOVF9BRE1JTiJdLCJzZXNzaW9uSWQiOiJiNjg0ZThkMS00MDA2LTQwZTItOTFiNi0zYzk0MjMxOGNhMjEiLCJleHAiOjE3MjA2MDY0NTAsImlzcyI6InRoaW5nc2JvYXJkLmlvIiwiaWF0IjoxNzIwNTk3NDUwLCJlbmFibGVkIjp0cnVlLCJpc1B1YmxpYyI6ZmFsc2UsInRlbmFudElkIjoiMmQ3M2UyODAtM2RlMS0xMWVmLWJmN2UtNTViYWRhYmJlZGI1IiwiY3VzdG9tZXJJZCI6IjEzODE0MDAwLTFkZDItMTFiMi04MDgwLTgwODA4MDgwODA4MCJ9.JfnvHnnNA7tMI49q7gvzs_H6YOsc76N8kBu7XDF1A8HyreL0zSRp811yTTyX81Umnyj8rkqwMuSiQGYcbu6hnA'

async def subscribe_to_telemetry():
    url = f"ws://{THINGSBOARD_HOST}:8080/api/ws/plugins/telemetry?token={JWT_TOKEN}"
    async with websockets.connect(url) as websocket:
        # Subscribe to telemetry data for a specific device
        subscribe_message = {
            "tsSubCmds": [{
                "entityType": "DEVICE",
                "entityId": "91c3d2f0-3e8f-11ef-acf7-5ffa715571f5",
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
            if data['data'] is not None:
                lt = list(data["data"]["temperature"])
                print("Received telemetry data:", lt[0][1])
                
                if int(lt[0][1]) > 40:
                    publish('High Temperature Alert! Please Stay Indoors.',lt[0][1])
                elif int(lt[0][1]) < 0:
                    publish('Low Temperature Alert! Please Stay Indoors.',lt[0][1])
           

# Run the asyncio event loop to start the WebSocket client
asyncio.get_event_loop().run_until_complete(subscribe_to_telemetry())











