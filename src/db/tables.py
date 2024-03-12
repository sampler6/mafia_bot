from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    is_active = Column(Boolean)


class TG(Base):
    __tablename__ = "telegram"

    tg_id = Column(String, primary_key=True)
    id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


class Roles(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)  # имя
    about = Column(String, nullable=False)  # роль возраст
    job = Column(String, nullable=False)  # работа
    relation = Column(String, nullable=False)  # отношения
    behavior = Column(String, nullable=False)  # поведение
    hobby = Column(String, nullable=False)  # хобби
    dark_side = Column(String, nullable=False)  # Пороки личности, лол
    gift = Column(String, nullable=False)  # подарки
    additional = Column(String, nullable=False)  # доп
    description = Column(String, nullable=False)  # описание
    first_fact = Column(String, nullable=False)
    second_fact = Column(String, nullable=False)
    third_fact = Column(String, nullable=False)
    token = Column(String, nullable=False, unique=True)
    is_dead = Column(Boolean, nullable=False, default=False)
    is_registered = Column(Boolean, nullable=False, default=False)
    opened = Column(String, nullable=False, default="")
    user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
