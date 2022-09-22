import logging
from pyowm.owm import OWM
from aiogram import Bot, Dispatcher, executor, types
from pyowm.utils.config import get_default_config
config_dict = get_default_config()
config_dict['language'] = 'ru'

API_TOKEN = 'YOU API TOKEN'
owm = OWM('09af5e7b80f9e46e0e0e4d45548a555a', config_dict)


# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("• Привет!\n• Напиши свой город что бы узнать погодку)")


@dp.message_handler()
async def echo(message: types.Message):
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(message.text)
    w = observation.weather

    resp_msg = f"• В городе: {message.text}\n\n"
    resp_msg += "• Температура: " + (str(round(w.temperature('celsius')["temp"]))) + " °C\n\n"
    resp_msg += f"• Состояние погоды: {w.detailed_status}\n\n"
    resp_msg += f"• Влажность составляет: {w.humidity}%\n\n"
    resp_msg += f"• Давление: {w.pressure['press']}mbar"

    if w.temperature('celsius')["temp"] < 17:
        resp_msg += "\n\n\n• Сейчас прохладно одевайтесь потеплее!♥"

    else:
        resp_msg += "\n\n\n• Сейчас тепло одевайтесь полегче!☺"

    await message.answer(resp_msg)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
