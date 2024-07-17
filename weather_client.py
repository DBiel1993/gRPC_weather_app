import grpc
import weather_pb2
import weather_pb2_grpc

def run():
    latitude = float(input("Enter the latitude: "))
    longitude = float(input("Enter the longitude: "))

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = weather_pb2_grpc.WeatherServiceStub(channel)
        location = weather_pb2.Location(latitude=latitude, longitude=longitude)
        response = stub.GetForecast(location)
        
        print("\nWeather Forecast:")
        for period in response.periods:
            print(f"{period.name}: {period.detailedForecast}")

if __name__ == '__main__':
    run()