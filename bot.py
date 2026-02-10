import pandas as pd
import asyncio
import random
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from datetime import datetime

BOT_TOKEN = "8468084793:AAHdu9ZiywoxWdrhrJLYSU2Wt7F3O2cnrfU"
GROUP_ID = -1003613716463
SHEET_CSV = "https://docs.google.com/spreadsheets/d/14Y5SwUSgO00VTgLYAZR73XoQGg3V-p8M/export?format=csv"

# --- Motivatsion xabarlar ---
MOTIVATION_MESSAGES = [
    "🚆 Bugun yo‘llar tinch, vagonlar tartibli, siz esa fidoyi xodim sifatida o‘z ishini mukammal bajarishda davom etyapsiz! 💪",
    "⚡️ Har bir temir yo‘l uzelining harakati sizning mehnatingiz bilan bog‘liq. Bugun yangi marralarga intiling! 🚄",
    "🌟 Sizning mas’uliyatli va e’tiborli mehnatingiz tufayli yurtimiz taraqqiyotga intilmoqda. Bugun ham shunday davom eting!",
    "🚧 Vagonlar, relslar, stansiyalar… hammasi sizning mehnatingiz bilan tinch va xavfsiz ishlaydi. Rahmat sizga!",
    "🎯 Har bir to‘xtovsiz harakat, har bir belgilangan vaqtni bajarish – bu sizning fidoyiligingiz! Bugun yangi marralarni zabt eting!",
    "💡 Yangi loyihalar, yangi imkoniyatlar – temir yo‘l sohasi doimo yangilanadi. Siz ham yangilikka tayyormisiz?",
    "🛤 Bugun hech kim tug‘ilgan kunini nishonlamasa ham, jamoamiz faol va yo‘llar xavfsiz! Sizning mehnatingiz buning garovi!",
    "🌈 Har bir kun – yangi imkoniyat. Bugun biror yangilikni o‘zingiz yaratib, hamkasblaringizni ilhomlantiring!",
    "🏅 Sizning mas’uliyatli mehnatingiz temir yo‘l infratuzilmasini mukammal ishlashini ta’minlaydi. Bugun ham shunday davom eting!",
    "🚀 Fidoyi xodimlar yo‘llarimizni xavfsiz qiladi va taraqqiyotga hissa qo‘shadi. Bugun yangi marralarga intiling!"
]

# --- Rahmatlar hisobini saqlash ---
thank_counter = {}  # foydalanuvchi_id: count

def get_today_birthdays():
    try:
        df = pd.read_csv(SHEET_CSV)
        df = df.fillna('')
        df['tugilgan_kun'] = pd.to_datetime(df['tugilgan_kun'], errors='coerce')
        today = datetime.now()
        return df[(df['tugilgan_kun'].dt.day == today.day) &
                  (df['tugilgan_kun'].dt.month == today.month)]
    except Exception as e:
        print("Xatolik CSV faylni o‘qishda:", e)
        return pd.DataFrame()

def prepare_message(df):
    if df.empty:
        return "Afsus, bugun tug‘ilgan kun yo‘q!\n\n" + random.choice(MOTIVATION_MESSAGES)

    names = []
    for _, row in df.iterrows():
        ism = str(row.get('ism', '')).strip()
        bolim = str(row.get('bolim', '')).strip()
        if ism:
            if bolim:
                names.append(f"*{ism} ({bolim})*")
            else:
                names.append(f"*{ism}*")

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
        await bot.send_message(chat_id=GROUP_ID, text=text, parse_mode="Markdown")
    except Exception as e:
        print("Xatolik Telegramga yuborishda:", e)

# --- Rahmat javobi, takrorlanganlarda Qaytarormen ---
async def handle_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.lower()
    if any(word in text for word in ["rahmat","raxmat","raxmad","rahmad","рахмад","рамат"]):
        count = thank_counter.get(user_id, 0) + 1
        thank_counter[user_id] = count
        if count == 1:
            await update.message.reply_text("🤗 Sizga doimo salomatlik va muvaffaqiyat tilaymiz!")
        else:
            await update.message.reply_text("Qaytarormen!")

async def main():
    df = get_today_birthdays()
    msg = prepare_message(df)
    if msg:
        await send_message(msg)

# --- To‘g‘ri start ---
if name == "__main__":
    # Telegram reply handler uchun application yaratish
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    # Foydalanuvchi xabarlarini kuzatish
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reply))
    # Botni ishga tushirish
    asyncio.run(main())
