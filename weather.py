from dataclasses import dataclass
from typing import TypeAlias
from enum import Enum
from urllib.error import URLError
from exceptions import ApiServiceError
from json.decoder import JSONDecodeError
import urllib.request
import json
import config

Celsius: TypeAlias = int

@dataclass(slots=True, frozen=True)
class Coordinates:
    latitude: float
    longitude: float


class WeatherType(Enum):
    THUNDERSTORM = "Гроза"
    DRIZZLE = "Изморось"
    RAIN = "Дождь"
    SNOW = "Снег"
    CLEAR = "Ясно"
    FOG = "Туман"
    CLOUDS = "Облачно"


@dataclass(slots=True, frozen=True)
class Weather:
    temperature: Celsius
    weather_type: WeatherType
    city: str


def get_weather(coordinates: Coordinates, weather_api: str) -> Weather:
    """Requests weather in OpenWeather API and returns it"""
    openweather_response = _get_openweather_response(latitude=coordinates.latitude,
                     longitude=coordinates.longitude, weather_api=weather_api)
    return _parse_openweather_response(openweather_response)


def _get_openweather_response(latitude: float, longitude: float,
                              weather_api: str) -> str:
    url = config.OPENWEATHER_URL.format(latitude=latitude, longitude=longitude,
                                        weather_api=weather_api)
    try:
        return urllib.request.urlopen(url).read()
    except URLError:
        raise ApiServiceError


def _parse_openweather_response(openweather_response: str) -> Weather:
    try:
        openweather_dict = json.loads(openweather_response)
    except JSONDecodeError:
        raise ApiServiceError
    return Weather(temperature=_parse_temperature(openweather_dict),
                   weather_type=_parse_weather_type(openweather_dict),
                   city=_parse_city(openweather_dict))


def _parse_temperature(openweather_dict: dict) -> Celsius:
    return Celsius(openweather_dict["main"]["temp"])


def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_dict["weather"][0]["id"])
    except (IndexError, KeyError):
        raise ApiServiceError
    weather_types = {
            "2": WeatherType.THUNDERSTORM,
            "3": WeatherType.DRIZZLE,
            "5": WeatherType.RAIN,
            "6": WeatherType.SNOW,
            "7": WeatherType.FOG,
            "800": WeatherType.CLEAR,
            "80": WeatherType.CLOUDS
    }
    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type
    raise ApiServiceError


def _parse_city(openweather_dict: dict) -> str:
    return openweather_dict["name"]

