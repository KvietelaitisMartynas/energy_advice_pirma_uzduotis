''' 

This class is used to visualize weather data and statistics, including displaying calculated indicators and plotting temperature comparisons.

'''

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Optional


class Visualization:
    @staticmethod
    def display_statistics(stats: Dict[str, Optional[float]], rainy_weekends: int) -> None:
        """
        Display calculated weather statistics.
        
        Args:
            stats: Dictionary containing statistical indicators
            rainy_weekends: Number of rainy weekends
        """
        print("=" * 50)
        print("       METINIAI STATISTINIAI RODIKLIAI")
        print("=" * 50)
        print()
        
        # Average yearly temperature and humidity
        if stats.get('avg_temperature') is not None:
            print(f"Vidutinė metų temperatūra: {stats['avg_temperature']:.1f}°C")
        else:
            print("Vidutinė metų temperatūra: duomenų nėra")
        
        if stats.get('avg_humidity') is not None:
            print(f"Vidutinė metų oro drėgmė: {stats['avg_humidity']:.1f}%")
        else:
            print("Vidutinė metų oro drėgmė: duomenų nėra")
        
        print()
        
        # Day and night temperatures
        print("DIENOS IR NAKTIES TEMPERATŪROS (LT laiko zona):")
        print("   (Diena: 08:00-20:00, Naktis: 20:01-07:59)")
        
        if stats.get('avg_day_temperature') is not None:
            print(f"   • Vidutinė dienos temperatūra: {stats['avg_day_temperature']:.1f}°C")
        else:
            print("   • Vidutinė dienos temperatūra: duomenų nėra")
        
        if stats.get('avg_night_temperature') is not None:
            print(f"   • Vidutinė nakties temperatūra: {stats['avg_night_temperature']:.1f}°C")
        else:
            print("   • Vidutinė nakties temperatūra: duomenų nėra")
        
        print()
        
        # Rainy weekends
        print(f"Lietingų savaitgalių skaičius per metus: {rainy_weekends}")
        
        print()
        print("=" * 50)

    @staticmethod
    def plot_temperature_comparison(historical_df: pd.DataFrame, 
                                  forecast_df: pd.DataFrame, 
                                  days_back: int = 7) -> None:
        """
        Plot temperature comparison between historical and forecast data.
        
        Args:
            historical_df: Historical weather data
            forecast_df: Forecast weather data  
            days_back: Number of days back to show historical data
        """
        plt.figure(figsize=(15, 8))
        
        # Get recent historical data
        if not historical_df.empty:
            end_date = historical_df.index.max()
            start_date = end_date - timedelta(days=days_back)
            
            recent_historical = historical_df[historical_df.index >= start_date]
            
            # Plot historical data
            if 'airTemperature' in recent_historical.columns:
                valid_historical = recent_historical['airTemperature'].dropna()
                if not valid_historical.empty:
                    plt.plot(valid_historical.index, valid_historical.values, 
                            'b-', label='Išmatuota temperatūra', linewidth=2, marker='o', markersize=4)
        
        # Plot forecast data
        if not forecast_df.empty and 'airTemperature' in forecast_df.columns:
            valid_forecast = forecast_df['airTemperature'].dropna()
            if not valid_forecast.empty:
                plt.plot(valid_forecast.index, valid_forecast.values, 
                        'r--', label='Prognozuojama temperatūra', linewidth=2, marker='s', markersize=4)
        
        plt.xlabel('Laikas', fontsize=12)
        plt.ylabel('Temperatūra (°C)', fontsize=12)
        plt.title('Temperatūros palyginimas: istoriniai duomenys vs prognozė', fontsize=14, fontweight='bold')
        plt.legend(fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Improve date formatting on x-axis
        import matplotlib.dates as mdates
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
        
        plt.show()