from weather_api import WeatherAPI
import pandas as pd
from datetime import datetime, timedelta

def main():
    location_code = "kaunas"

    weather_api = WeatherAPI(location_code)

    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    weather_data = weather_api.get_weather_data()

    if weather_data.empty:
        print("Nepavyko gauti prognozės duomenų!")
    else:
        print(f"Gauta {len(weather_data)} prognozės įrašų")

if __name__ == "__main__":
    main()