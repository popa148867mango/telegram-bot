import os
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import asyncio

# Берем токен из секретов GitHub
API_TOKEN = os.getenv('BOT_TOKEN6767')
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Словарь для хранения ставок: { "Имя_бойца": [список_юзернеймов] }
bets = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Бот для ставок запущен! Пиши '+имя бойца', чтобы поставить.")

@dp.message(F.text.startswith('+'))
async def add_bet(message: types.Message):
    # Получаем имя бойца из сообщения (все что после '+')
    fighter = message.text[1:].strip().lower()
    user = message.from_user.username or message.from_user.full_name
    
    if fighter not in bets:
        bets[fighter] = []
    
    if user not in bets[fighter]:
        bets[fighter].append(user)
        await message.answer(f"Принято! Ставка на {fighter} засчитана.")
    else:
        await message.answer("Ты уже ставил на этого бойца!")

@dp.message(Command("list"))
async def show_bets(message: types.Message):
    if not bets:
        await message.answer("Ставок пока нет.")
        return
    
    response = "Текущие ставки:\n"
    for fighter, users in bets.items():
        response += f"\nБоец {fighter.capitalize()}: {len(users)} чел. ({', '.join(users)})"
    await message.answer(response)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
