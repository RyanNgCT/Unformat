import telebot, re, os, platform, emoji

BOT_TOKEN = ""
if platform.system() == 'Windows' or platform.system() == 'Darwin':
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

    print(message.json['entities'], '\n')
    if message.entities: # check for nonetype -> i.e. user enters WA input without any formatting / normal tele w/o formatting
        common_offsets = {}
        offset_entities = {}
        for entity in message.json['entities']: # reference key of the attribute of the message object
            offset = entity['offset']
            if offset not in offset_entities:
                offset_entities[offset] = []
            offset_entities[offset].append(entity)

        # Identify common offsets with more than one dictionary in the list
        for offset, entities in offset_entities.items():
            if len(entities) > 1:
                common_offsets[offset] = [entity['type'] for entity in entities]

        print(common_offsets)
        order = ['bold', 'strikethrough', 'italic']
        for offset, entityList in common_offsets.items():
            if 'underline' in entityList and len(entityList) > 2: # [b, u, i, s]
                print('Three or more overlapping elements including underline. ', entityList)
            elif 'underline' in entityList: # catch [b, u]/[i, u]/[s, u]
                print('Underline with one other element. ', entityList)
            elif len(entityList) >= 2:
                print('Non-underline overlapping entities. ', entityList)

        for entity in message.json['entities']:
            # Adjust the entity offset
            offset = entity['offset'] + offset_adjustment
            if entity['type'] == "bold":
                content = content[:offset] + "*" + content[offset: offset + entity['length']] \
                                + "*" + content[offset + entity['length'] :]
                offset_adjustment += 2
            elif entity['type'] == "italic":
                content = content[:offset] + "_" + content[offset: offset + entity['length']] \
                                + "_" + content[offset + entity['length'] :]
                offset_adjustment += 2
            elif entity['type'] == "strikethrough":
                content = content[:offset] + "~" + content[offset: offset + entity['length']] \
                                + "~" + content[offset + entity['length'] :]
                offset_adjustment += 2
            elif entity['type'] == "underline":
                lengthofUnderLine = entity['length']
                underlineStr = f'\n{lengthofUnderLine * "="}'
                content = content[:offset] + content[offset: offset + entity['length']] \
                                + underlineStr + content[offset + entity['length'] :]
                offset_adjustment += entity['length'] + 1
            elif entity['type'] == "emoji":
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
        '👋 Welcome to Unformat Bot:\n- A Whatsapp <-> Telegram text formatting utility bot.\n- Use the "/wa2tele" or "/tele2wa" commands to begin formatting your texts!',
    )


@bot.message_handler(commands=["wa2tele"])
def sendReFormatMsgHelper(message):
    textReply = "Enter text to convert from WhatsApp to Telegram."
    sent_msg = bot.send_message(message.chat.id, textReply)
    bot.register_next_step_handler(sent_msg, sendReFormatMsg)


def sendReFormatMsg(message):
    try:
        res = reFormat(message.text)
        if res:
            # val = HTMLValidator()
            # val.validate(res)
            # if val.errors == []
                bot.send_message(message.chat.id, res, parse_mode="html")
        else:
            bot.reply_to(message, "Please check the syntax of your input!")
    except telebot.apihelper.ApiTelegramException: # catch tag mismatch
        bot.reply_to(message, "An error occurred! Check that the input tags are in the right order.")


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