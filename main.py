import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message

# Настройка логирования
logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv('BOT_TOKEN6767')
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Хранилище: { "Имя_бойца": [список_юзернеймов] }
bets = {}

# --- Команды ---

@dp.message(Command("start"))
async def start(message: Message):
    text = (
        "Привет! Я бот для ставок.\n\n"
        "Команды:\n"
        "/add [имя] — добавить бойца\n"
        "+[имя] — поставить на бойца\n"
        "/list — посмотреть список бойцов и ставки"
    )
    await message.answer(text)

@dp.message(Command("add"))
async def add_fighter(message: Message):
    # Разделяем команду и аргумент (имя бойца)
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Используй: /add ИмяБойца")
        return
    
    fighter_name = args[1].strip()
    if fighter_name not in bets:
        bets[fighter_name] = []
        await message.answer(f"Боец {fighter_name} добавлен!")
    else:
        await message.answer("Такой боец уже есть в списке.")

@dp.message(F.text.startswith("+"))
async def place_bet(message: Message):
    fighter_name = message.text[1:].strip()
    username = message.from_user.username or message.from_user.full_name
    
    if fighter_name in bets:
        if username not in bets[fighter_name]:
            bets[fighter_name].append(username)
            await message.answer(f"Ставка принята! Ты поставил на {fighter_name}.")
        else:
            await message.answer("Ты уже поставил на этого бойца.")
    else:
        await message.answer(f"Боец {fighter_name} не найден. Сначала добавь его через /add.")

@dp.message(Command("list"))
async def show_list(message: Message):
    if not bets:
        await message.answer("Список пуст.")
        return
    
    response = "Текущие ставки:\n\n"
    for fighter, users in bets.items():
        count = len(users)
        response += f"🥊 {fighter}: {count} чел. ({', '.join(users)})\n"
    
    await message.answer(response)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
