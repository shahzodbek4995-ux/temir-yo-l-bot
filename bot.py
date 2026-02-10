import pandas as pd
from datetime import datetime
import random
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8468084793:AAHdu9ZiywoxWdrhrJLYSU2Wt7F3O2cnrfU"
GROUP_ID = -1003613716463
SHEET_CSV = "https://docs.google.com/spreadsheets/d/14Y5SwUSgO00VTgLYAZR73XoQGg3V-p8M/export?format=csv"

motivational_messages = [
    "🚆 Bugun yo‘llar tinch, vagonlar tartibli, siz esa fidoyi xodim sifatida o‘z ishini mukammal bajarishda davom etyapsiz! 💪",
    "⚡ Har bir temir yo‘l uzelining harakati sizning mehnatingiz bilan bog‘liq. Bugun yangi marralarga intiling! 🚄",
    "🌟 Sizning mas’uliyatli va e’tiborli mehnatingiz tufayli yurtimiz taraqqiyotga intilmoqda. Bugun ham shunday davom eting!",
    "🚧 Vagonlar, relslar, stansiyalar… hammasi sizning mehnatingiz bilan tinch va xavfsiz ishlaydi. Rahmat sizga!",
    "🎯 Har bir to‘xtovsiz harakat, har bir belgilangan vaqtni bajarish – bu sizning fidoyiligingiz! Bugun yangi marralarni zabt eting!",
    "💡 Yangi loyihalar, yangi imkoniyatlar – temir yo‘l sohasi doimo yangilanadi. Siz ham yangilikka tayyormisiz?",
    "🛤️ Bugun hech kim tug‘ilgan kunini nishonlamasa ham, jamoamiz faol va yo‘llar xavfsiz! Sizning mehnatingiz buning garovi!",
    "🌈 Har bir kun – yangi imkoniyat. Bugun biror yangilikni o‘zingiz yaratib, hamkasblaringizni ilhomlantiring!",
    "🏅 Sizning mas’uliyatli mehnatingiz temir yo‘l infratuzilmasini mukammal ishlashini ta’minlaydi. Bugun ham shunday davom eting!",
    "🚀 Fidoyi xodimlar yo‘llarimizni xavfsiz qiladi va taraqqiyotga hissa qo‘shadi. Bugun yangi marralarga intiling!"
]

LAST_MSG_FILE = "last_message.json"

def save_last_message_date(date_str):
    try:
        with open(LAST_MSG_FILE, "w") as f:
            json.dump({"last_no_birthday": date_str}, f)
    except:
        pass

def load_last_message_date():
    try:
        with open(LAST_MSG_FILE, "r") as f:
            data = json.load(f)
            return datetime.fromisoformat(data.get("last_no_birthday")).date()
    except:
        return None

def get_today_birthdays():
    try:
        df = pd.read_csv(SHEET_CSV)
        df = df.fillna('')
        df['tugilgan_kun'] = pd.to_datetime(df['tugilgan_kun'], errors='coerce')
        today = datetime.now()
        return df[(df['tugilgan_kun'].dt.day == today.day) & 
                  (df['tugilgan_kun'].dt.month == today.month)]
    except:
        return pd.DataFrame()

def prepare_message(df):
    today = datetime.now().date()
    last_date = load_last_message_date()
    
    if df.empty:
        if last_date and last_date == today:
            return None
        if last_date and (today - last_date).days > 0:
            msg = random.choice(motivational_messages)
        else:
            msg = "🎉 Afsus! Bugun tug‘ilgan kun yo‘q!\nLekin bugun mening tug‘ilgan kunim! Uraaa, tabriklasalaring bo‘ladi! 🥳🎂"
        save_last_message_date(today.isoformat())
        return msg
    
    names = [f"{row['ism']} ({row['bolim']}) 🎉" for _, row in df.iterrows() if row['ism']]
    if len(names) == 1:
        return f"""🎉🥳 Hurmatli {names[0]}!

Sizni tug‘ilgan kuningiz bilan tabriklaymiz!  
Mas’uliyatli mehnatingiz va fidoyiligingiz bilan yurtimiz taraqqiyotiga hissa qo‘shib kelmoqdasiz.  

🌟 Sizga sog‘liq, oilaviy baxt, ishlaringizda muvaffaqiyat va ko‘plab qiziqarli lahzalar tilaymiz!  

Hurmat bilan, "Qo'qon elektr ta'minoti" masofasi filiali 💡"""
    else:
        names_text = '\n- '.join(names)
        return (
            f"🎉 Bugun tug‘ilganlar:\n- {names_text}\n\n"
            "Sizlarni chin qalbimizdan tabriklaymiz!\n"
            "🌟 Sizlarga sog‘liq, oilaviy baxt va ishlaringizda doimiy muvaffaqiyat tilaymiz!\n\n"
            "Hurmat bilan, \"Qo'qon elektr ta'minoti\" masofasi filiali 💡"
        )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("🎊 Sizni yana bir bor tabriklaymiz! 🎂")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    df = get_today_birthdays()
    msg = prepare_message(df)
    if msg:
        keyboard = [[InlineKeyboardButton("🎉 Tug‘ilgan kuningiz bilan tabriklash!", callback_data='celebrate')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=GROUP_ID, text=msg, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

# --- Yangilangan reply_text funksiyasi ---
async def reply_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    thanks_words = ["rahmat", "rahmad", "рахмат", "рахмад"]
    if any(word in text for word in thanks_words):
        await update.message.reply_text("🤗 Sizga doimo muvaffaqiyat tilaymiz!")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_text))

app.run_polling()
