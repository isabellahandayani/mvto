import re
import sys

from const import *
from mvcc.manager import *
from mvcc.transaction import *


def main():
    file = open(sys.argv[1], "r")
    text = list(file)
    text[len(text) - 1] += "\n"
    text = [s.strip() for s in text]
    manager = Manager()
    manager._queue = text
    manager.run()


if __name__ == "__main__":
    main()
