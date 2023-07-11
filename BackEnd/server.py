from telebot_router import TeleBot

app = TeleBot(__name__)

@app.route('/tele2wa ?(.*)')
def telegram2WhatsappFormat(message, cmd):
    chat_dest = message['chat']['id']
    msg = "Command Received: {}".format(cmd)

    app.send_message(chat_dest, msg)


@app.route('(?!/).+')
def test(message):
    pass

def main():
    pass

if __name__ == '__main__':
    key = ''
    with open('.env', 'r') as f:
        rawkey = f.readline()
        _, _, key = str(rawkey).rpartition('=')
    print(key)
    # app.config['api_key'] = 'xxxxxxxx:enterYourBotKeyHereToTest'
    # app.poll(debug=True)
