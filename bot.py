import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase using serviceAccountKey.json
cred = credentials.Certificate("setting.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Bot Token
BOT_TOKEN = "7879631782:AAHgMBYY764r5hjbmpHECPcpfYvZzqQHhog"
WEBGL_GAME_URL = "https://sudok-tau.vercel.app/"

bot = telebot.TeleBot(BOT_TOKEN)

def save_referral(new_user_id, referrer_id):
    """Save referral in Firestore if user is new."""
    print("saving data")
    user_ref = db.collection("referrals").document(str(new_user_id)).get()
    
    if not user_ref.exists:  # User is new
        db.collection("referrals").document(str(new_user_id)).set({"referrer_id": referrer_id})
        return True
    return False

@bot.message_handler(commands=['start', 'game'])
def send_game_button(message):
    chat_id = message.chat.id
    text = message.text
    referrer_id = None
    print(f"Referral text: {text}")
    print(f"Chat id : {chat_id}")
    # Extract referral code from /start
    if text.startswith("/start "):
        ref_code = text.split(" ")[1]
        if ref_code.isdigit():  # Ensure it's a valid user ID
            referrer_id = int(ref_code)

    # Save referral if valid
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
