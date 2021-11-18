from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters
from telegram import Update, ReplyKeyboardMarkup
from bot.base_bot import TelegramBot
from .messages import *

FROM_CURRENCY, TO_CURRENCY, AMOUNT = range(3)


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

    @staticmethod
    def start_convert(update: Update, context: CallbackContext):
        print('start conversation')
        update.message.reply_text('send me alphabetic currency code: ')
        return FROM_CURRENCY

    def from_currency(self, update: Update, context: CallbackContext):
        from_currency = update.message.text.upper()
        if not self.source.allowed_currencies.get(from_currency):
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


class CommandsHandler(TelegramBot):
    def __init__(self, dispatcher):
        super(CommandsHandler, self).__init__()
        self.dispatcher = dispatcher
        self.add_handlers()


    def add_handlers(self):
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CommandHandler('latest', self.get_latest))

    def start(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        markup = ReplyKeyboardMarkup(keyboard=[
            ['/latest'],
            ['/convert'],
        ])
        self.send_message(recipient=chat_id, message=GREETING, keyboard=markup)

    def get_latest(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat.id
        latest_rates = self.source.get_latest_info()
        self.send_message(recipient=chat_id, message=latest_rates)
