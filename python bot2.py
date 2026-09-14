import json
import os
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import Forbidden
from telegram.ext import Application, CommandHandler, ContextTypes

# =========================
# BOT TOKEN
# =========================
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN Environment Variable পাওয়া যায়নি!")

USERS_FILE = "users.json"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# =========================
# USER DATABASE
# =========================
def load_users():
    if not os.path.exists(USERS_FILE):
        return set()

    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except Exception:
        return set()


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(users), f)


# =========================
# START COMMAND
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.effective_user:
        return

    user = update.effective_user
    user_id = user.id
    full_name = user.full_name

    users = load_users()

    # আগে greeting দেওয়া হলে আর পাঠাবে না
    if user_id in users:
        return

    message = f"""প্লেবয় এজেন্সি থেকে সাইমন বলছি।

আসসালামু আলাইকুম {full_name} 👋

আপনি নিচের Telegram লিংকে প্রবেশ করে আমাদের সার্ভিস ও বিস্তারিত তথ্যগুলো এজেন্টের থেকে জেনে নিন।

Telegram-এ বিস্তারিত জানতে যোগাযোগ করুন @sesbukchat
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "📲 এজেন্টের সাথে যোগাযোগ করুন",
                url="https://t.me/sesbukchat"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await update.message.reply_text(
            message,
            reply_markup=reply_markup
        )

        # Greeting সফলভাবে পাঠানোর পর user save হবে
        users.add(user_id)
        save_users(users)

    except Forbidden:
        logging.warning(
            f"User {user_id} has blocked the bot."
        )

    except Exception as e:
        logging.error(f"Error: {e}")


# =========================
# MAIN
# =========================
def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    print("Bot চলছে...")

    app.run_polling()


# =========================
# RUN BOT
# =========================
if __name__ == "__main__":
    main()