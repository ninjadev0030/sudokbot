import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import sqlite3  # For storing referrals

# Bot Token
BOT_TOKEN = "YOUR_BOT_TOKEN"
WEBGL_GAME_URL = "https://sudok-tau.vercel.app/"

bot = telebot.TeleBot(BOT_TOKEN)

# Database connection
conn = sqlite3.connect("referrals.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS referrals (
                    user_id INTEGER PRIMARY KEY,
                    referrer_id INTEGER
                )''')
conn.commit()

def save_referral(new_user_id, referrer_id):
    """Save referral to database if user is new."""
    cursor.execute("SELECT * FROM referrals WHERE user_id=?", (new_user_id,))
    if not cursor.fetchone():  # Only save if the user is new
        cursor.execute("INSERT INTO referrals (user_id, referrer_id) VALUES (?, ?)", (new_user_id, referrer_id))
        conn.commit()
        return True
    return False

@bot.message_handler(commands=['start', 'game'])
def send_game_button(message):
    chat_id = message.chat.id
    text = message.text
    referrer_id = None

    # Extract referral code from start command
    if text.startswith("/start "):
        ref_code = text.split(" ")[1]  # Get ref code after /start
        if ref_code.isdigit():  # Ensure it's a valid user ID
            referrer_id = int(ref_code)

    # If there's a referral, save it
    if referrer_id and referrer_id != chat_id:
        if save_referral(chat_id, referrer_id):
            bot.send_message(referrer_id, f"🎉 Someone joined using your referral link! (User ID: {chat_id})")

    # Create inline keyboard with Web App button
    markup = InlineKeyboardMarkup()
    web_app_button = InlineKeyboardButton("Conquer Sudoku (listing incoming)", web_app=WebAppInfo(url=WEBGL_GAME_URL))
    markup.add(web_app_button)

    bot.send_message(
        chat_id,
        "⬆️ Level up your intelligence by conquering the popular Sudoku game. Increase your brain power🧠 and accumulate as many gems💎 as possible to earn more $MMT. Do you have what it takes to conquer the game?",
        reply_markup=markup
    )

# Start bot polling
bot.polling()
