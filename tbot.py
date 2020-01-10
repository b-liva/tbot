import os
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import re

token = os.environ['TOKEN']


def get_url():
    contents = requests.get('https://random.dog/woof.json').json()    
    url = contents['url']
    return url


def bop(bot, update):
    url = get_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)


def hello(bot, update):
    chat_id = update.message.chat_id
    # update.message.reply_text('Hello {}'.format(update.message.from_user.first_name))
    print(bot.username())
    bot.send_message(chat_id, f'hello from {bot.username()}')


def main():
    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop', bop))
    dp.add_handler(CommandHandler('hello', hello))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
