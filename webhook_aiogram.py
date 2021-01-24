import logging

import ssl

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.webhook import SendMessage
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.executor import start_webhook

from config import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


class Proba(StatesGroup):
    START = State()
    SECOND = State()
    FIN = State()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    logging.info('start command!')
    await Proba.START.set()
    await message.reply("Hi there! Yahho!")
#    link_info = await get_start_link(x)  # result: 'https://t.me/MyBot?start=foo'
#    print(link_info, x)
#    print(message.text)
#    await bot.send_message(message.from_user.id, phrases[state]['text'], reply_markup=get_keyboard(state))


@dp.message_handler(state=Proba.START)
async def echo(message: types.Message, state: FSMContext):
    cur_state = await state.get_state()
    logging.info(f' cur state = {cur_state}')

    async with state.proxy() as data:
        logging.info(f'message! {message.text}')
        data['saved'] = message.text

    await Proba.SECOND.set()

    return SendMessage(message.chat.id, message.text)


@dp.message_handler(state=Proba.SECOND)
async def echo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        prev = data['saved']
        logging.info(f'message! {message.text}')
        data['saved'] = message.text

    await Proba.FIN.set()

    return SendMessage(message.chat.id, prev)


@dp.message_handler(state=Proba.FIN)
async def echo(message: types.Message, state: FSMContext):
    cur_state = await state.get_state()
    logging.info(f' cur state = {cur_state}')
    if cur_state is None:
        return

    return SendMessage(message.chat.id, 'FIN!')



async def on_startup(dp):
    logging.info(f"set webhook - {WEBHOOK_URL_BASE} + {WEBHOOK_URL_PATH}")
    await bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, 'r'))
    # insert code here to run it after start


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':

    context = ssl.SSLContext()
    context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

    logging.info(f"start_webhook: {WEBAPP_HOST}:{WEBAPP_PORT}/{WEBHOOK_PATH}")

    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=False,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
        ssl_context=context,
        )
