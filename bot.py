import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import requests
import qrcode
from io import BytesIO

# Bot Token
BOT_TOKEN = "7879631782:AAHgMBYY764r5hjbmpHECPcpfYvZzqQHhog"
WEBGL_GAME_URL = "https://sudok-tau.vercel.app/"
SERVER_URL = "https://sudockserver.vercel.app/saveReferral"

bot = telebot.TeleBot(BOT_TOKEN)

def generate_qr_code(data):
    """Generate a QR code for the given data."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

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

def connect_ton_wallet(chat_id):
    """Function to handle TON wallet connection."""
    try:
        # Generate a unique connection link or data
        connection_link = "https://tonwallet.io/connect?user_id=" + str(chat_id)

        # Generate QR code
        qr_img = generate_qr_code(connection_link)

        # Save QR code to a bytes buffer
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        buffer.seek(0)

        # Send QR code to the user
        bot.send_photo(chat_id, buffer, caption="Scan this QR code to connect your TON wallet.")

    except Exception as e:
        bot.send_message(chat_id, f"Error connecting TON wallet: {e}")

@bot.message_handler(commands=['start', 'game'])
def send_game_button(message):
    chat_id = message.chat.id
    text = message.text
    referrer_id = None

    # Extract referral code from /start
    if text.startswith("/start "):
        ref_code = text.split(" ")[1]
        referrer_id = int(ref_code)

    # Save referral if valid
    save_referral(chat_id, referrer_id)

    # Create inline keyboard with Web App button
    markup = InlineKeyboardMarkup()
    web_app_button = InlineKeyboardButton("Conquer Sudoku (listing incoming)", web_app=WebAppInfo(url=WEBGL_GAME_URL))
    connect_wallet_button = InlineKeyboardButton("Connect TON Wallet", callback_data="connect_ton_wallet")
    markup.add(web_app_button, connect_wallet_button)

    bot.send_message(
        chat_id,
        "⬆️ Level up your intelligence by conquering the popular Sudoku game. Increase your brain power🧠 and accumulate as many gems💎 as possible to earn more $MMT. Do you have what it takes to conquer the game?",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "connect_ton_wallet":
        connect_ton_wallet(call.message.chat.id)

# Start bot polling
bot.polling()
