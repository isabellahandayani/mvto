import re

from const import *
from manager import *
from transaction import *

def main():
    query = input()
    done = False
    manager = Manager()
    while not done:
        query = query.lower()
        # Begin
        if re.search(Pattern.VALID, query) is not None or re.search(Pattern.COMMIT, query) is not None:
            manager._queue.append(query)
        # End
        elif re.search(Pattern.END, query) is not None:
            done = True
            break
        # Invalid
        else:
            print("Invalid Input Format")
            done = True
            break
        query = input()
    manager.run()


if __name__ == "__main__":
    main()