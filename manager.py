from resource import *
from const import *
from util import *
from transaction import *
import re

class Manager:
    def __init__(self):
        self._transaction = []
        self._queue = []
        self._ts = 1

    def get_last_idx(self):
        return len(self._transaction)

    def print_transaction(self):
        for x in self._transaction:
            print(x)

    def get_ts(self):
        return self._ts
    
    def set_ts(self, ts):
        self._ts = ts

    def validate(self, res, txn):
        for item in res.get_version().items():
            print(item)
    
    def run(self):
        while len(self._queue) > 0:
            # Begin
            if(re.search(Pattern.BEGIN, self._queue[0]) is not None):
                txn = Transaction(self.get_last_idx(), "T" + str(getNumber(self._queue[0])), self.get_ts())
                self.set_ts(self.get_ts() + 1)
                self._transaction.append(txn)

            # W/R
            elif(re.search(Pattern.WRITE, self._queue[0]) is not None):
                pass

            elif(re.search(Pattern.READ, self._queue[0]) is not None):
                pass
            
            # Commit
            elif(re.search(Pattern.COMMIT, self._queue[0]) is not None):
                pass
            self._queue.pop(0)
