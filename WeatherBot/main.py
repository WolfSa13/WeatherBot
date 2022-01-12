import requests
import datetime
from conf import *
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer_sticker(
        sticker="https://cdn.tlgrm.app/stickers/697/ba1/697ba160-9c77-3b1a-9d97-86a9ce75ff4d/192/3.webp")
    await message.answer("Hello! Enter the city")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "☀ Clear ",
        "Clouds": "☁ Clear ",
        "Rain": "🌧 Rain",
        "Drizzle": "⛈ Drizzle",
        "Thunderstorm": "🌩 Thunderstorm",
        "Snow": "❄❄❄ Snow",
        "Mist": "🌫🌫 Mist"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={WEATHER_TOKEN}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = round(data["main"]["temp"], 1)

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Complicated.."

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        await message.answer("Oh, I know!")
        await message.answer_sticker(
            sticker="https://tlgrm.ru/_/stickers/697/ba1/697ba160-9c77-3b1a-9d97-86a9ce75ff4d/192/94.webp")
        await message.reply(f"Today {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                            f"The weather in: {city}\nTemperature: {cur_weather}C° {wd}\n"
                            f"Humidity is 💧: {humidity}%\nAtmospheric pressure: {pressure} \n Wind: {wind} m/s \n"
                            )
    except ValueError:
        await message.answer_sticker(
            sticker="https://tlgrm.ru/_/stickers/697/ba1/697ba160-9c77-3b1a-9d97-86a9ce75ff4d/6.webp")
        await message.answer("Hmmm, I don't know this city")


if __name__ == '__main__':
    executor.start_polling(dp)
