import re

def reFormat(message):
    starRegex = r'^\*.*\*$' # WA bold
    tildeRegex = r'^~.*~$'  # WA strikethrough
    underscoreRegex = r'^_.*_$' # WA italic
    backtickRegex = r'^```.*```$' # WA monospace

    if re.search(starRegex, message):
        return "Verified to have the same start and end character: *"
    elif re.search(tildeRegex, message):
        return "Verified to have the same start and end character: ~"
    elif re.search(underscoreRegex, message):
        return "Verified to have the same start and end character: _"
    elif re.search(backtickRegex, message):
        return "Verified to have the same start and end character: ```"
    else:
        return "Not the same start and end character"

def main():
    try:
        userInput = input('Enter a string: ') # replace with telegram app route for input later
        print(reFormat(userInput))
    except:
        pass

if __name__ == "__main__":
    main()
