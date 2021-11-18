from telegram import Bot
from telegram.ext import Updater
from telegram.utils.request import Request

from bot.sources import ExchangeRateApiSource
from settings import TOKEN, LISTEN_WEBHOOK, WEBHOOK_PORT, SOURCE_URL_BASE


class TelegramBot:
    def __init__(self):
        self.request = Request(con_pool_size=9, read_timeout=1.0, connect_timeout=0.5)
        self.bot = Bot(request=self.request, token=TOKEN)
        self.updater = Updater(bot=self.bot, use_context=True)
        self.source = ExchangeRateApiSource(base_url=SOURCE_URL_BASE)

    def start_webhook(self):
        url = f'{LISTEN_WEBHOOK}/{TOKEN}'
        self.updater.start_webhook(listen='0.0.0.0', port=WEBHOOK_PORT, url_path=TOKEN,  webhook_url=url)

    def send_message(self, recipient, message, keyboard=None, parse_mode=None, *args):
        self.bot.send_message(chat_id=recipient, text=message, reply_markup=keyboard, parse_mode=parse_mode)
