from flask import Flask
from threading import Thread
import telebot
import json
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

# --- FLASK SERVERI (Render uchun) ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is running"

def run():
    app.run(host='0.0.0.0', port=8080)

t = Thread(target=run)
t.start()

# --- BOT SOZLAMALARI ---
BOT_TOKEN = "8512233110:AAEbVt0kZulqNgCGNzLl_HnIzUwtNLWLCGs"
bot = telebot.TeleBot("8512233110:AAEbVt0kZulqNgCGNzLl_HnIzUwtNLWLCGs")
ADMIN_ID = 8263438510

# --- BAZA BILAN ISHLASH ---
def load_json(file):
    if not os.path.exists(file): return {}
    with open(file, "r") as f:
        try: return json.load(f)
        except: return {}

def save_json(file, data):
    with open(file, "w") as f: json.dump(data, f, indent=4)

# --- BOT MENYULARI ---
@bot.message_handler(commands=['start'])
def start(message):
    db = load_json("users_db.json")
    uid = str(message.chat.id)
    if uid not in db:
        db[uid] = 0
        save_json("users_db.json", db)
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📱 Raqam sotib olish", "💰 Balans")
    if message.chat.id == ADMIN_ID: markup.add("⚙️ Admin Panel")
    bot.send_message(message.chat.id, "Axic Virtiumga xush kelibsiz!", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "💰 Balans")
def show_balance(message):
    db = load_json("users_db.json")
    balans = db.get(str(message.chat.id), 0)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💳 Pul yechish", callback_data="withdraw"))
    bot.send_message(message.chat.id, f"Sizning balansingiz: {balans} so'm", reply_markup=markup)

# --- ADMIN BUYRUQLARI ---
@bot.message_handler(commands=['add'])
def add_balance(message):
    if message.chat.id != ADMIN_ID: return
    try:
        _, user_id, summa = message.text.split()
        db = load_json("users_db.json")
        db[user_id] = db.get(user_id, 0) + int(summa)
        save_json("users_db.json", db)
        bot.send_message(user_id, f"✅ Balansingiz {summa} so'mga to'ldirildi!")
        bot.reply_to(message, "✅ Balans muvaffaqiyatli qo'shildi.")
    except: bot.reply_to(message, "❌ Format: /add [ID] [Summa]")

@bot.message_handler(commands=['setprice'])
def set_price(message):
    if message.chat.id != ADMIN_ID: return
    try:
        _, davlat, narx = message.text.split()
        prices = load_json("prices.json")
        prices[davlat] = int(narx)
        save_json("prices.json", prices)
        bot.reply_to(message, f"✅ {davlat} narxi {narx} so'mga o'zgartirildi!")
    except: bot.reply_to(message, "❌ Format: /setprice [Davlat] [Narx]")

# --- PUL YECHISH TIZIMI ---
@bot.callback_query_handler(func=lambda call: call.data == "withdraw")
def withdraw_req(call):
    bot.send_message(call.message.chat.id, "💳 Karta raqamingizni yuboring:")
    bot.register_next_step_handler(call.message, send_admin_request)

def send_admin_request(message):
    card = message.text
    bot.send_message(ADMIN_ID, f"⚠️ To'lov so'rovi:\nUser ID: {message.chat.id}\nKarta: {card}", 
                     reply_markup=InlineKeyboardMarkup().add(
                         InlineKeyboardButton("✅ To'landi", callback_data=f"pay_{message.chat.id}")))
    bot.reply_to(message, "✅ So'rovingiz adminga yuborildi.")

@bot.callback_query_handler(func=lambda call: call.data.startswith("pay_"))
def admin_pay(call):
    user_id = call.data.split("_")[1]
    bot.send_message(user_id, "🎉 Pul kartangizga o'tkazildi!")
    bot.edit_message_text("✅ To'landi deb belgilandi.", call.message.chat.id, call.message.message_id)

bot.infinity_polling()
