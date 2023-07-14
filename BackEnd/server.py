import telebot, re

BOT_TOKEN = ""
with open(".env", "r") as f:
    rawkey = f.readline()
    _, _, BOT_TOKEN = str(rawkey).rpartition("=")
bot = telebot.TeleBot(BOT_TOKEN)
bot.remove_webhook()
bot.set_webhook()


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
    # print(message)
    starRegex = r"\*(.*?)\*"  # Updated bold regex
    tildeRegex = r"~(.*?)~"  # Updated strikethrough regex
    underscoreRegex = r"_(.*?)_"  # Updated italic regex

    previous_message = ""
    while previous_message != message:
        previous_message = message
        message = replace_tags_recursive(message, starRegex, tildeRegex, underscoreRegex)

    return message.strip()


def unFormat(message):
    command = "/tele2wa "
    content = message.text
    formattedContent = content[len(command) :]
    offset_adjustment = 0  # Initialize the cumulative offset adjustment

    for entity in message.entities:
        offset = entity.offset - len(command) + offset_adjustment # Adjust the entity offset
        if entity.type == "bold":
            formattedContent = formattedContent[:offset] + "*" + formattedContent[offset : offset + entity.length] \
                    + "*" + formattedContent[offset + entity.length :]
            offset_adjustment += 2
        elif entity.type == "italic":
            formattedContent = formattedContent[:offset] + "_" + formattedContent[offset : offset + entity.length] \
                                + "_" + formattedContent[offset + entity.length :]
            offset_adjustment += 2
        elif entity.type == "strikethrough":
            formattedContent = formattedContent[:offset] + "~" + formattedContent[offset : offset + entity.length] \
                                + "~" + formattedContent[offset + entity.length :]
            offset_adjustment += 2
        elif entity.type == "underline":
            underlineStr = f'\n{entity.length * "="}'
            formattedContent = formattedContent[:offset] + formattedContent[offset : offset + entity.length] \
                + underlineStr + formattedContent[offset + entity.length :]
            offset_adjustment += entity.length + 1

    # print(formattedContent.strip())
    return formattedContent.strip()


@bot.message_handler(commands=["start", "hello", "help"])
def send_welcome(message):
    bot.reply_to(
        message,
        '👋 Welcome to Unformat Bot:\n- A Whatsapp <-> Telegram text formatting utility bot.\n- Use the "/wa2tele <text>" or "/tele2wa <text>" commands to begin formatting your texts!',
    )


@bot.message_handler(commands=["wa2tele"])
def sendReFormatMsg(message):
    res = reFormat(message.text)
    if res:
        bot.send_message(message.chat.id, res, parse_mode="html")
    else:
        bot.reply_to(message, "Please check the syntax of your input!")


@bot.message_handler(commands=["tele2wa"])
def sendUnFormatMsg(message):
    res = unFormat(message)
    if res:
        bot.send_message(message.chat.id, res)
    else:
        bot.reply_to(message, "Please check the syntax of your input!")


bot.infinity_polling()