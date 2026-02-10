import pandas as pd
import random
from datetime import datetime
from telegram import Bot

BOT_TOKEN = "BOT_TOKENINGNI_QO‘Y"
GROUP_ID = -100XXXXXXXXXX
SHEET_CSV = "https://docs.google.com/spreadsheets/d/ID/export?format=csv"

MOTIVATION = [
    "🚆 Bugun yo‘llar tinch, siz esa fidoyilik bilan xizmat qilyapsiz!",
    "⚡ Temir yo‘l — intizom va mas’uliyat. Bugun ham shunday davom eting!",
    "🛤️ Sizning mehnatingiz xavfsiz yo‘llarning kafolati!",
    "🏅 Fidoyi xodimlarga hurmat cheksiz!",
    "🚄 Har bir reys — sizning e’tiboringiz bilan xavfsiz!",
    "💡 Temir yo‘l taraqqiyoti siz bilan!",
    "🌟 Bugun ham mas’uliyat bilan xizmat qiling!",
    "🚧 Xavfsizlik — birinchi o‘rinda!",
    "🎯 Aniqlik va intizom — sizning kuchingiz!",
    "🚀 Bugun yangi marralar sari!"
]

def get_today_birthdays():
    df = pd.read_csv(SHEET_CSV)
    df['tugilgan_kun'] = pd.to_datetime(df['tugilgan_kun'], errors='coerce')
    today = datetime.now()
    return df[
        (df['tugilgan_kun'].dt.day == today.day) &
        (df['tugilgan_kun'].dt.month == today.month)
    ]

def main():
    bot = Bot(BOT_TOKEN)
    df = get_today_birthdays()

    if not df.empty:
        names = [f"{r['ism']} ({r['bolim']})" for _, r in df.iterrows()]
        if len(names) == 1:
            text = f"""🎉🥳 Hurmatli {names[0]}!

Sizni tug‘ilgan kuningiz bilan tabriklaymiz!
Mustahkam sog‘liq, oilaviy baxt va ishlaringizda muvaffaqiyat tilaymiz!

Hurmat bilan,
"Qo'qon elektr ta'minoti" masofasi filiali 💡"""
        else:
            text = f"""🎉 Bugun tug‘ilganlar:
- """ + "\n- ".join(names) + """

Sizlarni chin qalbimizdan tabriklaymiz!

Hurmat bilan,
"Qo'qon elektr ta'minoti" masofasi filiali 💡"""
    else:
        text = "❗ Bugun tug‘ilgan kun yo‘q.\n\n" + random.choice(MOTIVATION)

    bot.send_message(chat_id=GROUP_ID, text=text)

if name == "__main__":
    main()
