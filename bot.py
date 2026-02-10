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
        df = df.fillna('')  # bo‘sh kataklarni tozalash
        df['tugilgan_kun'] = pd.to_datetime(df['tugilgan_kun'], errors='coerce')
        today = datetime.now()
        return df[(df['tugilgan_kun'].dt.day == today.day) &
                  (df['tugilgan_kun'].dt.month == today.month)]
    except Exception as e:
        print("Xatolik CSV faylni o‘qishda:", e)
        return pd.DataFrame()

def prepare_message(df):
    if df.empty:
        return None

    names = []
    for _, row in df.iterrows():
        ism = str(row.get('ism', '')).strip()
        bolim = str(row.get('bolim', '')).strip()
        if ism:
            names.append(f"{ism} ({bolim})" if bolim else ism)

    if len(names) == 1:
        return f"""Hurmatli {names[0]} temir yo‘l sohasining fidoyi xodimi.

Sizni tug‘ilgan kuningiz bilan chin qalbimizdan tabriklaymiz. Mas’uliyatli va sharafli mehnatingiz bilan yurtimiz taraqqiyotiga munosib hissa qo‘shib kelmoqdasiz. Sizga mustahkam sog‘liq, oilaviy baxt, ishlaringizda doimiy muvaffaqiyat va xavfsiz yo‘llar tilaymiz! Yana bir bor tug'ulgan kunigiz bilan tabriklaymiz.

Hurmat bilan "Qo'qon elektr ta'minoti" masofasi filiali!"""
    else:
        return f"""Hurmatli {', '.join(names)} temir yo‘l sohasining fidoyi xodimlari.

Sizlarni tug‘ilgan kuningiz bilan chin qalbimizdan tabriklaymiz. Mas’uliyatli va sharafli mehnatingiz bilan yurtimiz taraqqiyotiga munosib hissa qo‘shib kelmoqdasiz. Sizlarga mustahkam sog‘liq, oilaviy baxt, ishlaringizda doimiy muvaffaqiyat va xavfsiz yo‘llar tilaymiz! Yana bir bor tug'ulgan kunigiz bilan tabriklaymiz.

Hurmat bilan "Qo'qon elektr ta'minoti" masofasi filiali!"""

async def send_message(text):
    try:
        bot = Bot(BOT_TOKEN)
        await bot.send_message(chat_id=GROUP_ID, text=text)
    except Exception as e:
        print("Xatolik Telegramga yuborishda:", e)

async def main():
    df = get_today_birthdays()
    msg = prepare_message(df)
    if msg:
        await send_message(msg)

# Workaround xatoli bilan ishlay oladigan variant
name = "main"
if name == "main":
    asyncio.run(main())
