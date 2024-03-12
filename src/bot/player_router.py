# -*- coding: utf-8 -*-
from typing import Optional

from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select, update
from settings import settings
from db.database import async_session
from db.tables import TG, Roles
from bot.supdict import sqltranslation, translation

router = Router()


async def find_role(message: Message) -> Optional[int]:
    async with async_session() as session:
        query = select(TG.__table__.c.id).where(TG.__table__.c.tg_id == str(message.from_user.id))
        result = await session.execute(query)
        uid = result.one_or_none()
        if result is None:
            return None
        query = select(Roles.role_id, Roles.is_dead).where(Roles.__table__.c.user == int(uid[0]))
        result = (await session.execute(query)).one_or_none()
        if result is None or result[1]:
            return None
        role_id = result[0]
        if role_id is None:
            return None
        return int(role_id)


@router.message(F.text == "/get")
async def get(message: Message):
    role_id = await find_role(message)
    if role_id is None:
        await message.answer("Вы не игрок")
        return

    tmp = []
    tmp_facts = []
    cnt = 0
    for fact in settings.facts:
        if settings.facts[fact]:
            cnt += 1
            tmp.append(sqltranslation[fact])
            tmp_facts.append(fact)
    if cnt == 0:
        await message.answer("Пока все факты о вас закрыты(")
        return
    async with async_session() as session:
        query = select(Roles.__table__.c.opened).where(Roles.__table__.c.role_id == int(role_id))
        opened = (await session.execute(query)).first()[0].split(", ")
        query = select(*tmp).where(Roles.__table__.c.role_id == int(role_id))
        result = await session.execute(query)
        result = result.one_or_none()
        ans = ""
        for i in range(0, len(result)):
            ans += (("✅️ " if (tmp_facts[i] in opened) else "❎ ") + result[i] + "\n")
        t = 4000
        for i in range(0, int(len(ans)/t + 1)):
            await message.answer(ans[t*i:(t*(i+1))])


@router.message(F.text.startswith("/open "))
async def get(message: Message):
    role_id = await find_role(message)
    if role_id is None:
        await message.answer("Вы не игрок")
        return

    try:
        command, field = message.text.split(" ", maxsplit=1)
        if field not in translation:
            await message.answer(f"Неверно указано поле для открытия\n"
                                 f"Возможные поля:{[f for f in translation.keys()].__str__()}")
            return
        query = select(Roles.__table__.c.opened).where(Roles.__table__.c.role_id == int(role_id))
        if not settings.facts[translation[field]]:
            await message.answer("Поле закрыто администратором")
            return
        async with async_session() as session:
            result = (await session.execute(query)).first()[0]
            stmt = update(Roles.__mapper__
                          ).where(Roles.__table__.c.role_id == int(role_id)
                                                  ).values(opened=result + f", {translation[field]}")
            await session.execute(stmt)
            await session.commit()
            await message.answer("Успешно")
    except Exception as exc:
        await message.answer("Неверно указано поле для открытия")
        raise exc


@router.message(F.text == "/close_all")
async def get(message: Message):
    role_id = await find_role(message)
    if role_id is None:
        await message.answer("Вы не игрок")
        return

    try:
        async with async_session() as session:
            stmt = update(Roles.__mapper__
                          ).where(Roles.__table__.c.role_id == int(role_id)
                                                  ).values(opened="")
            await session.execute(stmt)
            await session.commit()
            await message.answer("Успешно")
    except Exception as exc:
        await message.answer("Ошибка")
        raise exc
