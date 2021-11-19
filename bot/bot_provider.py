from bot.base_bot import TelegramBot
from bot.handlers.commands import CommandsHandler
from bot.handlers.conversations import ConversationsHandler


class ExchangeRateBotProvider(TelegramBot):
    def __init__(self):
        super(ExchangeRateBotProvider, self).__init__()
        self.dispatcher = self.updater.dispatcher
        self.add_handlers()

    def add_handlers(self):
        CommandsHandler(self.dispatcher)
        ConversationsHandler(self.dispatcher)
