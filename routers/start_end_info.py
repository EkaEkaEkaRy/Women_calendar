import aiogram
from aiogram.filters.command import Command, CommandStart

router = aiogram.Router()

#добавление информации о начале или конце периода
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
    await message.answer("Начало менструации?", reply_markup=keyboard)

@router.message(aiogram.F.text.lower() == "начало")
async def with_puree(message: aiogram.types.Message):
    await message.reply("Данные успешно сохранены")

@router.message(aiogram.F.text.lower() == "конец")
async def without_puree(message: aiogram.types.Message):
    await message.reply("Данные успешно сохранены")

#получение информации о цикле
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

