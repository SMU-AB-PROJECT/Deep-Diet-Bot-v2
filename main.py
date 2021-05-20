# pip install python-telegram-bot
# tensorflow version 2.4.1
# python ver 3.7x

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler  # import modules
import os


path = 'C:\\Users\\yoonho\\Desktop'
dir_now = os.path.dirname(os.path.abspath(path))  # real path to dirname


# message reply function
def get_message(update, context) :
    update.message.reply_text("got text")
    update.message.reply_text(update.message.text)


# help reply function
def help_command(update, context) :
    update.message.reply_text("무엇을 도와드릴까요?")

import time
# photo reply function
def get_photo(update, context) :
    file_path = os.path.join(dir_now, 'from_telegram.png')
    photo_id = update.message.photo[-1].file_id  # photo 번호가 높을수록 화질이 좋음
    photo_file = context.bot.getFile(photo_id)
    photo_file.download(file_path)
    update.message.reply_text('photo saved')

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    api_key = '1760236283:AAFcjOBmTOM8MPWNUZrhDfGN52-ToK4YAfw'
    print('start telegram chat bot')

    updater = Updater(api_key, use_context=True)

    message_handler = MessageHandler(Filters.text & (~Filters.command), get_message)  # 메세지중에서 command 제외
    updater.dispatcher.add_handler(message_handler)

    help_handler = CommandHandler('help', help_command)
    updater.dispatcher.add_handler(help_handler)

    photo_handler = MessageHandler(Filters.photo, get_photo)
    updater.dispatcher.add_handler(photo_handler)

    updater.idle()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
