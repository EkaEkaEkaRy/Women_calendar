import re
import aiogram
from aiogram.filters.command import Command, CommandStart
#from telegram_calendar import SimpleCalendar, SimpleCalendarCallback, DialogCalendar, DialogCalendarCallback, get_user_locale
from routers.telegram_calendar import simple_calendar
from routers.telegram_calendar import common
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from datetime import datetime

from .bd import sel1, sel2, delet, select_periops_info

router = aiogram.Router()

@router.message(Command("calendar"))
async def calendar(message: aiogram.types.Message):
    periods = await select_periops_info(message.from_user.id)
    print(periods)
    await message.answer(
        "Календарь",
        reply_markup=await simple_calendar.SimpleCalendar(locale=await common.get_user_locale(message.from_user)).start_calendar(periods)
    )

@router.message(Command("sel"))
async def cmd_start(message: aiogram.types.Message):
    await sel1()
    print('\n***************************************\n')
    await sel2()

