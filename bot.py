import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Replace with your bot token
BOT_TOKEN = "7879631782:AAHgMBYY764r5hjbmpHECPcpfYvZzqQHhog"
WEBGL_GAME_URL = "https://sudok-tau.vercel.app/"  # Your Unity WebGL Game URL

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'game'])
def send_game_button(message):
    chat_id = message.chat.id
    
    # Create inline keyboard with Telegram Web App
    markup = InlineKeyboardMarkup()
    web_app_button = InlineKeyboardButton("Conquer Sudoku(listing incoming)", web_app=WebAppInfo(url=WEBGL_GAME_URL))  # ✅ Corrected WebAppInfo usage
    markup.add(web_app_button)

    bot.send_message(chat_id, "⬆️Level up your intelligence by conquering the popular Sudoku game. Increase your brain power🧠 and accumulate as many gems💎 as possible to earn more $MMT. Do you have what it takes to conquer the game?", reply_markup=markup)

# Start the bot
bot.polling()