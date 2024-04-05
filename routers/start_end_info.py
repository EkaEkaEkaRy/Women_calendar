import aiogram
from aiogram.filters.command import Command, CommandStart
from .bd import create_user_cycles, start_date, end_date, cycle_start
from datetime import date
from datetime import datetime
#from .calendar import date_period

from routers.telegram_calendar import simple_calendar
from routers.telegram_calendar import common
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from datetime import datetime




router = aiogram.Router()

global date_period_from_calendar
date_period_from_calendar = None

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

#нажатие кнопкок на календаре
@router.callback_query(simple_calendar.SimpleCalendarCallback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData):
    calendar = simple_calendar.SimpleCalendar(
        locale=await common.get_user_locale(callback_query.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime(2000, 1, 1), datetime(2100, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
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
        await callback_query.message.answer("Начало менструации?", reply_markup=keyboard)
        global date_period_from_calendar
        date_period_from_calendar = date.strftime("%d.%m.%Y")
        print(date_period_from_calendar)


@router.message(aiogram.F.text.lower() == "начало")
async def with_puree(message: aiogram.types.Message):
    global date_period_from_calendar
    # если дата выбрана на календаре
    if date_period_from_calendar != None:
        # добавление даты из date_period_from_calendar в бд
        # date_period_from_calendar это переменная в которой хранится дата выбранная в календаре
        print(date_period_from_calendar)
        date_period_from_calendar = None
    # иначе дата берется сегодняшняя
    else:
        print(date.today().strftime("%d.%m.%Y"))
        # добавление даты в бд
        current_date_time = date.today().strftime("%Y-%m-%d")
        await start_date(user_id=message.from_user.id, start=current_date_time)
        await message.reply("Данные успешно сохранены")
        global starting
        starting = current_date_time

@router.message(aiogram.F.text.lower() == "конец")
async def without_puree(message: aiogram.types.Message):
    global date_period_from_calendar
    if date_period_from_calendar != None:
        # добавление даты из date_period в бд
        # date_period это переменная в которой хранится дата выбранная в календаре
        print(date_period_from_calendar)
        date_period_from_calendar = None
    else:
        print(date.today().strftime("%d.%m.%Y"))
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

