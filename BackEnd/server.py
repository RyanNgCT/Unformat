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
    print(message)
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


def unFormat(message):
    message = str(message).strip('/unformat ')
    tBoldRegex = r'\*\*(.*?)\*\*'
    tStrikeThruRegex = r'~~(.*?)~~' 
    tItalicRegex = r'__(.*?)__'
    tUnderLineRegex = r'<u>(.*?)</u>'
    # tags_with_content = re.findall(r'<[^>]+>[^<]+</[^>]+>', message)  # Extract tags with content

    boldList = re.findall(tBoldRegex, message)
    STList = re.findall(tStrikeThruRegex, message)
    italicList = re.findall(tItalicRegex, message)
    print(boldList, STList, italicList)

    # underLineList = re.findall(tUnderLineRegex, message)
    for bold in boldList:
        message = message.replace(f'*{bold}*', bold)
    for st in STList:
        message = message.replace(f'~{st}~', st)
    for italic in italicList:
        message = message.replace(f'_{italic}_', italic)

    # tags_with_content = [re.sub(r'<[^>]+>', '', tag) for tag in tags_with_content if re.search(r'<[^>]+>', tag)]

    # for underlined in underLineList:
    #     elementLen = len(underlined)
    #     suffixStr = elementLen * '-'
    #     if underlined == tags_with_content[0]:
    #         prefixStr = f"{underlined}\n"
    #         suffixStr += "\n"
    #     elif underlined != tags_with_content[-1] and underlined != tags_with_content[0]:
    #         prefixStr = f"\n\n{underlined}\n"
    #         suffixStr += "\n"
    #     elif underlined == tags_with_content[-1]:
    #         prefixStr = f"\n{underlined}\n"
    #     message = message.replace(f'<u>{underlined}</u>', f"{prefixStr}{suffixStr}")
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

@bot.message_handler(commands=['unformat'])
def sendUnFormatMsg(message):
    print(bot.get_messages(message.chat.id, parse_mode='html'))
    res = unFormat(message.text)
    if res:
        bot.send_message(message.chat.id, res)
    else:
        bot.reply_to(message,"Please check the syntax of your input!") 

bot.infinity_polling()