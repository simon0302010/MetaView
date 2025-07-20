from datetime import datetime, timedelta

import requests

from . import extra_data


def get_weather(date_str, lat, lon):
    # convert so api can understand
    dt = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
    if dt < datetime.now() - timedelta(days=7):
        return get_historical(dt, lat, lon)
    else:
        return get_forecast(dt, lat, lon)


def get_forecast(dt, lat, lon):
    dt = dt.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ("temperature_2m", "weather_code"),
        "past_days": "14",
        "forecast_days": "2",
        "timezone": "auto",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if "error" in data and data["error"]:
            return data["reason"], data["reason"]
        else:
            times = data["hourly"]["time"]
            temps = data["hourly"]["temperature_2m"]
            codes = data["hourly"]["weather_code"]

            combined = [
                {"time": t, "temperature_2m": temp, "weather_code": code}
                for t, temp, code in zip(times, temps, codes)
            ]

            success = False
            for timeset in combined:
                dt2 = datetime.strptime(timeset["time"], "%Y-%m-%dT%H:%M")
                if dt2 == dt:
                    temperature = str(timeset["temperature_2m"]) + " °C"
                    weather_code = str(timeset["weather_code"])
                    success = True
                    break
            if not success:
                return "Not found", "Not found"

        if str(weather_code) in extra_data.weather_codes.keys():
            # check if night or day
            if 6 <= dt.hour < 20:
                weather_str = extra_data.weather_codes[str(weather_code)]["day"][
                    "description"
                ]
            else:
                weather_str = extra_data.weather_codes[str(weather_code)]["night"][
                    "description"
                ]
        else:
            weather_str = f"Weather code {str(weather_code)} not found. Please create an issue on GitHub."

        return temperature, weather_str
    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}")
        return "Network Error", "Network Error"


def get_historical(dt, lat, lon):
    date = dt.strftime("%Y-%m-%d")

    hour = int(dt.strftime("%H"))

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": date,
        "end_date": date,
        "hourly": ("temperature_2m", "weather_code"),
        "timezone": "auto",
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if "error" in data and data["error"]:
            return data["reason"], data["reason"]
        else:
            temperature = str(data["hourly"]["temperature_2m"][hour]) + " °C"
            weather_code = str(data["hourly"]["weather_code"][hour])

        if str(weather_code) in extra_data.weather_codes.keys():
            # check if night or day
            if 6 <= hour < 20:
                weather_str = extra_data.weather_codes[str(weather_code)]["day"][
                    "description"
                ]
            else:
                weather_str = extra_data.weather_codes[str(weather_code)]["night"][
                    "description"
                ]
        else:
            weather_str = f"Weather code {str(weather_code)} not found. Please create an issue on GitHub."

        return temperature, weather_str
    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}")
        return "Network Error", "Network Error"


if __name__ == "__main__":
    print(get_weather("2022:08:14 14:12:31"))
