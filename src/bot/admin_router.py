# -*- coding: utf-8 -*-
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from sqlalchemy import select, update

from config import ADMIN
from db.database import async_session
from db.tables import Roles
from settings import settings
from bot.supdict import names
router = Router()


@router.message(F.text.startswith("/open_register"),
                F.chat.id == ADMIN)
async def open_register(message: Message):
    settings.is_register_open = True
    await message.answer("Регистрация открыта")


@router.message(F.text.startswith("/close_register"),
                F.chat.id == ADMIN)
async def open_register(message: Message):
    settings.is_register_open = False
    await message.answer("Регистрация закрыта")


@router.message(F.text.startswith("/open_fact"),
                F.chat.id == ADMIN)
async def open_fact(message: Message):
    spl = message.text.split(" ", maxsplit=1)
    if len(spl) < 2 or (fact := spl[1]) not in settings.facts.keys():
        await message.answer("Неправильное имя поля")
    else:
        settings.facts[fact] = True
        await message.answer("Поле успешно открыто")


@router.message(F.text.startswith("/close_fact"),
                F.chat.id == ADMIN)
async def open_fact(message: Message):
    spl = message.text.split(" ", maxsplit=1)
    if len(spl) < 2 or (fact := spl[1]) not in settings.facts.keys():
        await message.answer("Неправильное имя поля")
    else:
        settings.facts[fact] = False
        await message.answer("Поле успешно закрыто")


@router.message(F.text.startswith("/get_facts"),
                F.chat.id == ADMIN)
async def get_facts(message: Message):
    ans = ""
    for s in settings.facts.items():
        ans += f"{s[0]}: {s[1]}\n"
    await message.answer(ans)


@router.message(F.text.startswith("/get_roles"),
                F.chat.id == ADMIN)
async def get_roles(message: Message):
    query = select(Roles.__table__.c.role_id, Roles.__table__.c.about,
                   Roles.__table__.c.is_registered, Roles.__table__.c.is_dead)
    async with async_session() as session:
        result = await session.execute(query)
        result = result.all()
        ans = ""
        result = sorted(result, key=lambda x: x[0], reverse=False)
        for i in result:
            ans += f"{i[0]}: {i[1]}\nЗарегистрирован?: {i[2]}\nМертв?: {i[3]}\n"
    await message.answer(ans)


@router.message(F.text.startswith("/kill"),
                F.chat.id == ADMIN)
async def kill_player(message: Message):
    spl = message.text.split(" ", maxsplit=1)
    if len(spl) < 2:
        await message.answer("Неправильный id роли")
    role_id = spl[1]
    async with async_session() as session:
        stmt = update(Roles.__mapper__
                      ).where(Roles.__table__.c.role_id == int(role_id)).values(is_dead=True
                                                                                ).returning(Roles.__table__.c.role_id)
        result = await session.execute(stmt)
        result = result.one_or_none()
        if result is None:
            await message.answer("Неправильный id роли")
        else:
            await message.answer("Успешно убит")
        await session.commit()


@router.message(F.text.startswith("/heal"),
                F.chat.id == ADMIN)
async def heal_player(message: Message):
    spl = message.text.split(" ", maxsplit=1)
    if len(spl) < 2:
        await message.answer("Неправильный id роли")
    role_id = spl[1]
    async with async_session() as session:
        stmt = update(Roles.__mapper__
                      ).where(Roles.__table__.c.role_id == int(role_id)).values(is_dead=False
                                                                                ).returning(Roles.__table__.c.role_id)
        result = await session.execute(stmt)
        result = result.one_or_none()
        if result is None:
            await message.answer("Неправильный id роли")
        else:
            await message.answer("Успешно воскрешен")
        await session.commit()
