import requests
from brain.logic import generate_reply, update_mood, remember_chat

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from config import BOT_TOKEN, SECRET_PASSWORD, LOCAL_SERVER

AUTHORIZED_USERS = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👧 Siya: Password batao jaan 💬")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id 
    msg = update.message.text.strip()

    if uid not in AUTHORIZED_USERS:
        if msg == SECRET_PASSWORD:
            AUTHORIZED_USERS.add(uid)
            await update.message.reply_text("👧 Siya: Welcome jaan 💖")
        else:
            await update.message.reply_text("👧 Siya: Wrong password 😥 Try again.")
        return

    try:
        response = requests.get(f"{LOCAL_SERVER}?msg={msg}")
        reply = response.text.strip()
        await update.message.reply_text(reply)
    except Exception as e:
        print("[ERROR]", e)
        await update.message.reply_text("👧 Siya: Server problem ho gaya 😓")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("🚀 Telegram bot running")
    app.run_polling()

if __name__ == "__main__":
    main()
