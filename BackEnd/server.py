import telebot, re, os, platform, emoji

BOT_TOKEN = ""
if os.name == 'nt':
    path = '.env'
else:
    path = '/home/0x55AA/Unformatter/.env'

with open(path, 'r') as f:
    rawkey = f.readline()
    _, _, BOT_TOKEN = str(rawkey).rpartition("=")
bot = telebot.TeleBot(BOT_TOKEN)
bot.remove_webhook()
bot.set_webhook()
print(f'Running on {platform.system()}...\nProcess id: {os.getpid()}')


def replace_tags_recursive(text, starRegex, tildeRegex, underscoreRegex):
    # Replace bold tags
    text = re.sub(starRegex, r"<b>\1</b>", text)
    # Replace strikethrough tags
    text = re.sub(tildeRegex, r"<s>\1</s>", text)
    # Replace italic tags
    text = re.sub(underscoreRegex, r"<i>\1</i>", text)
    return text


def reFormat(message):
    message = str(message).strip("/wa2tele ")
    starRegex = r"\*(.*?)\*"  # Updated bold regex
    tildeRegex = r"~(.*?)~"  # Updated strikethrough regex
    underscoreRegex = r"_(.*?)_"  # Updated italic regex

    previous_message = ""
    while previous_message != message:
        previous_message = message
        message = replace_tags_recursive(message, starRegex, tildeRegex, underscoreRegex)

    return message.strip()


def unFormat(message):
    content = message.text
    offset_adjustment = 0  # Initialize the cumulative offset adjustment
    emoji_positions = []

    for entity in message.entities:
        offset = entity.offset + offset_adjustment  # Adjust the entity offset
        if entity.type == "bold":
            content = content[:offset] + "*" + content[offset: offset + entity.length] \
                               + "*" + content[offset + entity.length :]
            offset_adjustment += 2
        elif entity.type == "italic":
            content = content[:offset] + "_" + content[offset: offset + entity.length] \
                               + "_" + content[offset + entity.length :]
            offset_adjustment += 2
        elif entity.type == "strikethrough":
            content = content[:offset] + "~" + content[offset: offset + entity.length] \
                               + "~" + content[offset + entity.length :]
            offset_adjustment += 2
        elif entity.type == "underline":
            underlineStr = f'\n{entity.length * "="}'
            content = content[:offset] + content[offset: offset + entity.length] \
                               + underlineStr + content[offset + entity.length :]
            offset_adjustment += entity.length + 1
        elif entity.type == "emoji":
            emoji_positions.append(offset)

    for position in emoji_positions:
        offset = position + offset_adjustment
        content = content[:offset] + content[position] + content[offset:]
        if emoji.is_emoji(content[position]):
            offset_adjustment += 1

    return content


@bot.message_handler(commands=["start", "hello", "help"])
def send_welcome(message):
    bot.reply_to(
        message,
        '👋 Welcome to Unformat Bot:\n- A Whatsapp <-> Telegram text formatting utility bot.\n- Use the "/wa2tele <text>" or "/tele2wa <text>" commands to begin formatting your texts!',
    )


@bot.message_handler(commands=["wa2tele"])
def sendReFormatMsgHelper(message):
    textReply = "Enter text to convert from WhatsApp to Telegram."
    sent_msg = bot.send_message(message.chat.id, textReply)
    bot.register_next_step_handler(sent_msg, sendReFormatMsg)


def sendReFormatMsg(message):
    res = reFormat(message.text)
    if res:
        bot.send_message(message.chat.id, res, parse_mode="html")
    else:
        bot.reply_to(message, "Please check the syntax of your input!")


@bot.message_handler(commands=["tele2wa"])
def sendUnFormatMsgHelper(message):
    textReply = "Enter text to convert from Telegram to WhatsApp formatting."
    sent_msg = bot.send_message(message.chat.id, textReply)
    bot.register_next_step_handler(sent_msg, sendUnFormatMsg)


def sendUnFormatMsg(message):
    res = unFormat(message)
    if res:
        bot.send_message(message.chat.id, res)
    else:
        bot.reply_to(message, "Please check the syntax of your input!")


bot.infinity_polling()