import re

def reFormat(message):
    message = str(message).strip('/reformat ')
    # print(message, type(message))
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
    tBoldRegex = r'<b>(.*?)</b>'
    tStrikeThruRegex = r'<s>(.*?)</s>' 
    tItalicRegex = r'<i>(.*?)</i>'
    tUnderLineRegex = r'<u>(.*?)</u>' # dk if will work

    boldList = re.findall(tBoldRegex, message)
    STList = re.findall(tStrikeThruRegex, message)
    italicList = re.findall(tItalicRegex, message)
    underLineList = re.findall(tUnderLineRegex, message)

    for bold in boldList:
        message = message.replace(f'<b>{bold}</b>', f'*{bold}*')
    for st in STList:
        message = message.replace(f'<s>{st}</s>', f'~{st}~')
    for italic in italicList:
        message = message.replace(f'<i>{italic}</i>', f'_{italic}_')

    for underlined in underLineList:
        elementLen = len(underlined)
        string = elementLen * '-'
        message = message.replace(f'<u>{underlined}</u>', f"\n{underlined}\n{string}\n")

    return message


def main():
    try:
        userInput = input('Enter a string: ') # replace with telegram app route for input later
        print(unFormat(userInput)) # can alternate btwn the two funcs above
    except:
        pass

if __name__ == "__main__":
    main()
