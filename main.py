import re

from const import *
from manager import *
from transaction import *
from util import getNumber

def main():
    query = input()
    done = False
    manager = Manager()
    while not done:
        query = query.lower()
        # Begin
        if(re.search(Pattern.BEGIN, query) is not None):
            txn = Transaction(manager.get_last_idx(), "T" + getNumber(query), 0)
            manager._transaction.append(txn)
        # W/R
        elif(re.search(Pattern.WRITE, query) is not None):
            pass

        elif(re.search(Pattern.READ, query) is not None):
            pass
        
        # Commit
        elif(re.search(Pattern.COMMIT, query) is not None):
            pass


        # End
        elif(re.search(Pattern.END, query) is not None):
            pass

        # Invalid
        else:
            print("Invalid Input Format")
            done = True
        query = input()


if __name__ == "__main__":
    main()