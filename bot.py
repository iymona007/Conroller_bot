import telebot
import re
from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask, request


BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bizning ilk botimizga xush keldingiz!")

def link(text):
    return re.search(r'(https|http|t.me)', text)

bad_words = ['jinni', 'ahmoq','yaramas', 'dumb', 'stupid', 'idiot', 'fool', 'silly', 'moron', 'jerk', 'loser', 'dork', 'twit', 'buffoon', 'clown', 'cretin', 'imbecile']  

@bot.message_handler(func=lambda message: True)
def check_message(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text

    member = bot.get_chat_member(chat_id, user_id)
    is_admin = member.status in ['administrator', 'creator']

    if text and link(text):
        if not is_admin:
            bot.delete_message(chat_id, message.message_id)
            bot.send_message(chat_id, f"{message.from_user.first_name}, siz havfsiz link yuborishingiz mumkin emas!")

    if text:
        for bad_word in bad_words:
            if bad_word in text.lower():
                bot.delete_message(chat_id, message.message_id)

@bot.message_handler(content_types=["new_chat_members", "left_chat_member"])
def delete_join_leave_messages(message):
    bot.delete_message(message.chat.id, message.message_id)

@app.route('/webhook', methods=['POST'])
def webhook():  
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url='https://bot-t6re.onrender.com/webhook')
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))