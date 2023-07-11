import telebot, re

BOT_TOKEN = ''
with open('.env', 'r') as f:
    rawkey = f.readline()
    _, _, BOT_TOKEN = str(rawkey).rpartition('=')
bot = telebot.TeleBot(BOT_TOKEN)

def reFormat(message):
    message = str(message).strip('/reformat ')
    starRegex = r'^\*.*\*$' # WA bold
    tildeRegex = r'^~.*~$'  # WA strikethrough
    underscoreRegex = r'^_.*_$' # WA italic
    backtickRegex = r'^```.*```$' # WA monospace

    if re.search(starRegex, message):
        return f'<b>{message[1:-1]}</b>'
    elif re.search(tildeRegex, message):
        return f'<s>{message[1:-1]}</s>'
    elif re.search(underscoreRegex, message):
        return f'<i>{message[1:-1]}</i>'
    elif re.search(backtickRegex, message):
        return f'<tt>{message[3:-3]}</tt>'
    return False


@bot.message_handler(commands=['start', 'hello', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome to Unformatter:\n A Whatsapp <-> Telegram text formatting utility bot. Use the \"/reformat <text>\" command to begin formatting your text!")

@bot.message_handler(commands=['reformat'])
def sendReFormatMsg(message):
    res = reFormat(message.text)
    if res:
        bot.send_message(message.chat.id, res, parse_mode='html')
    else:
        bot.reply_to(message,"Please check the syntax of your input!") 

bot.infinity_polling()