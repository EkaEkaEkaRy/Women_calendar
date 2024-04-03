import aiogram
from aiogram.filters.command import Command, CommandStart
from .bd import create_user_cycles, start_date, end_date, cycle_start
from datetime import date
router = aiogram.Router()


# подключение к базе данных (или ее создание, если не существует)
async def on_startup(_):
    await cycle_start()


# добавление информации о начале или конце периода
@router.message(Command("adddataperiod"))
async def adddataperiod(message: aiogram.types):
    kb = [
        [
            aiogram.types.KeyboardButton(text="Начало"),
            aiogram.types.KeyboardButton(text="Конец")
        ],
    ]
    keyboard = aiogram.types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Отметьте начало или конец периода"
    )
    await create_user_cycles(message.from_user.id)
    await message.answer("Начало менструации?", reply_markup=keyboard)


@router.message(aiogram.F.text.lower() == "начало")
async def with_puree(message: aiogram.types.Message):
    # добавление даты в бд
    await start_date(user_id=message.from_user.id, start=date.today())
    await message.reply("Данные успешно сохранены")
    global starting
    starting = date.today()


@router.message(aiogram.F.text.lower() == "конец")
async def without_puree(message: aiogram.types.Message):
    # добавление даты в бд
    await end_date(user_id=message.from_user.id, start=starting, end=date.today())
    await message.reply("Данные успешно сохранены")


# получение информации о цикле
@router.message(Command("info"))
async def info(message: aiogram.types):
    kb = [
        [
            aiogram.types.KeyboardButton(text="Начало"),
            aiogram.types.KeyboardButton(text="Конец")
        ],
    ]
    keyboard = aiogram.types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Отметьте начало или конец периода"
    )
    await message.answer(f"Начало цикла через <b>{12}</b>\nФертильные дни через <b>{3}</b>", reply_markup=keyboard, parse_mode=aiogram.enums.ParseMode.HTML)

