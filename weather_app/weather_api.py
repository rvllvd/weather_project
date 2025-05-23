import requests

USER_AGENT = "weather-app-example"

def get_city_coordinates(city_name: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "format": "json",
        "q": city_name,
        "limit": 1,
    }
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    if not data:
        return None
    return float(data[0]["lat"]), float(data[0]["lon"])

def get_weather(lat: float, lon: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "hourly": "relative_humidity_2m",
        "timezone": "auto",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    current = data.get("current_weather", {})
    humidity_list = data.get("hourly", {}).get("relative_humidity_2m", [])
    humidity = humidity_list[0] if humidity_list else None
    return {
        "temperature": current.get("temperature"),
        "windspeed": current.get("windspeed"),
        "humidity": humidity,
        "time": current.get("time"),
    }
