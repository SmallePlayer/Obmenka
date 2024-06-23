import telebot
from telebot import types
from ultralytics import YOLO

model = YOLO(r'C:\Models\Ovoshi\weights\best.pt')
bot = telebot.TeleBot('7028879480:AAFQ6yAOwFo9TKqMceH-gQr88lB-SlTn1u4')

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name} ')

@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, message)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    markup = types.InlineKeyboardMarkup()
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    save_path = 'photo.jpg'
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    btn1 = types.InlineKeyboardButton('Задетектить обьекты', callback_data='detect')
    markup.row(btn1)
    bot.reply_to(message, 'Что пожелаете сделать с фоткой?.', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback_data: True)
def callback_detect(callback):
    if callback.data == 'detect':
        results = model('photo.jpg')
        #model.predict('photo.jpg', save=True, imgsz=320, conf=0.5)
        for result in results:
            boxes = result.boxes  # Boxes object for bounding box outputs
            masks = result.masks  # Masks object for segmentation masks outputs
            keypoints = result.keypoints  # Keypoints object for pose outputs
            probs = result.probs  # Probs object for classification outputs
            result.save(filename='result.jpg')
        file = open('result.jpg', 'rb')
        bot.send_photo(callback.message.chat.id, file)

@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name} ')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')

#bot.polling(none_stop=True)
bot.infinity_polling()