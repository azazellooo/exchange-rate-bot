from telegram.ext import CommandHandler, CallbackContext
from telegram import Update

from base_bot import TelegramBot


class CommandsHandler(TelegramBot):
    def __init__(self, dispatcher):
        super(CommandsHandler, self).__init__()
        self.dispatcher = dispatcher
        self.add_handlers()

    def add_handlers(self):
        self.dispatcher.add_handler(CommandHandler('start', self.start))

    def start(self, update: Update, context: CallbackContext):
        pass
