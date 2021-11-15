from telegram.ext import CommandHandler, CallbackContext
from telegram import Update, ForceReply, ReplyKeyboardMarkup, KeyboardButton

from bot.base_bot import TelegramBot
from bot.sources import ExchangeRateApiSource
from settings import SOURCE_URL_BASE


class CommandsHandler(TelegramBot):
    def __init__(self, dispatcher):
        super(CommandsHandler, self).__init__()
        self.dispatcher = dispatcher
        self.add_handlers()
        self.source = ExchangeRateApiSource(base_url=SOURCE_URL_BASE)

    def add_handlers(self):
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CommandHandler('latest', self.get_latest))

    def start(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        markup = ReplyKeyboardMarkup(keyboard=[
            ['/latest'],
        ])
        self.send_message(recipient=chat_id, message='hello', keyboard=markup)

    def get_latest(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        latest_rates = self.source.get_latest_info()
        self.send_message(recipient=chat_id, message=latest_rates)
