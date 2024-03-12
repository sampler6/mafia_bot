# -*- coding: utf-8 -*-
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from sqlalchemy import insert, select, update

from db.database import async_session
from db.tables import Users, TG, Roles
from settings import settings
import numpy as np
from bot.supdict import sqltranslation, translation

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    async with async_session() as session:
        query = select(TG.__table__.c.tg_id).where(TG.tg_id == str(message.from_user.id))
        result = await session.execute(query)
        if result is not None and result.scalars().first() == str(message.from_user.id):
            await message.answer("Вы уже зарегистрированы")
            return
        if settings.is_register_open:
            stmt = insert(Users.__mapper__).values({"is_active": True}).returning(Users.__table__.c.id)
            result = await session.execute(stmt)
            current_id = result.first()[0]
            stmt = insert(TG.__mapper__).values((str(message.from_user.id), current_id))
            await session.execute(stmt)
            await session.commit()
            await message.answer("Поздравляем, вы зарегистрированы")

        else:
            await message.answer("Регистрация закрыта")


@router.message(F.text.startswith("/token"))
async def get_token(message: Message):
    async with (async_session() as session):
        role_token = message.text.split(" ", maxsplit=1)[1]
        query = select(Roles.__table__.c.role_id, Roles.__table__.c.is_registered).where(Roles.__table__.c.token == role_token)
        result = await session.execute(query)
        result = result.first()
        if result[1]:
            await message.answer("Роль уже занята")

        query = select(TG.__table__.c.tg_id, TG.__table__.c.id).where(TG.tg_id == str(message.from_user.id))
        result = await session.execute(query)
        result = result.one_or_none()
        if result is None or result[0] != str(message.from_user.id):
            await message.answer("Вы не зарегистрированы. Используйте команду /start")
            return
        uid = result[1]

        stmt = update(Roles.__mapper__).where(Roles.__table__.c.token == role_token).values(user=uid, is_dead=False,
                                                                                           is_registered=True
                                                                                           ).returning(Roles.__table__.c.description)

        result = await session.execute(stmt)
        result = result.scalars().first()
        await message.answer(f"Описание вашего персонажа: {result}")
        await session.commit()


@router.message(F.text == "Узнать факты")
async def game(message: Message):
    query = select(Roles.__table__.c.role_id, Roles.__table__.c.name, Roles.__table__.c.opened,
                   Roles.__table__.c.is_dead)
    async with async_session() as session:
        result = (await session.execute(query)).all()
        for player in result:
            facts = np.unique(player[2].split(", "))
            q = []
            for fact in facts:
                if fact in sqltranslation and fact != "name":
                    q.append(sqltranslation[fact])
            if len(q) == 0:
                continue
            else:
                query = select(*q).where(Roles.role_id == player[0])
                result = (await session.execute(query)).one()
                ans = (f"{player[1]}:\n"
                       f"Статус: {'Выбыл' if player[3] else 'В игре'}\n\n")
                for i in range(0, len(result)):
                    ans += (result[i] + "\n")
                t = 4000
                for i in range(0, int(len(ans) / t + 1)):
                    await message.answer(ans[t * i:(t * (i + 1))])


@router.callback_query(F.data.startswith('AFBDFsplayer'))
async def vote(callback: CallbackQuery):
    role_id = int(callback.data[len("AFBDFsplayer"):])
    if not settings.is_poll_open or int(role_id) not in settings.current_poll_users:
        await callback.message.answer("Голосование закончилось или эта роль уже выбыла")
        return
    if callback.from_user.id in settings.current_poll_voted_users:
        await callback.message.answer("Вы уже проголосовали в этом голосовании")
        return
    settings.current_poll_users[role_id] += 1
    settings.current_poll_voted_users.append(callback.from_user.id)
    await callback.message.edit_reply_markup()
    await callback.message.answer("Ваш голос учтен")
