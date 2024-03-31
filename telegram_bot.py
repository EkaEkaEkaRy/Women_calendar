import asyncio
import logging
import aiogram
import my_token
from routers import help,start_end_info, post_info, calendar, bd
from apscheduler.schedulers.asyncio import AsyncIOScheduler
#from config_reader import config


async def main():
    bot = aiogram.Bot(token=my_token.my_token)
    dp = aiogram.Dispatcher()
    dp.include_routers(help.router, calendar.router, start_end_info.router, post_info.router)
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())