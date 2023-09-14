import telebot
TOKEN = "1982450546:AAHlsy4LeqGdybw4cJoMdiVIAosrAcomoSo"
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
     bot.infinity_polling()
