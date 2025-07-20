import requests
from datetime import datetime

from . import extra_data

def get_weather(date_str, lat, lon):
    # convert so api can understand
    dt = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
    date = dt.strftime("%Y-%m-%d")
    
    hour = int(dt.strftime("%H"))
    
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": date,
        "end_date": date,
        "hourly": ("temperature_2m", "weather_code"),
        "timezone": "auto"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        temperature = str(data["hourly"]["temperature_2m"][hour - 1]) + " °C"
        weather_code = data["hourly"]["weather_code"][hour - 1]
        
        if str(weather_code) in extra_data.weather_codes.keys():
            # check if night or day
            if 6 <= hour < 20:
                weather_str = extra_data.weather_codes[str(weather_code)]["day"]["description"]
            else:
                weather_str = extra_data.weather_codes[str(weather_code)]["night"]["description"]
        else:
            weather_str = f"Weather code {str(weather_code)} not found. Please create an issue on GitHub."
        
        return temperature, weather_str
    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}")
        return "Network Error.", "Network Error."

if __name__ == "__main__":
    print(get_weather("2022:08:14 14:12:31"))