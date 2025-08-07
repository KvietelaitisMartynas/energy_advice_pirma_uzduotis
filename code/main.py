'''
A program meant to analyze weather data for a specific location.
It fetches historical weather data, calculates statistics, and visualizes the results.

'''

from data_processing import DataProcessing
from visualization import Visualization
from weather_api import WeatherAPI
from datetime import datetime, timedelta


def main() -> None:
    location_code = "kaunas"

    # Initialize the WeatherAPI class with the location code
    weather_api = WeatherAPI(location_code)

    # Define the date range for historical data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # Fetch historical weather data for the specified date range
    historical_data = weather_api.get_historical_weather_data(start_date_str, end_date_str)
    
    if historical_data.empty:
        print("Nepavyko gauti istorinių duomenų")
        return
    
    print(f"Gauta {len(historical_data)} istorinių įrašų")

    # Calculate statistics from historical data
    stats = DataProcessing.calculate_yearly_statistics(historical_data)
    rainy_weekends = DataProcessing.count_rainy_weekends(historical_data)

    Visualization.display_statistics(stats, rainy_weekends)

    # Fetch weather forecast data
    weather_data = weather_api.get_weather_data()

    if weather_data.empty:
        print("Nepavyko gauti prognozės duomenų")
    else:
        print(f"Gauta {len(weather_data)} prognozės įrašų")

    # Visualize the temperature comparison
    Visualization.plot_temperature_comparison(historical_data, weather_data)


if __name__ == "__main__":
    main()