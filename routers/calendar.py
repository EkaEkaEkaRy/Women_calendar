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


