import pandas as pd
from datetime import datetime
import random
import json
from telegram import Bot

# ================== SOZLAMALAR ==================
BOT_TOKEN = "8468084793:AAHdu9ZiywoxWdrhrJLYSU2Wt7F3O2cnrfU"
GROUP_ID = -1003613716463
SHEET_CSV = "https://docs.google.com/spreadsheets/d/14Y5SwUSgO00VTgLYAZR73XoQGg3V-p8M/export?format=csv"
STATE_FILE = "state.json"

# ================== 10 TA MOTIVATSION XABAR ==================
MOTIVATION_MESSAGES = [
    "🚆 Bugun yo‘llar tinch, vagonlar tartibli. Siz fidoyi temiryo‘lchisiz! 💪",
    "⚡ Temir yo‘l – mas’uliyat va e’tibor. Bugun ham xavfsizlikni unutmang!",
    "🌟 Sizning mehnatingiz tufayli yo‘llarimiz ishonchli!",
    "🚧 Har bir rels, har bir vagon — sizning fidoyiligingiz samarasi!",
    "🎯 Belgilangan vaqt va xavfsiz yo‘l — bu sizning mehnatingiz!",
    "💡 Temir yo‘l sohasi rivojida sizning hissangiz katta!",
    "🛤️ Bugun tug‘ilgan kun bo‘lmasa ham, jamoamiz ishda!",
    "🌈 Har bir ish kuni — yangi imkoniyat!",
    "🏅 Siz temir yo‘l tizimining tayanchisiz!",
    "🚀 Fidoyi temiryo‘lchilar — taraqqiyot poydevori!"
]

# ================== STATE ==================
def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"last_type": None}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

# ================== TUG‘ILGAN KUN ==================
def get_today_birthdays():
    df = pd.read_csv(SHEET_CSV)
    df = df.fillna("")
    df["tugilgan_kun"] = pd.to_datetime(df["tugilgan_kun"], errors="coerce")

    today = datetime.now()
    return df[
        (df["tugilgan_kun"].dt.day == today.day) &
        (df["tugilgan_kun"].dt.month == today.month)
    ]

# ================== ASOSIY ISH ==================
bot = Bot(token=BOT_TOKEN)
state = load_state()
df = get_today_birthdays()

if not df.empty:
    people = [f"{r['ism']} ({r['bolim']})" for _, r in df.iterrows()]

    if len(people) == 1:
        text = f"""🎉🥳 Hurmatli {people[0]}!

Sizni tug‘ilgan kuningiz bilan chin qalbimizdan tabriklaymiz!
Sog‘liq, baxt va ishlaringizda omad tilaymiz.

Hurmat bilan,
"Qo‘qon elektr ta’minoti" masofasi filiali 💡"""
    else:
        text = (
            "🎉 Bugun tug‘ilganlar:\n- " +
            "\n- ".join(people) +
            "\n\nBarchangizni chin qalbimizdan tabriklaymiz! 🎊"
        )

    bot.send_message(chat_id=GROUP_ID, text=text)
    save_state({"last_type": "birthday"})

else:
    if state.get("last_type") != "no_birthday":
        text = (
            "🎉 Afsus, bugun tug‘ilgan kun yo‘q!\n\n"
            "Lekin bugun mening tug‘ilgan kunim! 🥳🎂\n"
            "Tabriklasalaring bo‘ladi 😄"
        )
        save_state({"last_type": "no_birthday"})
    else:
        text = random.choice(MOTIVATION_MESSAGES)

    bot.send_message(chat_id=GROUP_ID, text=text)
    bot.send_message(chat_id=GROUP_ID, text="✅ TEST: bot ishlayapti")
