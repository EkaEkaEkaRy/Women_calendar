import asyncio
import logging
import aiogram
import re
from aiogram.filters.command import Command, CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

#from config_reader import config

logging.basicConfig(level=logging.INFO)
#bot = aiogram.Bot(token=config.bot_token.get_secret_value())
bot = aiogram.Bot(token="TOKEN")

dp = aiogram.Dispatcher()

global isStartDate
global isPeriodDur
global isCycleDur
isStartDate = False
isPeriodDur = False
isCycleDur = False

#начало работы бота
@dp.message(Command("start"))
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

@dp.callback_query(aiogram.F.data == "addstartinfo")
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

@dp.callback_query(aiogram.F.data == "addperiodinfo")
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

@dp.callback_query(aiogram.F.data == "addcycleinfo")
async def send_random_value(callback: aiogram.types.CallbackQuery):
    global isCycleDur
    isCycleDur = False
    await callback.message.answer("Для помощи введите команду /help")

#ввод информации о цикле
@dp.message(Command("addinfo"))
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

#помощь по функциям бота
@dp.message(Command("help"))
async def help(message: aiogram.types.Message):
    await message.answer(f"Основные функции:\n\n<b>/info</b> - получить информацию о предстоящем цикле\n<b>/calendar</b> - календарь\n<b>/adddataperiod</b> - отметить начало или конец цикла\n<b>/addinfo</b> - добавить или изменить информацию о цикле",
        parse_mode=aiogram.enums.ParseMode.HTML)

#добавление информации о начале или конце периода
@dp.message(Command("adddataperiod"))
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

@dp.message(aiogram.F.text.lower() == "начало")
async def with_puree(message: aiogram.types.Message):
    await message.reply("Данные успешно сохранены")

@dp.message(aiogram.F.text.lower() == "конец")
async def without_puree(message: aiogram.types.Message):
    await message.reply("Данные успешно сохранены")

#получение информации о цикле
@dp.message(Command("info"))
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

#ввод информации
@dp.message(aiogram.F.text)
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



"""
@dp.message(Command("dice"))
async def cmd_dice(message: aiogram.types.Message):
    await message.answer_dice(emoji="🏀")
    print(message.from_user.full_name, message.from_user.url)

@dp.message(aiogram.F.text, Command("test"))
async def any_message(message: aiogram.types.Message):
    await message.answer(
        "Hello, <b>world</b>!",
        parse_mode=aiogram.enums.ParseMode.HTML
    )
    await message.answer(
        "Hello, *world*\!",
        parse_mode=aiogram.enums.ParseMode.MARKDOWN_V2
    )
"""
# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
