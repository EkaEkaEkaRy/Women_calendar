import re
import aiogram
from aiogram.filters.command import Command, CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
#from apscheduler.schedulers.asyncio import AsyncIOScheduler
import my_token

from .bd import create_user_users, add_info_period, add_info_cycle, db_start

router = aiogram.Router()


global isStartDate
global isPeriodDur
global isCycleDur
isStartDate = False
isPeriodDur = False
isCycleDur = False

# scheduler = AsyncIOScheduler(timezone='utc')
bot = aiogram.Bot(token=my_token.my_token)
async def remind():
    await bot.send_message(chat_id=954353874, text="Хей🖖 не забудь выбрать свой ужин сегодня")


# подключение к базе данных (или ее создание, если не существует)
async def on_startup(_):
    await db_start()


# начало работы бота
@router.message(Command("start"))
async def cmd_start(message: aiogram.types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(aiogram.types.InlineKeyboardButton(
        text="Пропустить",
        callback_data="addstartinfo")
    )
    await create_user_users(message.from_user.id)
    await message.answer("Этот календарь помогает: \n🌸 определить регулярность цикла\n🌸 прогнозировать дату ожидаемых месячных и дни овуляции\n🌸 помочь в диагностике при нарушениях менструального цикла\n\nДля начала работы необходимо ответить на несколько вопросов\nДля помощи введите команду /help")
    await message.answer(f"Введите дату начала последней менструации:\n<i>{'(В формате дд.мм.гггг)'}</i>",
        parse_mode=aiogram.enums.ParseMode.HTML, reply_markup=builder.as_markup())
    global isStartDate
    isStartDate = True
    #scheduler.add_job(remind(), 'cron', day_of_week='mon-sun', hour=13, minute=50, end_date='3025-10-13')


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
    await callback.message.answer(f"Введите продолжительность периода:\n<i>{'(Только количество дней)'}</i>",
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
    await callback.message.answer(f"Введите продолжительность цикла:\n<i>{'(Только количество дней)'}</i>",
        parse_mode=aiogram.enums.ParseMode.HTML, reply_markup=builder.as_markup())


@router.callback_query(aiogram.F.data == "addcycleinfo")
async def send_random_value(callback: aiogram.types.CallbackQuery):
    global isCycleDur
    isCycleDur = False
    await callback.message.answer("Для помощи введите команду /help")


# ввод информации о цикле
@router.message(Command("addinfo"))
async def addinfo(message: aiogram.types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(aiogram.types.InlineKeyboardButton(
        text="Пропустить",
        callback_data="addperiodinfo")
    )
    await message.answer(f"Введите продолжительность периода:\n<i>{'(Только количество дней)'}</i>",
        parse_mode=aiogram.enums.ParseMode.HTML, reply_markup=builder.as_markup())
    global isPeriodDur
    isPeriodDur = True


# ввод информации
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
        format = r'\d\d.\d\d.\d{4}'
        if (not re.match(format, message.text)):
            await message.answer("Неверный формат ввода")
        else:
            #добавление даты в бд
            await message.answer(f"Введите продолжительность периода:\n<i>{'(Только количество дней)'}</i>",
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
            #добавление периода в бд
            isPeriodDur = False
            isCycleDur = True
            await message.answer(f"Введите продолжительность цикла:\n<i>{'(Только количество дней)'}</i>",
                parse_mode=aiogram.enums.ParseMode.HTML, reply_markup=builder.as_markup())
            await add_info_period(user_id=message.from_user.id, period_length=message.text)
    elif (isCycleDur):
        if(not message.text.isdigit()):
            await message.answer("Неверный формат ввода")
        else:
            #добавление цикла в бд
            isCycleDur = False
            await message.answer("Данные успешно сохранены\n\nДля помощи введите команду /help")
            await add_info_cycle(user_id=message.from_user.id, cycle_length=message.text)
