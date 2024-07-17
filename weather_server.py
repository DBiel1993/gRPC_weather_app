import grpc
from concurrent import futures
import time
import requests
import weather_pb2
import weather_pb2_grpc

class WeatherServiceServicer(weather_pb2_grpc.WeatherServiceServicer):
    def GetForecast(self, request, context):
        latitude = request.latitude
        longitude = request.longitude
        
        try:
            office, gridX, gridY = get_grid_points(latitude, longitude)
            forecast = get_forecast(office, gridX, gridY)
            response = weather_pb2.ForecastResponse()
            for period in forecast:
                forecast_period = weather_pb2.ForecastPeriod(
                    name=period['name'],
                    detailedForecast=period['detailedForecast']
                )
                response.periods.append(forecast_period)
            return response
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return weather_pb2.ForecastResponse()

def get_grid_points(latitude, longitude):
    url = f"https://api.weather.gov/points/{latitude},{longitude}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        office = data['properties']['gridId']
        gridX = data['properties']['gridX']
        gridY = data['properties']['gridY']
        return office, gridX, gridY
    else:
        raise Exception("Failed to get grid points. Please check the latitude and longitude.")

def get_forecast(office, gridX, gridY):
    url = f"https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast"
    response = requests.get(url)
    if response.status_code == 200:
        forecast_data = response.json()
        return forecast_data['properties']['periods']
    else:
        raise Exception("Failed to get forecast data.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    weather_pb2_grpc.add_WeatherServiceServicer_to_server(WeatherServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()