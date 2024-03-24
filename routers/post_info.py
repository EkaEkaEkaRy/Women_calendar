import re

import aiogram
from aiogram.filters.command import Command, CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = aiogram.Router()

global isStartDate
global isPeriodDur
global isCycleDur
isStartDate = False
isPeriodDur = False
isCycleDur = False

#начало работы бота
@router.message(Command("start"))
async def cmd_start(message: aiogram.types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(aiogram.types.InlineKeyboardButton(
        text="Пропустить",
        callback_data="addstartinfo")
    )

    await message.answer("Этот календарь помогает: \n🌸 определить регулярность цикла\n🌸 прогнозировать дату ожидаемых месячных и дни овуляции\n🌸 помочь в диагностике при нарушениях менструального цикла\n\nДля начала работы необходимо ответить на несколько вопросов\nДля помощи введите команду /help")
    await message.answer(f"Введите дату начала последней менструации:\n<i>{"(В формате дд.мм.гггг)"}</i>",
        parse_mode=aiogram.enums.ParseMode.HTML, reply_markup=builder.as_markup())
    global isStartDate
    isStartDate = True

@router.callback_query(aiogram.F.data == "addstartinfo")
async def send_random_value(callback: aiogram.types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(aiogram.types.InlineKeyboardButton(
        text="Пропустить",
        callback_data="addperiodinfo")
    )
    global isStartDate
    global isPeriodDur
    isStartDate = False
    isPeriodDur = True
    await callback.message.answer(f"Введите продолжительность периода:\n<i>{"(Только количество дней)"}</i>",
        parse_mode=aiogram.enums.ParseMode.HTML, reply_markup=builder.as_markup())

@router.callback_query(aiogram.F.data == "addperiodinfo")
async def send_random_value(callback: aiogram.types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(aiogram.types.InlineKeyboardButton(
        text="Пропустить",
        callback_data="addcycleinfo")
    )
    global isPeriodDur
    global isCycleDur
    isPeriodDur = False
    isCycleDur = True
    await callback.message.answer(f"Введите продолжительность цикла:\n<i>{"(Только количество дней)"}</i>",
        parse_mode=aiogram.enums.ParseMode.HTML, reply_markup=builder.as_markup())

@router.callback_query(aiogram.F.data == "addcycleinfo")
async def send_random_value(callback: aiogram.types.CallbackQuery):
    global isCycleDur
    isCycleDur = False
    await callback.message.answer("Для помощи введите команду /help")

#ввод информации о цикле
@router.message(Command("addinfo"))
async def addinfo(message: aiogram.types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(aiogram.types.InlineKeyboardButton(
        text="Пропустить",
        callback_data="addperiodinfo")
    )
    await message.answer(f"Введите продолжительность периода:\n<i>{"(Только количество дней)"}</i>",
        parse_mode=aiogram.enums.ParseMode.HTML, reply_markup=builder.as_markup())
    global isPeriodDur
    isPeriodDur = True

#ввод информации
@router.message(aiogram.F.text)
async def info_last_day(message: aiogram.types.Message):
    global isStartDate
    global isPeriodDur
    global isCycleDur
    if (isStartDate):
        builder = InlineKeyboardBuilder()
        builder.add(aiogram.types.InlineKeyboardButton(
            text="Пропустить",
            callback_data="addperiodinfo")
        )
        format = r'\d\d-\d\d-\d{4}'
        if (not re.match(format, message.text)):
            await message.answer("Неверный формат ввода")
        else:
            await message.answer(f"Введите продолжительность периода:\n<i>{"(Только количество дней)"}</i>",
                parse_mode=aiogram.enums.ParseMode.HTML, reply_markup=builder.as_markup())
            isStartDate = False
            isPeriodDur = True
    elif (isPeriodDur):
        builder = InlineKeyboardBuilder()
        builder.add(aiogram.types.InlineKeyboardButton(
            text="Пропустить",
            callback_data="addcycleinfo")
        )
        if (not message.text.isdigit()):
            await message.answer("Неверный формат ввода")
        else:
            isPeriodDur = False
            isCycleDur = True
            await message.answer(f"Введите продолжительность цикла:\n<i>{"(Только количество дней)"}</i>",
                parse_mode=aiogram.enums.ParseMode.HTML, reply_markup=builder.as_markup())
    elif (isCycleDur):
        if(not message.text.isdigit()):
            await message.answer("Неверный формат ввода")
        else:
            isCycleDur = False
            await message.answer("Данные успешно сохранены\n\nДля помощи введите команду /help")
