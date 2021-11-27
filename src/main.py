import re
import sys 

from const import *
from mvcc.manager import *
from mvcc.transaction import *


def main():
    file = open(sys.argv[1], "r")
    text = list(file)
    text[len(text) - 1] += "\n"
    text = [s.strip().lower() for s in text]
    manager = Manager()
    manager._queue = text
    manager.run()
    manager.result()


if __name__ == "__main__":
    main()
