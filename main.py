from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from pprint import pprint as print
from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
key = os.getenv("key")
url =  f"https://v6.exchangerate-api.com/v6/{key}/pair/usd/uzs"

# tugmalar 
button = KeyboardButton("Dollar kursi")
button2 = KeyboardButton("Rubl kursi")
keyboard = ReplyKeyboardMarkup([[button, button2]], resize_keyboard=True)

# start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Maskur bot orqali siz dollarning va rublning so'mga nisbatan kursini bilib olishingiz mumkin.",
        reply_markup=keyboard)

# dollar kursi tugmasi bosilganda
async def dollar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get(url)
    data = response.json()  
    if response.status_code == 200:
        dollar_kursi = data['conversion_rate']
        await update.message.reply_text(f"1 USD = {dollar_kursi} UZS")
    else:
        await update.message.reply_text("Kursni olishda xatolik yuz berdi.")
# rubl kursi tugmasi bosilganda
async def rubl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url_rubl = "https://v6.exchangerate-api.com/v6/11286813c9fa5ce8bab61e03/pair/rub/uzs"
    response = requests.get(url_rubl)
    data = response.json()  
    if response.status_code == 200:
        rubl_kursi = data['conversion_rate']
        await update.message.reply_text(f"1 RUB = {rubl_kursi} UZS")
    else:
        await update.message.reply_text("Kursni olishda xatolik yuz berdi.")    
    
# botni ishga tushirish
def main():
    app = ApplicationBuilder().token(API_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^Dollar kursi$"), dollar))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^Rubl kursi$"), rubl))

    app.run_polling()

if __name__ == "__main__":
    main()