import pandas as pd
import random
from datetime import datetime
from telegram import Bot

# --- Sozlamalar ---
BOT_TOKEN = "8468084793:AAHdu9ZiywoxWdrhrJLYSU2Wt7F3O2cnrfU"
GROUP_ID = -1003613716463
SHEET_CSV = "https://docs.google.com/spreadsheets/d/14Y5SwUSgO00VTgLYAZR73XoQGg3V-p8M/export?format=csv"

# --- Motivatsion xabarlar ---
MOTIVATION_MESSAGES = [
    "🚆 Afsus, bugun tug‘ilgan kun yo‘q! Ammo yo‘llar tinch, ishlar barqaror. Sizning mehnatingiz bilan!",
    "⚡ Afsus, bugun tug‘ilgan kun yo‘q! Har bir rels sizning mas’uliyatingiz bilan mustahkam.",
    "🌟 Afsus, bugun tug‘ilgan kun yo‘q! Temir yo‘l fidoyilari bilan barqaror ishlayapti.",
    "🚧 Afsus, bugun tug‘ilgan kun yo‘q! Xavfsizlik va tartib — sizning qo‘lingizda.",
    "🎯 Afsus, bugun tug‘ilgan kun yo‘q! Har bir harakat aniqlik va intizom talab qiladi.",
    "💡 Afsus, bugun tug‘ilgan kun yo‘q! Yangilikka ochiq bo‘lish — muvaffaqiyat kaliti.",
    "🛤️ Afsus, bugun tug‘ilgan kun yo‘q! Lekin jamoa kuchli va ishlar ishonchli.",
    "🌈 Afsus, bugun tug‘ilgan kun yo‘q! Bugun ham xavfsiz yo‘llar sari.",
    "🏅 Afsus, bugun tug‘ilgan kun yo‘q! Fidoyiligingiz bilan faxrlanamiz.",
    "🚀 Afsus, bugun tug‘ilgan kun yo‘q! Taraqqiyot siz bilan davom etadi."
]

# --- Bugungi tug‘ilgan kunlarni olish ---
def get_today_birthdays():
    df = pd.read_csv(SHEET_CSV)
    df = df.fillna("")
    df["tugilgan_kun"] = pd.to_datetime(df["tugilgan_kun"], errors="coerce")
    today = datetime.now()
    return df[
        (df["tugilgan_kun"].dt.day == today.day) &
        (df["tugilgan_kun"].dt.month == today.month)
    ]

# --- Xabar tayyorlash ---
def prepare_message(df):
    if df.empty:
        return random.choice(MOTIVATION_MESSAGES)

    names = [f"{row['ism']} ({row['bolim']})" for _, row in df.iterrows()]

    if len(names) == 1:
        return (
            f"🎉🥳 Hurmatli {names[0]}!\n\n"
            "Sizni tug‘ilgan kuningiz bilan chin qalbimizdan tabriklaymiz!\n"
            "Mas’uliyatli va fidoyi mehnatingiz bilan temir yo‘l sohasiga katta hissa qo‘shyapsiz.\n\n"
            "🌟 Sizga sog‘liq, oilaviy baxt va ishlaringizda muvaffaqiyat tilaymiz!\n\n"
            "Hurmat bilan,\n"
            "\"Qo‘qon elektr ta’minoti\" masofasi filiali 💡"
        )

    else:
        joined = ", ".join(names)
        return (
            f"🎉 Hurmatli {joined}!\n\n"
            "Sizlarni tug‘ilgan kuningiz bilan chin qalbimizdan tabriklaymiz!\n"
            "Temir yo‘l sohasidagi fidoyiligingiz uchun tashakkur.\n\n"
            "🌟 Barchangizga sog‘liq va muvaffaqiyat!\n\n"
            "Hurmat bilan,\n"
            "\"Qo‘qon elektr ta’minoti\" masofasi filiali 💡"
        )

# --- Asosiy ish ---
def main():
    bot = Bot(BOT_TOKEN)
    df = get_today_birthdays()
    message = prepare_message(df)
    bot.send_message(chat_id=GROUP_ID, text=message)

# --- TO‘G‘RI START ---  
if name == "__main__":
    main()
