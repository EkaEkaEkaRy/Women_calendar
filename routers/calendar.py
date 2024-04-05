import re
import aiogram
from aiogram.filters.command import Command, CommandStart
#from telegram_calendar import SimpleCalendar, SimpleCalendarCallback, DialogCalendar, DialogCalendarCallback, get_user_locale
from routers.telegram_calendar import simple_calendar
from routers.telegram_calendar import common
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from datetime import datetime

router = aiogram.Router()
global date_period
date_period = None

@router.message(Command("calendar"))
async def calendar(message: aiogram.types.Message):
    await message.answer(
        "Календарь",
        reply_markup=await simple_calendar.SimpleCalendar(locale=await common.get_user_locale(message.from_user)).start_calendar()
    )


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
        global date_period
        date_period = date.strftime("%d.%m.%Y")
        print(date_period)



