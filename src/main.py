# -*- coding: utf-8 -*-
import asyncio
import sys

from aiogram import Dispatcher, Bot, F
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from sqlalchemy import select

from bot.admin_router import router as admin_router
from bot.supdict import names
from bot.user_router import router as user_router
from bot.player_router import router as player_router
from config import ADMIN, TOKEN
from db.database import async_session
from db.tables import TG, Roles
from settings import settings
from db.roles_updator import update_roles


dp = Dispatcher()
bot = Bot(token=TOKEN)


@dp.message(F.chat.id == ADMIN,
            F.text.startswith("/role_update"))
async def role_update(message: Message):
    try:
        await loop.create_task(update_roles())
        await message.answer("Роли успешно обновлены")
    except Exception as exc:
        exc_info = sys.exc_info()
        await message.answer(f"Произошла ошибка: {str(exc_info)}")


@dp.message(F.text.startswith("/start_poll"),
            F.chat.id == ADMIN)
async def start_poll(message: Message):
    kb = InlineKeyboardBuilder()
    query = select(Roles.role_id, Roles.name, Roles.is_dead)
    if settings.is_poll_open:
        await message.answer("Вы не завершили прошлое голосование. /end_poll")
        return
    async with async_session() as session:
        result = (await session.execute(query)).all()
        for player in result:
            if not player[2]:
                kb.button(text=player[1], callback_data=f'AFBDFsplayer{player[0]}')
                settings.current_poll_users[player[0]] = 0
        settings.is_poll_open = True
        query = select(TG.tg_id)
        result = (await session.execute(query)).scalars().all()
        kb.adjust(2, 2, 2, 2, 2, 2)
        for user in result:
            await bot.send_message(user, text="Началось голосование. Выберете, кто покинет свадебный зал",
                                   reply_markup=kb.as_markup(resize_keyboard=True))


@dp.message(F.text.startswith("/final_poll"),
            F.chat.id == ADMIN)
async def final_poll(message: Message):
    kb = InlineKeyboardBuilder()
    if settings.is_poll_open:
        await message.answer("Вы не завершили прошлое голосование. /end_poll")
        return
    async with async_session() as session:
        kb.button(text="Продолжаем", callback_data=f'AFBDFsplayer0')
        kb.button(text="Заканчиваем", callback_data=f'AFBDFsplayer1')
        settings.current_poll_users[0] = 0
        settings.current_poll_users[1] = 0
        settings.is_poll_open = True
        settings.is_final_poll = True
        query = select(TG.tg_id)
        result = (await session.execute(query)).scalars().all()
        kb.adjust(2)
        for user in result:
            await bot.send_message(user, text="Началось голосование. Продолжаем или заканчиваем?",
                                   reply_markup=kb.as_markup(resize_keyboard=True))


@dp.message(F.text.startswith("/show_poll"),
            F.chat.id == ADMIN)
async def show_poll(message: Message):
    ans = ""
    for player in settings.current_poll_users:
        if not settings.is_final_poll:
            ans += f"{names[player - 1]}: {settings.current_poll_users[player]} голосов\n"
        else:
            ans += f"{'Продолжаем' if player == 0 else 'Заканчиваем'}: {settings.current_poll_users[player]} голосов\n"
    await message.answer(ans)


@dp.message(F.text.startswith("/end_poll"),
            F.chat.id == ADMIN)
async def end_poll(message: Message):
    ans = ""
    for player in settings.current_poll_users:
        if not settings.is_final_poll:
            ans += f"{names[player-1]}: {settings.current_poll_users[player]} голосов\n"
        else:
            ans += f"{'Продолжаем' if player==0 else 'Заканчиваем'}: {settings.current_poll_users[player]} голосов\n"
    await message.answer(ans)
    settings.current_poll_voted_users = []
    settings.current_poll_users = {}
    settings.is_poll_open = False
    settings.is_final_poll = False


async def bot_main():
    dp.include_router(admin_router)
    dp.include_router(user_router)
    dp.include_router(player_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(bot_main())
    loop.run_forever()
