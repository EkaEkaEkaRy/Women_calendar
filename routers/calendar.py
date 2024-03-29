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
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}',
        )



