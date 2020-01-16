#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards.
"""
import logging
import os

import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from config import base_url
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

token = os.environ['INFORMMTPH_TOKEN']


def start(update, context):
    keyboard = [[InlineKeyboardButton("dnses", callback_data='1'),
                 InlineKeyboardButton("servers", callback_data='2')],

                [InlineKeyboardButton("diffs", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    if query.data == str(1):
        response = requests.get(f'{base_url}cloud/get-all-dns')
        ips = response.json()
        text = str()
        for ip in ips['dnses']:
            text += f"{ip['Value']}\n"
        query.edit_message_text(text=f"ips: \n {text}")
    if query.data == str(2):
        response = requests.get(f'{base_url}cloud/get-all-servers')
        drops = response.json()
        text = str()
        for drop in drops:
            text += f"{drop}\n"
        query.edit_message_text(text=f"{text}")
    if query.data == str(3):
        dnses = requests.get(f'{base_url}cloud/get-all-dns')
        servers = requests.get(f'{base_url}cloud/get-all-servers')
        dns_ips = [dns['Value'] for dns in dnses.json()['dnses']]
        server_ips = [server['ip'] for server in servers.json()]
        diff = list(set(server_ips) - set(dns_ips))
        query.edit_message_text(text=f"ips: \n {diff}")


def help(update, context):
    update.message.reply_text("Use /start to test this bot.")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def add_ip_to_dns(update, context):
    chat_id = update.message.chat_id
    print(chat_id)
    print(context.args)
    url = f'{base_url}cloud/change-dns'
    data = {
        'action': 'add',
        'new_ip': context.args[0]
    }
    response = requests.post(url, data)
    update.message.reply_text(f"response: {response}")


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler("adns", add_ip_to_dns,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
