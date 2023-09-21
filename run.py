import os
import django
from aiogram import Bot, Dispatcher
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loader import bot
from data_import.add_data import add_postgres_users, add_postgres_category,\
    add_postgres_subcategory, add_postgres_manufacturer, add_postgres_item, add_postgres_invoices


def set_scheduled_jobs(scheduler, *args, **kwargs):

    # scheduler.add_job(add_postgres_category, "interval", seconds=20)
    # scheduler.add_job(add_postgres_manufacturer, "interval", seconds=20)
    # scheduler.add_job(add_postgres_users, "interval", seconds=20)
    # scheduler.add_job(add_postgres_subcategory, "interval", seconds=60)
    # scheduler.add_job(add_postgres_item, "interval", seconds=100)
    scheduler.add_job(add_postgres_invoices, "interval", seconds=60)


async def on_startup(dp):
    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)


def start_schudeler():
    scheduler = AsyncIOScheduler()
    set_scheduled_jobs(scheduler)
    try:
        return scheduler.start()
    except Exception as exx:
        print(exx)

    
async def on_shutdown(dp):
    await dp.storage.close()
    await dp.storage.wait_closed()


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "core.settings"
    )
    os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})
    django.setup()


if __name__ == '__main__':
    setup_django()

    from aiogram.utils import executor
    from loader import bot
    from handlers import dp
    start_schudeler()

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
