# Weather Forecast App with gRPC

This is a simple Weather Forecast App that uses gRPC to fetch weather forecasts from the NOAA API based on user-provided latitude and longitude.

## Setup Instructions

1. Ensure you have Python installed on your system.
2. Install the required dependencies by running:
   ```sh
   pip install -r requirements.txt
   ```
   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. weather.proto

weather_forecast_app/
├── weather.proto
├── weather_pb2.py
├── weather_pb2_grpc.py
├── weather_server.py
├── weather_client.py
├── README.md
└── requirements.txt
