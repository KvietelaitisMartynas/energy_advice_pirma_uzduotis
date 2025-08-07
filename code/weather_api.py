import pandas as pd
import requests
import time
from datetime import datetime, timedelta

class WeatherAPI:
    def __init__(self, location_code, api_key="https://api.meteo.lt/v1/"):
        self.location_code = location_code
        self.api_key = api_key.rstrip("/")

    def get_historical_weather_data(self, start_date, end_date):
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")

        all_data = []
        current_date = start_datetime

        stations_url = f"{self.api_key}/stations/"

        try:
            stations_response = requests.get(stations_url)
            if stations_response.status_code == 200:
                stations = stations_response.json()

                station_code = None
                for station in stations:
                    if self.location_code.lower() in station['name'].lower():
                        station_code = station['code']
                        break
                
                if not station_code and stations:
                    station_code = stations[0]['code']
                    print(f"Nerasta stotis '{self.location_code}', naudojama '{station_code}'")
                
                if not station_code:
                    print("Nerasta jokių stočių")
                    return pd.DataFrame()
                    
        except Exception as e:
            print(f"Klaida gaunant stočių sąrašą: {e}")
            return pd.DataFrame()

        while current_date <= end_datetime:
            date_str = current_date.strftime("%Y-%m-%d")
            url = f"{self.api_key}/stations/{station_code}/observations/{date_str}"

            try:
                response = requests.get(url)
                time.sleep(0.5)

                if response.status_code == 200:
                    data = response.json()

                    if 'observations' in data:
                        for entry in data['observations']:
                            if 'observationTimeUtc' in entry:
                                entry['observationTimeUtc'] = pd.to_datetime(entry['observationTimeUtc'])
                                all_data.append(entry)
                else:
                    print(f"Klaida gaunant duomenis {date_str}: {response.status_code}")

            except Exception as e:
                print(f"Klaida gaunant duomenis {date_str}: {e}")

            current_date += timedelta(days=1)

        if not all_data:
            return pd.DataFrame()
        
        df = pd.DataFrame(all_data)
        
        # Konvertuojame laiką
        df = df.set_index('observationTimeUtc')
        df.index = df.index.tz_localize('UTC').tz_convert('Europe/Vilnius')
        
        return df

    def get_weather_data(self):
        url = f"{self.api_key}/places/{self.location_code}/forecasts/long-term"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                
                forecast_data = data.get('forecastTimestamps', [])

                if not forecast_data:
                    print("Nėra prognozės duomenų")
                    return pd.DataFrame()

                df = pd.DataFrame(forecast_data)

                df['forecastTimeUtc'] = pd.to_datetime(df['forecastTimeUtc'])
                df = df.set_index('forecastTimeUtc')

                df.index = df.index.tz_localize('UTC').tz_convert('Europe/Vilnius')

                return df
            
        except Exception as e:
            print(f"Klaida gaunant ilgalaikės prognozės duomenis: {e}")
        
        return pd.DataFrame()
