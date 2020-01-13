import logging
import os
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import re


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

token = os.environ['TOKEN']


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def get_url():
    contents = requests.get('https://random.dog/woof.json').json()    
    url = contents['url']
    return url


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


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
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop', bop))
    dp.add_handler(CommandHandler('hello', hello))
    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
