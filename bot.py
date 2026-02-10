import pandas as pd
import asyncio
from telegram import Bot
from datetime import datetime

BOT_TOKEN = "8468084793:AAHdu9ZiywoxWdrhrJLYSU2Wt7F3O2cnrfU"
GROUP_ID = -1003613716463
SHEET_CSV = "https://docs.google.com/spreadsheets/d/14Y5SwUSgO00VTgLYAZR73XoQGg3V-p8M/export?format=csv"

def get_today_birthdays():
    try:
        df = pd.read_csv(SHEET_CSV)
        df['tugilgan_kun'] = pd.to_datetime(df['tugilgan_kun'], errors='coerce')
        today = datetime.now()
        return df[(df['tugilgan_kun'].dt.day == today.day) & (df['tugilgan_kun'].dt.month == today.month)]
    except:
        return pd.DataFrame()

def prepare_message(df):
    if df.empty:
        return None
    names = [str(row.get('ism','')) for _, row in df.iterrows()]
    names = [n for n in names if n]
    if not names:
        return None
    if len(names) == 1:
        return f"🎉 Hurmatli {names[0]}, tug‘ilgan kuningiz bilan tabriklaymiz!"
    return f"🎉 Hurmatli {', '.join(names)}, tug‘ilgan kuningiz bilan tabriklaymiz!"

async def send_message(text):
    bot = Bot(BOT_TOKEN)
    await bot.send_message(chat_id=GROUP_ID, text=text)

async def main():
    df = get_today_birthdays()
    msg = prepare_message(df)
    if msg:
        await send_message(msg)

if name == "__main__":
    asyncio.run(main())
