## ThingsBoard with InfluxDB and Python

## Overview

This project integrates ThingsBoard, an open-source IoT platform, with InfluxDB, a time-series database, using Python for data handling and processing. The goal is to demonstrate how to store telemetry data from ThingsBoard into InfluxDB for further analysis and visualization.

## Requirements

- Docker: To manage and run ThingsBoard and potentially InfluxDB containers.
- Python 3.8+: Required for the integration script.
- InfluxDB: A time-series database for storing telemetry data.
- ThingsBoard: An IoT platform to receive and manage telemetry data.

## Setup Instructions

### 1. Running ThingsBoard Server

Ensure Docker is installed and operational. Use Docker Compose to start ThingsBoard:

```bash
docker-compose up -d
```

This command starts ThingsBoard in detached mode (`-d`), allowing it to run in the background.

### 2. Setting Up InfluxDB

#### Starting InfluxDB Server

Start InfluxDB using the following command:

```bash
sudo influxd
```

#### Creating a Database

Access the InfluxDB CLI by running `influx` in your terminal. Inside the InfluxDB shell, create a new database:

```sql
CREATE DATABASE my_database
```

### 3. Configuring and Running Python Script

#### Installing Python Dependencies

Install necessary Python packages using pip:

```bash
pip install influxdb websockets
```

#### Configuring the Python Script

Open `task7.py` in a text editor and configure the following variables based on your setup:

```python
from influxdb import InfluxDBClient
import asyncio
import websockets
import json

# InfluxDB configuration
host = 'localhost'  # Replace with your InfluxDB host
port = 8086
user = 'admin'  # InfluxDB username
password = 'admin'  # InfluxDB password
dbname = 'my_database'  # InfluxDB database name
measurement = 'temperature'  # Measurement name

# ThingsBoard configuration
THINGSBOARD_HOST = 'localhost'  # Replace with your ThingsBoard host
JWT_TOKEN = '<your JWT token>'
```

#### Running the Python Script

Execute the Python script to initiate data integration:

```bash
python script.py
```

### Generating JWT Token for ThingsBoard

To generate a JWT token for accessing ThingsBoard APIs, use the following curl command:

```bash
curl -X POST -d "{\"username\":\"tenant@thingsboard.org\", \"password\":\"tenant\"}" http://localhost:8080/api/auth/login --header "Content-Type:application/json"
```

Replace `tenant@thingsboard.org` and `tenant` with your actual ThingsBoard credentials.

## Testing the Integration

To test the integration, publish telemetry data to ThingsBoard. The Python script will receive this data via the WebSocket API and insert it into InfluxDB.

## Additional Notes

- Ensure Docker and necessary services (ThingsBoard, InfluxDB) are running before executing the Python script.
- Adjust host addresses, credentials, and other parameters as per your environment setup.

