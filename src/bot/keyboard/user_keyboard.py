from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='Мой номер'
            )
        ],
        [
            KeyboardButton(
                text='Мое место в рейтинге'
            )
        ],
    ],
    resize_keyboard=True
)
