import re
from const import *

def getNumber(text):
    """
    Get The Number of Transaction Referred
    """
    return int(''.join([n for n in text if n.isdigit()]))

def getParam(text):
    """
    Get The Parameter of Write and Read
    """
    result = re.search(Pattern.BETWEEN, text)
    return result.group(1).split(",")

def getTrans(text):
    """
    Get The Transaction Number
    """
    result = re.search("\d+", text)
    if result == None: return None 
    else: return result.group(0)