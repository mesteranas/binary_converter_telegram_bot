import message,app
import telegram
from telegram import InlineKeyboardMarkup,InlineKeyboardButton,Update
from telegram.ext import CommandHandler,MessageHandler,filters,ApplicationBuilder,CallbackQueryHandler,CallbackContext
original_user_messages = {}
with open("token.bot","r",encoding="utf-8") as file:
    bot=ApplicationBuilder().token(file.read()).build()
async def to_binary(update:Update,context:CallbackContext):
    try:
        binary = ' '.join(format(ord(char), '08b') for char in original_user_messages.get(update.message.chat_id))
        await update.message.reply_text(binary)
    except ValueError:
        await update.message.reply_text("Invalid input")

async def textHandler(update:Update,context:CallbackContext):
    global original_user_messages
    original_user_messages[update.message.chat_id] = update.message.text
    info=update.effective_user
    keyboard=InlineKeyboardMarkup([[InlineKeyboardButton(text="to binary",callback_data="to_binary")],[InlineKeyboardButton(text="to text",callback_data="to_text")]])
    await update.message.reply_text("select action",reply_markup=keyboard)
async def start(update,contextt):
    info=update.effective_user
    keyboard=InlineKeyboardMarkup([[InlineKeyboardButton("donate",url="https://www.paypal.me/AMohammed231")],[InlineKeyboardButton("help",callback_data="help")]])
    await message.Sendmessage(chat_id=info.id,text="welcome " + str(info.first_name) + "to this bot. this bot make to convert from or to binary , please send text or code",reply_markup=keyboard)
async def helb(update,contextt):
    links="""<a href="https://t.me/mesteranasm">telegram</a>

<a href="https://t.me/tprogrammers">telegram channel</a>

<a href="https://x.com/mesteranasm">x</a>

<a href="https://Github.com/mesteranas">Github</a>

email:
anasformohammed@gmail.com

<a href="https://Github.com/mesteranas/binary_converter_telegram_bot">visite project on Github</a>
"""
    info=update.effective_user
    await message.Sendmessage(info.id,"""name: {}\nversion: {}\ndescription: {}\n developer: {}\n contect us {}""".format(app.name,str(app.version),app.description,app.developer,links))
async def callBake(update:Update,contextt):
    q=update.callback_query
    q.answer()
    if q.data=="help":
        await helb(update,contextt)
    elif q.data=="to_binary":
        await to_binary(q,contextt)
    elif q.data=="to_text":
        try:
            chunks = original_user_messages.get(q.message.chat_id).split()  # Split binary string by spaces
            text1 = ''.join(chr(int(chunk, 2)) for chunk in chunks)
            await q.message.reply_text(text1)
        except:
            await q.message.reply_text("input error")


print("running")
bot.add_handler(CommandHandler("start",start))
bot.add_handler(CommandHandler("help",helb))
bot.add_handler(CallbackQueryHandler(callBake))
bot.add_handler(MessageHandler(filters.TEXT,textHandler))
bot.run_polling()