return f"""🎉 Bugun tug‘ilganlar:  
- {'\n- '.join(names)}

Sizlarni chin qalbimizdan tabriklaymiz!  
🌟 Sizlarga sog‘liq, oilaviy baxt va ishlaringizda doimiy muvaffaqiyat tilaymiz!  

Hurmat bilan, "Qo'qon elektr ta'minoti" masofasi filiali 💡"""

# --- Inline tugma va javob qabul qilish ---
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

async def reply_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "rahmat" in text:
        await update.message.reply_text("🤗 Sizga doimo muvaffaqiyat tilaymiz!")

# --- Bot ishga tushishi ---
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_text))

# Botni ishga tushirish
app.run_polling()
