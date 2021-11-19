from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackContext

from bot.base_bot import TelegramBot

FROM_CURRENCY, TO_CURRENCY, AMOUNT = range(3)
FROM_CRYPTO = range(1)


class ConversationsHandler(TelegramBot):
    def __init__(self, dispatcher):
        super(ConversationsHandler, self).__init__()
        self.dispatcher = dispatcher

        self.add_handlers()

    def add_handlers(self):
        self.dispatcher.add_handler(ConversationHandler(
            entry_points=[CommandHandler('convert', self.start_convert)],
            states={
                FROM_CURRENCY: [MessageHandler(Filters.text, self.from_currency, pass_user_data=True)],
                TO_CURRENCY: [MessageHandler(Filters.text, self.to_currency, pass_user_data=True)],
                AMOUNT: [MessageHandler(Filters.text, self.amount, pass_user_data=True)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        ))
        self.dispatcher.add_handler(ConversationHandler(
            entry_points=[CommandHandler('crypto', self.start_crypto)],
            states={
                FROM_CRYPTO: [MessageHandler(Filters.text, self.from_crypto)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        ))

    @staticmethod
    def start_convert(update: Update, context: CallbackContext):
        print('start conversation')
        update.message.reply_text('send me alphabetic currency code: ')
        return FROM_CURRENCY

    def from_currency(self, update: Update, context: CallbackContext):
        from_currency = update.message.text.upper()
        if not self.source.allowed_currencies.get(from_currency) and from_currency != '/cancel':
            update.message.reply_text('no such currency code, try again: ')
            return FROM_CURRENCY
        context.user_data['from_curr'] = from_currency
        update.message.reply_text('send me second alphabetic currency code: ')
        print(context.user_data)
        return TO_CURRENCY

    def to_currency(self, update: Update, context: CallbackContext):
        to_currency = update.message.text.upper()
        if not self.source.allowed_currencies.get(to_currency):
            update.message.reply_text('no such currency, try again: ')
            return TO_CURRENCY
        context.user_data['to_curr'] = to_currency
        update.message.reply_text('amount?')
        return AMOUNT

    def amount(self, update: Update, context: CallbackContext):
        amount = update.message.text
        if not amount.isdigit():
            update.message.reply_text('please, send me number ')
            return AMOUNT
        result = self.source.convert_currency(
            curr_from=context.user_data.get('from_curr'),
            curr_to=context.user_data.get('to_curr'),
            amount=int(amount)
        )
        update.message.reply_text(result)
        return ConversationHandler.END

    def cancel(self, update: Update, context: CallbackContext):
        update.message.reply_text('Bye! I hope we can talk again some day.')
        return ConversationHandler.END

    @staticmethod
    def start_crypto(update: Update, context: CallbackContext):
        print('start crypto conversation')
        update.message.reply_text('send me alphabetic crypto code: ')
        return FROM_CRYPTO

    def from_crypto(self, update: Update, context: CallbackContext):
        crypto_code = update.message.text.upper()
        if not self.source.allowed_cryptos.get(crypto_code):
            update.message.reply_text('no such cryptocurrency, try again: ')
            return FROM_CRYPTO
        result = self.source.get_latest_crypto_rate(crypto_code)
        update.message.reply_text(result)
        return ConversationHandler.END

