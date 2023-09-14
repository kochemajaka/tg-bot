
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters
import config28
import db_sql

class tg_bot:
    def __init__(self):
        self.updater = Updater(token=config28.API_TOKEN)
        self.dispatcher = self.updater.dispatcher
        self.dbase = config28.DBase()
        # обработчик команды '/start'
        start_handler = CommandHandler('start', self.func_start)
        self.dispatcher.add_handler(start_handler)

        # обработчик текстовых сообщений
        text_handler = MessageHandler(Filters.text & (~Filters.command), self.func_text)
        self.dispatcher.add_handler(text_handler)

        # обработчик команды '/find'
        find_handler = CommandHandler('find', self.func_find)
        self.dispatcher.add_handler(find_handler)

        # обработчик команды '/addata
        addata_handler = CommandHandler('adddata', self.func_addata)
        self.dispatcher.add_handler(adddata_handler)

        # обработчик команды '/delete'
        delete_handler = CommandHandler('delete', self.func_delete)
        self.dispatcher.add_handler(delete_handler)

        # обработчик не распознанных команд
        unknown_handler = MessageHandler(Filters.command, self.func_unknown)
        self.dispatcher.add_handler(unknown_handler)

        # запуск прослушивания сообщений
        self.updater.start_polling()
        # обработчик нажатия Ctrl+C
        self.updater.idle()

    def about(self):
        return "Для извлечения исходных данных используйте команды:" \
           "/find word, где word - слово из фразы, которую нужно найти;" \
           "/adddata index, где index - номер параметра в таблице производителей" \
           "/delete index,"

    # функция обработки команды '/start'
    def func_start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
            text="Бот")

    # функция обработки текстовых сообщений
    def func_text(self, update, context):
        text_out = 'Получено сообщение: ' + update.message.text + '\n' + self.about()
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_out)

    # функция обработки команды '/find'
    def func_find(self, update, context):
        if context.args:
            text_reply = self.dbase.get_navigator_data(context.args[0])
            context.bot.send_message(chat_id=update.effective_chat.id,
                text=text_reply)
            return 1
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                text='Необходимо указать аргумент команды /find')
            return -1

    # функция обработки команды '/vendors'
    def func_vendors(update, context):
        if context.args:
            text_reply = "Команда вызвана с первым параметром " + context.args[0]
            context.bot.send_message(chat_id=update.effective_chat.id,
                text=text_reply)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                text='Необходимо указать аргумент команды /vendors')

    # функция обработки не распознанных команд
    def func_unknown(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
            text="Введена неизвестная команда!(")

if __name__ == '__main__':
    new_bot = tg_bot()