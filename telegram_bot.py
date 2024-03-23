import asyncio
import logging
import aiogram
import re
from aiogram.filters.command import Command
#from config_reader import config

logging.basicConfig(level=logging.INFO)
#bot = aiogram.Bot(token=config.bot_token.get_secret_value())
bot = aiogram.Bot(token="1417403958:AAHzkxdVS3AtrKl74w1186iSbzFNCDi5n38")

dp = aiogram.Dispatcher()



@dp.message(Command("start"))
async def cmd_start(message: aiogram.types.Message):
    await message.answer("Этот календарь помогает: \n🌸 определить регулярность цикла\n🌸 прогнозировать дату ожидаемых месячных и дни овуляции\n🌸 помочь в диагностике при нарушениях менструального цикла\n\nДля начала работы необходимо ответить на несколько вопросов")
    await message.answer(f"Начало последней менструации:\n<i>{"(В формате дд.мм.гггг)"}</i>",
        parse_mode=aiogram.enums.ParseMode.HTML)
    @dp.message(aiogram.F.text)
    async def info_last_day(message: aiogram.types.Message):
        format = '\d\d-\d\d-\d{4}'
        print(re.match(format, message.text))
        print(re.match(message.text, format))
        if (not re.fullmatch(format, message.text)):
            print(3)
            message.answer("Неверный формат ввода")
            print(4)
            while (not re.fullmatch(format, message.text)):
                @dp.message(aiogram.F.text)
                async def info_last_days(message: aiogram.types.Message):
                    print(message.text)
                    print(7)
        print(8)
        print(message.text)
        print(9)




@dp.message(Command("dice"))
async def cmd_dice(message: aiogram.types.Message):
    await message.answer_dice(emoji="🏀")
    print(message.from_user.full_name, message.from_user.url)


"""
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