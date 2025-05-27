
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
from generate_image import generate_collage
import subprocess

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

logging.basicConfig(level=logging.INFO)

async def fetch_shop_data():
    result = subprocess.run(["node", "scrape.js"], capture_output=True, text=True)
    return result.stdout.strip()

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Получаю магазин...")
    json_data = await fetch_shop_data()
    img_path = generate_collage(json_data)
    with open(img_path, "rb") as img:
        await update.message.reply_photo(photo=img)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("shop", shop))

if __name__ == "__main__":
    app.run_polling()
