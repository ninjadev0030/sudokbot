import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import firebase_admin
from firebase_admin import credentials, firestore
import requests

# Initialize Firebase using serviceAccountKey.json
try:
    cred = credentials.Certificate("setting.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase initialized successfully.")
except Exception as e:
    print(f"Error initializing Firebase: {e}")

# Bot Token
BOT_TOKEN = "7879631782:AAHgMBYY764r5hjbmpHECPcpfYvZzqQHhog"
WEBGL_GAME_URL = "https://sudok-tau.vercel.app/"
SERVER_URL = "https://sudockserver.vercel.app/saveReferral"

bot = telebot.TeleBot(BOT_TOKEN)

def save_referral(new_user_id, referrer_id):
    """Send referral data to the server."""
    print("Saving user info...")
    try:
        response = requests.post(SERVER_URL, json={"new_user_id": new_user_id, "referrer_id": referrer_id})
        if response.status_code == 200:
            print(f"Referral saved for new user {new_user_id} with referrer {referrer_id}.")
            return True
        else:
            print(f"Error saving referral: {response.json().get('error')}")
            return False
    except Exception as e:
        print(f"Error saving referral: {e}")
        return False

@bot.message_handler(commands=['start', 'game'])
def send_game_button(message):
    chat_id = message.chat.id
    text = message.text
    referrer_id = None

    # Extract referral code from /start
    if text.startswith("/start "):
        ref_code = text.split(" ")[1]
        if ref_code.isdigit():  # Ensure it's a valid user ID
            referrer_id = int(ref_code)
            print(f"Referral code extracted: {ref_code}")  # Print the referral code

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
