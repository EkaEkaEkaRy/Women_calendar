import aiogram
from aiogram.filters.command import Command, CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = aiogram.Router()
#помощь по функциям бота
@router.message(Command("help"))
async def help(message: aiogram.types.Message):
    await message.answer(f"Основные функции:\n\n<b>/info</b> - получить информацию о предстоящем цикле\n<b>/calendar</b> - календарь\n<b>/adddataperiod</b> - отметить начало или конец цикла\n<b>/addinfo</b> - добавить или изменить информацию о цикле",
        parse_mode=aiogram.enums.ParseMode.HTML)
    print(message.from_user.id)
    print(message.from_user.username)
    print(message.text)
