import asyncio

from aiogram import Dispatcher, Bot
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.storage.memory import MemoryStorage

from middlewares import ResponseMiddleware
from routers import routers

bot = Bot(token="...")

storage = MemoryStorage()


dp = Dispatcher(storage=storage, fsm_strategy=FSMStrategy.USER_IN_CHAT)


async def main():
    dp.include_routers(*routers)
    dp.update.middleware(ResponseMiddleware())
    await dp.start_polling(bot)


asyncio.run(main())
