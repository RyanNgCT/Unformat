import re

def reFormat(message):
    message = str(message).strip('/reformat ')
    print(message, type(message))
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

def main():
    try:
        userInput = input('Enter a string: ') # replace with telegram app route for input later
        print(reFormat(userInput))
    except:
        pass

if __name__ == "__main__":
    main()
