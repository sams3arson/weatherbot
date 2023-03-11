from pyrogram import Client, filters
from pyrogram.types import Message
from tools import creds
from pathlib import Path
from weather import get_weather, Coordinates
from formatter import format_weather
from exceptions import ApiServiceError
import config
import texts


credentials = creds.get(Path(config.CREDS_FILE))
api_id, api_hash, bot_token, weather_api = credentials.api_id,\
        credentials.api_hash, credentials.bot_token, credentials.weather_api

app = Client("weather_bot", api_id, api_hash, bot_token)


@app.on_message(filters.command(["start", "help"]))
async def send_help(client: Client, message: Message) -> None:
    await message.reply(texts.HELP_TEXT)


@app.on_message(filters.location)
async def process_location(client: Client, message: Message) -> None:
    location = message.location
    try:
        weather = get_weather(Coordinates(longitude=location.longitude,
                          latitude=location.latitude), weather_api=weather_api)
    except ApiServiceError:
        await message.reply("Не удалось получить погоду в API сервиса погоды.")
        return
    await message.reply(format_weather(weather))


@app.on_message(filters.private)
async def provide_help(client: Client, message: Message) -> None:
    await message.reply(texts.PROVIDE_HELP)


app.run()

