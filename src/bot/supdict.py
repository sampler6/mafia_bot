# -*- coding: utf-8 -*-
from db.tables import Roles

translation = {
    "Имя": "name",
    "Описание": "about",
    "Работа": "job",
    "Отношения с персонажами": "relation",
    "Поведение": "behavior",
    "Хобби": "hobby",
    "Порок": "dark_side",
    "Подарок": "gift",
    "Дополнительная информация": "additional",
    "1 факт": "first_fact",
    "2 факт": "second_fact",
    "3 факт": "third_fact"
}

sqltranslation = {
    "name": Roles.__table__.c.name,
    "about": Roles.__table__.c.about,
    "job": Roles.__table__.c.job,
    "relation": Roles.__table__.c.relation,
    "behavior": Roles.__table__.c.behavior,
    "hobby": Roles.__table__.c.hobby,
    "dark_side": Roles.__table__.c.dark_side,
    "gift": Roles.__table__.c.gift,
    "additional": Roles.__table__.c.additional,
    "first_fact": Roles.__table__.c.first_fact,
    "second_fact": Roles.__table__.c.second_fact,
    "third_fact": Roles.__table__.c.third_fact
}

names = ["Александр", "Тамара", "Ксюша", "Варя", "Костян", "Алексей", "Андрей", "Борис", "Дмитрий", "Ольга", "Наталья"]