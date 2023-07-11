import telebot, re

BOT_TOKEN = ''
with open('.env', 'r') as f:
    rawkey = f.readline()
    _, _, BOT_TOKEN = str(rawkey).rpartition('=')
bot = telebot.TeleBot(BOT_TOKEN)
bot.remove_webhook()
bot.set_webhook()

def reFormat(message):
    message = str(message).strip('/reformat ')
    # print(message, type(message)) # for debugging
    starRegex = r'\*(.*?)\*'  # Updated bold regex
    tildeRegex = r'~(.*?)~'  # Updated strikethrough regex
    underscoreRegex = r'_(.*?)_'  # Updated italic regex

    boldList = re.findall(starRegex, message)
    STList = re.findall(tildeRegex, message)
    italicList = re.findall(underscoreRegex, message)

    for bold in boldList:
        message = message.replace(f'*{bold}*', f'<b>{bold}</b>')
    for st in STList:
        message = message.replace(f'~{st}~', f'<s>{st}</s>')
    for italic in italicList:
        message = message.replace(f'_{italic}_', f'<i>{italic}</i>')
    
    return message


@bot.message_handler(commands=['start', 'hello', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome to Unformat Bot:\n A Whatsapp <-> Telegram text formatting utility bot. Use the \"/reformat <text>\" command to begin formatting your text!")

@bot.message_handler(commands=['reformat'])
def sendReFormatMsg(message):
    res = reFormat(message.text)
    if res:
        bot.send_message(message.chat.id, res, parse_mode='html')
    else:
        bot.reply_to(message,"Please check the syntax of your input!") 

bot.infinity_polling()