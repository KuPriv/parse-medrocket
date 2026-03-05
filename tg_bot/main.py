import asyncio
import logging
import subprocess
import os
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config_bot import token, my_id

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher()

stop_event = asyncio.Event()


def run_parser():
    parser_path = os.path.join(os.path.dirname(__file__), "..", "try_to_parse.py")
    subprocess.run([sys.executable, parser_path])
    logging.info("Парсер отработал")


async def check_file():
    while not stop_event.is_set():
        try:
            with open("status_indicator.txt", mode="r", encoding="utf-8") as file:
                check = file.read().strip()

            if check:
                logging.info("Отправили сообщение.")
                await send_message(check)
                stop_event.set()
                return

        except Exception as e:
            logging.error(f"Ошибка чтения файла: {e}")

        await asyncio.sleep(10)


async def send_message(s: str):
    await bot.send_message(chat_id=my_id, text=f"Пора проверить МедРокет! {s}")


@dp.message(Command("check"))
async def check_work(message: types.Message):
    await bot.send_message(chat_id=my_id, text="Подход, подход, еще подход.")


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_parser, "interval", minutes=15)
    scheduler.start()
    logging.info("Планировщик запущен. Каждые 15 минут будет запускаться парсер")

    asyncio.create_task(check_file())
    polling_task = asyncio.create_task(dp.start_polling(bot))

    await stop_event.wait()

    scheduler.shutdown()

    dp.stop_polling()

    try:
        await polling_task
    except asyncio.CancelledError:
        pass

    logging.info("Бот остановлен корректно")


if __name__ == "__main__":
    asyncio.run(main())
