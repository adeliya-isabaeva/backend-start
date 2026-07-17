!pip install aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
import asyncio
from g4f.client import Client

# Токен бота (получаем у @BotFather)
BOT_TOKEN = "8124101890:AAHvweFNKQjvIrOCu7gStnYritzqN_X57ZI"

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(
      parse_mode=ParseMode.MARKDOWN,
    ))
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
      "👋 Привет! Я пример бота на aiogram\n"
      "Задайте любой вопрос, связанный с различными языками программирования, и я отвечу на него)\n"
      "! В запросе не забывайте указывать про какой язык программирования вы имеете ввиду ! :)\n"
      "Для просмотра справки бота напишите '/help'\n\n"
    )

# Обработчик команды /help
@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
      "ℹ **Доступные команды:**\n"
      "/start - начать работу\n"
      "/help - справка\n\n"
    )

async def send_request_gpt(content: str,message : Message):
    client = Client()
    response = client.chat.completions.create(
        #model="gpt-4o-mini",
		model="g4f.models.gpt_4",
		#model=g4f.models.gpt_4,
        messages=[{"role":"user","content":content}],
        web_search=False
    )
    await message.answer (response.choices[0].message.content)

# Обработчик текстовых сообщений
@dp.message()
async def echo_message(message: Message):
    text=message.text.lower()
    await send_request_gpt(text, message)

# Запуск бота
async def main():
    await dp.start_polling(bot)

# asyncio.run(main())

