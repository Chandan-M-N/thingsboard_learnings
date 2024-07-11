from influxdb import InfluxDBClient
import asyncio
import websockets
import json


def influx_write(val):
    # Configure InfluxDB connection variables
    host = '24.98.212.253'  # InfluxDB host
    port = 8086         # InfluxDB HTTP API port
    user = 'admin'  # InfluxDB username
    password = 'admin'  # InfluxDB password
    dbname = 'my_database'  # InfluxDB database name
    measurement = 'temperature'  # Measurement name

    # Create a connection to InfluxDB
    client = InfluxDBClient(host, port, user, password, dbname)

    # Define the data point to be inserted
    json_body = [
        {
            "measurement": measurement,
            "fields": {
                "value": float(val)
            }
        }
    ]

    # Write the data to InfluxDB
    client.write_points(json_body)

    # Query the data to verify insertion
    result = client.query(f'SELECT * FROM {measurement}')
    print(f"Query result: {result.raw}")

    # Close the InfluxDB client connection
    client.close()


THINGSBOARD_HOST = '24.98.212.253'
JWT_TOKEN = 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZW5hbnRAdGhpbmdzYm9hcmQub3JnIiwidXNlcklkIjoiMmUyNGUzMDAtM2RlMS0xMWVmLWJmN2UtNTViYWRhYmJlZGI1Iiwic2NvcGVzIjpbIlRFTkFOVF9BRE1JTiJdLCJzZXNzaW9uSWQiOiJiYjg1NWZhNC01ZGI3LTRjZDQtYjY0OS1mNTE2OWI5MjczMDkiLCJleHAiOjE3MjA2OTk5NDMsImlzcyI6InRoaW5nc2JvYXJkLmlvIiwiaWF0IjoxNzIwNjkwOTQzLCJlbmFibGVkIjp0cnVlLCJpc1B1YmxpYyI6ZmFsc2UsInRlbmFudElkIjoiMmQ3M2UyODAtM2RlMS0xMWVmLWJmN2UtNTViYWRhYmJlZGI1IiwiY3VzdG9tZXJJZCI6IjEzODE0MDAwLTFkZDItMTFiMi04MDgwLTgwODA4MDgwODA4MCJ9.kcKXWcESJK9G0YUDtOSE8UCF8QTgvFQMM8I586VRlZS_XNs5upNHiXtROkNguFqi6FWjyTk-DiF1zKWNm0PqtQ'

async def subscribe_to_telemetry():
    url = f"ws://{THINGSBOARD_HOST}:8080/api/ws/plugins/telemetry?token={JWT_TOKEN}"
    async with websockets.connect(url) as websocket:
        # Subscribe to telemetry data for a specific device
        subscribe_message = {
            "tsSubCmds": [{
                "entityType": "DEVICE",
                "entityId": "4fddadf0-3edc-11ef-acf7-5ffa715571f5",
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
                influx_write(lt[0][1])

# Run the asyncio event loop to start the WebSocket client
asyncio.get_event_loop().run_until_complete(subscribe_to_telemetry())
