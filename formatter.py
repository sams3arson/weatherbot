from weather import Weather

def format_weather(weather: Weather) -> str:
    """Formats weather data to string"""
    city = weather.city if weather.city else "Неизвестное место"
    return (f"{city}, температура {weather.temperature}°C, "
            f"{weather.weather_type.value}")

