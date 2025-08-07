import pandas as pd
import requests

class WeatherAPI:
    def __init__(self, location_code, api_key="https://api.meteo.lt/v1/"):
        self.location_code = location_code
        self.api_key = api_key.rstrip("/")

    def get_weather_data(self):
        url = f"{self.api_key}/places/{self.location_code}/forecasts/long-term"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                
                forecast_data = data.get('forecastTimestamps', [])

                if not forecast_data:
                    print("Nėra prognozės duomenų.")
                    return pd.DataFrame()

                df = pd.DataFrame(forecast_data)

                df['forecastTimeUtc'] = pd.to_datetime(df['forecastTimeUtc'])
                df = df.set_index('forecastTimeUtc')

                df.index = df.index.tz_localize('UTC').tz_convert('Europe/Vilnius')

                return df
            
        except Exception as e:
            print(f"Klaida gaunant ilgalaikės prognozės duomenis: {e}")
            return pd.DataFrame()