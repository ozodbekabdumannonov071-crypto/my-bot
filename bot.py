from flask import Flask
from threading import Thread
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import json
import os

# --- FLASK SERVERI ---
app = Flask('')
@app.route('/')
def home(): return "Bot is running"
def run(): app.run(host='0.0.0.0', port=8080)
Thread(target=run).start()

# --- SOZLAMALAR ---
BOT_TOKEN = "8512233110:AAEbVt0kZulqNgCGNzLl_HnIzUwtNLWLCGs"
CHANNEL_ID = "@A_ToolsX" # Kanal manzilingiz
ADMIN_ID = 8263438510
bot = telebot.TeleBot(BOT_TOKEN)

# --- FUNKSIYALAR ---
def check_sub(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except: return False

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📱 Raqam sotib olish", "💰 Balans")
    markup.add("⚙️ Admin Panel")
    return markup

# --- BUYRUQLAR ---
@bot.message_handler(commands=['start'])
def start(message):
    if not check_sub(message.chat.id):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅ Obuna bo'lish", url=f"https://t.me/{CHANNEL_ID[1:]}"))
        bot.send_message(message.chat.id, "Botdan foydalanish uchun kanalga obuna bo'ling:", reply_markup=markup)
        return
    
    bot.send_message(message.chat.id, "Axic Virtiumga xush kelibsiz!", reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "💰 Balans")
def balans(message):
    bot.send_message(message.chat.id, "Sizning balansingiz: 0 so'm")

@bot.message_handler(func=lambda m: m.text == "📱 Raqam sotib olish")
def sotib_olish(message):
    bot.send_message(message.chat.id, "Raqamlar menyusi ochildi...")

@bot.message_handler(func=lambda m: m.text == "⚙️ Admin Panel")
def admin_panel(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Admin panel: /add [ID] [Summa] yoki /setprice [Davlat] [Narx]")
    else:
        bot.send_message(message.chat.id, "Siz admin emassiz!")

bot.infinity_polling()
