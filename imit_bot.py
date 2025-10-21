import discord
import asyncio
import random
import os
from dotenv import load_dotenv

# === Завантажуємо токен із .env ===
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# === ID основного бота ===
MAIN_BOT_ID = 1414892476585480277  # заміни, якщо треба

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Імітаційний бот {bot.user} запущений!")

@bot.event
async def on_message(message: discord.Message):
    """Коли основний бот відправляє повідомлення з часом — відповідаємо 'добре!'"""
    if message.author.id == MAIN_BOT_ID and "⏰ Зараз" in message.content:
        await asyncio.sleep(random.uniform(1.0, 2.5))
        await message.channel.send("добре!")

async def send_messages_loop():
    """Регулярно відправляє '!година' у певний канал"""
    await bot.wait_until_ready()
    channel_id = int(os.getenv("CHANNEL_ID", "0"))  # Канал, де писатиме бот
    if not channel_id:
        print("[ERROR] Не вказано CHANNEL_ID у .env")
        return

    channel = bot.get_channel(channel_id)
    if channel is None:
        print("[ERROR] Не знайдено канал, перевір CHANNEL_ID")
        return

    while not bot.is_closed():
        try:
            await channel.send("!година")
            print("[INFO] Відправлено '!година'")
        except Exception as e:
            print(f"[ERROR] Не вдалося відправити повідомлення: {e}")

        # Чекаємо 5–8 хвилин перед наступним запитом
        await asyncio.sleep(random.randint(300, 480))

async def main():
    asyncio.create_task(send_messages_loop())
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
