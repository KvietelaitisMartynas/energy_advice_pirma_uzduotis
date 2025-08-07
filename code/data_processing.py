'''

This class is used to process weather data (e.g., calculating yearly statistics, counting rainy weekends, and interpolating temperature data).

'''

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Optional


class DataProcessing:
    
    @staticmethod
    def calculate_yearly_statistics(data: pd.DataFrame) -> Dict[str, Optional[float]]:
        """
        Calculate yearly weather statistics from historical data.
        
        Args:
            data: DataFrame with weather data containing datetime index
                 and columns like 'airTemperature', 'relativeHumidity'
        
        Returns:
            Dictionary containing calculated statistics:
            - avg_temperature: Average temperature for the year
            - avg_humidity: Average humidity for the year  
            - avg_day_temperature: Average temperature during day hours (08:00-20:00)
            - avg_night_temperature: Average temperature during night hours (20:01-07:59)
        """
        stats = {}

        if 'airTemperature' in data.columns:
            valid_temps = data['airTemperature'].dropna()
            stats['avg_temperature'] = valid_temps.mean() if len(valid_temps) > 0 else None
        
        if 'relativeHumidity' in data.columns:
            valid_humidity = data['relativeHumidity'].dropna()
            stats['avg_humidity'] = valid_humidity.mean() if len(valid_humidity) > 0 else None

        if 'airTemperature' in data.columns:
            data_with_hour = data.copy()
            data_with_hour['hour'] = data_with_hour.index.hour
            
            # Day: 08:00-20:00, Night: 20:01-07:59
            day_mask = (data_with_hour['hour'] >= 8) & (data_with_hour['hour'] <= 20)
            night_mask = ~day_mask
            
            day_temps = data_with_hour[day_mask]['airTemperature'].dropna()
            night_temps = data_with_hour[night_mask]['airTemperature'].dropna()
            
            stats['avg_day_temperature'] = day_temps.mean() if len(day_temps) > 0 else None
            stats['avg_night_temperature'] = night_temps.mean() if len(night_temps) > 0 else None
        
        return stats

    @staticmethod
    def count_rainy_weekends(data: pd.DataFrame) -> int:
        """
        Count the number of weekends with precipitation.
        
        Args:
            data: DataFrame with weather data containing datetime index
                 and 'precipitation' column
        
        Returns:
            Number of weekends that had any precipitation
        """
        if 'precipitation' not in data.columns:
            return 0
        
        # Add weekday column (0=Monday, 5=Saturday, 6=Sunday)
        weekend_data = data.copy()
        weekend_data['weekday'] = weekend_data.index.weekday
        weekend_data['year'] = weekend_data.index.year
        weekend_data['week'] = weekend_data.index.isocalendar().week
        
        # Filter only weekends (Saturday and Sunday)
        weekend_data = weekend_data[weekend_data['weekday'].isin([5, 6])]
        
        if weekend_data.empty:
            return 0
        
        rainy_weekends = 0
        
        # Group by year and week
        for (year, week), group in weekend_data.groupby(['year', 'week']):
            # Check if there was precipitation during the weekend
            total_precipitation = group['precipitation'].sum()
            if total_precipitation > 0:
                rainy_weekends += 1
        
        return rainy_weekends

    @staticmethod
    def interpolate_temperature_data(temperature_series: pd.Series) -> pd.Series:
        """
        Interpolate hourly temperature data to 5-minute intervals.
        
        Takes a pandas Series with hourly temperature data and creates 
        intermediate values using time-based interpolation to produce
        a Series with 5-minute frequency.
        
        Args:
            temperature_series: pandas Series with datetime index containing
                               hourly temperature measurements
        
        Returns:
            pandas Series with 5-minute frequency and interpolated temperature values
        """
        if temperature_series.empty:
            return pd.Series(dtype=float)
        
        # Create new index with 5-minute intervals
        start_time = temperature_series.index.min()
        end_time = temperature_series.index.max()
        
        new_index = pd.date_range(start=start_time, end=end_time, freq='5T')
        
        # Reindex original data with new index
        reindexed_series = temperature_series.reindex(new_index)
        
        # Interpolate missing values using time-based method
        interpolated_series = reindexed_series.interpolate(method='time')
        
        return interpolated_series