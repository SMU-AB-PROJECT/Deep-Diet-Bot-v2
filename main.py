# pip install python-telegram-bot
# tensorflow version 2.5
# python ver 3.9

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler  # import modules
import os
from load_model import load_model,predict_output
import tensorflow as tf
import DBModel
import time

'''파일이 저장될 directory: 환경에 맞는 경로 수정 필요'''
path = 'C:\\deepdiet-files\\'
dir_now = os.path.dirname(os.path.abspath(path))  # real path to dirname

'''DB 모델 생성'''
dbm = DBModel.DBModel()

'''전역변수 정의'''
eatTime='처음'

'''Handler 정의'''
# reply username
def get_message(update, context) :
    global eatTime
    req = update.message.text
    print('req: ', req)

    if (req == '아침') or (req == '점심') or (req == '저녁'):
        eatTime = req
        update.message.reply_text("{}에 먹은 음식 사진을 보내주세요.".format(eatTime))
        print('get eat time: {}'.format(eatTime))

    elif req.count('오늘') > 0:
        username = update.message.from_user.first_name
        userdate = '2021-05-21'
        foodlist = dbm.selectByNameDate(username, userdate)

        print(foodlist)
        update.message.reply_text("오늘 먹은 음식은 {}, {}, {} 입니다."
                                  .format(foodlist[0], foodlist[1], foodlist[2]))
    else:
        # hello username
        update.message.reply_text("hello " + update.message.from_user.first_name)

# photo reply function
def get_photo(update, context) :
    global eatTime
    userdate = '2021-05-21' # 추후 동적으로 수정
    # 먹은 시간 설정 안돼있으면 먹은 시간 요청
    if not ((eatTime == '아침') or (eatTime == '점심') or (eatTime == '저녁')):
        update.message.reply_text('먹은 시간을 알려주세요. (아침/점심/저녁)')
        return

    file_path = os.path.join(path, 'from_telegram.png')
    photo_id = update.message.photo[-1].file_id  # photo 번호가 높을수록 화질이 좋음
    photo_file = context.bot.getFile(photo_id)
    photo_file.download(file_path)
    time.sleep(1.)


    print('먹은 시간: ' + eatTime)
    if os.path.isfile(path + 'from_telegram.png'):
        foodname = labels_list[predict_output(model, path+'from_telegram.png')]
        #foodname = labels_list[label]
        update.message.reply_text('{}에 먹은 음식은 {}입니다.'.format(eatTime, foodname))
        print(eatTime)

        username = update.message.from_user.first_name

        if eatTime == '아침':
            dbm.insert(username, userdate, 'breakfast', foodname)
            print('database 저장 완료.')
        elif eatTime == '점심':
            dbm.insert(username, userdate, 'lunch', foodname)
            print('database 저장 완료.')
        elif eatTime == '저녁':
            dbm.insert(username, userdate, 'dinner', foodname)
            print('database 저장 완료.')
        else:
            update.message.reply_text('다시 보내주세요.')

    else:
        update.message.reply_text('다시 보내주세요.')
        print('Image is not found!')

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.



if __name__ == '__main__':
    api_key = '1760236283:AAFcjOBmTOM8MPWNUZrhDfGN52-ToK4YAfw'
    labels_list = ['Grilled Mackerel', 'bibimbap', 'fish sushi', 'fruit salad', 'gimbap', 'jajangmyeon', 'miyeokguk',
                   'ramen', 'seolleongtang', 'spaghetti', 'tteokbokki', 'tteokguk']
    model = load_model()
    print('start telegram chat bot')

    updater = Updater(api_key, use_context=True)

    '''handler 매칭'''
    # 메시지 응답
    message_handler = MessageHandler(Filters.text & (~Filters.command), get_message)
    updater.dispatcher.add_handler(message_handler)

    # 사진 파일 응답
    photo_handler = MessageHandler(Filters.photo, get_photo)
    updater.dispatcher.add_handler(photo_handler)

    updater.start_polling(timeout=3, clean=True)
    updater.idle()
