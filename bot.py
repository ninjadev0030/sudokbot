import telebot

# Replace with your bot token
BOT_TOKEN = "7617620782:AAEpmcwWHpabyz8wtP1118moes5sQZNgEXE"
WEBGL_GAME_URL = "https://mentalmatics-telegram.vercel.app/"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'game'])
def send_game_link(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"🎮 Play the game here: [Click to Play]({WEBGL_GAME_URL})", parse_mode="Markdown")

# Start the bot
bot.polling()
