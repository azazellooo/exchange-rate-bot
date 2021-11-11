from bot.bot_provider import ExchangeRateBotProvider


class BotInit:
    def __init__(self):
        self.bot = ExchangeRateBotProvider()

    def launch(self):
        self.bot.start_webhook()
