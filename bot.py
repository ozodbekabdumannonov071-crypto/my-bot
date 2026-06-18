from flask import Flask
from threading import Thread
import telebot # yoki siz qaysi kutubxonani ishlatsangiz

app = Flask('')

@app.route('/')
def home():
    return "Bot is running"

def run():
    app.run(host='0.0.0.0', port=8080)

t = Thread(target=run)
t.start()

# --- Bu yerdan pastga o'zingizning bot kodingizni yozing ---
bot = telebot.TeleBot("8512233110:AAEbVt0kZulqNgCGNzLl_HnIzUwtNLWLCGs")
# ... va qolgan qismi ...
