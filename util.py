def getNumber(text):
    return int(''.join([n for n in text if n.isdigit()]))