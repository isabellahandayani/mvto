import re
from const import *

def getNumber(text):
    return int(''.join([n for n in text if n.isdigit()]))

def getParam(text):
    result = re.search(Pattern.BETWEEN, text)
    return result.group(1).split(",")