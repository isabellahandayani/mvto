from resource import Resource
from transaction import *
from const import *
from util import *
import re

class Manager:
    def __init__(self):
        self._transaction = []
        self._queue = []
        self._resource = {}
        self._ts = 1

    def is_rollback(self, txn):
        return self.get_txn(txn-1)._status == Status.ABORT

    def get_txn(self, key):
        try:
            return self._transaction[key]
        except:
            print("Transaction has not been initialized")
            quit()

    def get_vers(self, key):
        return self._resource[key]._version

    def get_last_idx(self):
        return len(self._transaction)

    def print_transaction(self):
        for x in self._transaction:
            print(x)
    
    def print_resource(self):
        for x in self._resource:
            print(self._resource[x])

    def check_prev(self, txn):
            pass


    def req_write(self, res, txn):
        curr = None
        TS = self.get_txn(txn).get_ts()
        for vers in self.get_vers(res):
            res_ts = self.get_vers(res)[vers]
            if TS < res_ts[0] :
                txn.set_status(Status.ABORT)
                self.check_prev(txn)
            elif TS == res_ts[1]:
                pass
            else:
                pass
        

    def req_read(self, res, txn):
        TS = self.get_txn(txn).get_ts()
        for vers in self.get_vers(res):
            res_ts = self.get_vers(res)[vers]
            if res_ts[0] < TS:
                res_ts[0] = TS
    
    def run(self):
        while len(self._queue) > 0:
            # Begin
            if(re.search(Pattern.BEGIN, self._queue[0]) is not None):
                txn = Transaction(self.get_last_idx(), getNumber(self._queue[0]), self._ts)
                self._ts += 1
                self._transaction.append(txn)

            # W/R
            elif(re.search(Pattern.WRITE, self._queue[0]) is not None):
                params = getParam(self._queue[0])
                if params[1] not in self._resource:
                    self._resource[params[1]] = Resource(params[1], params[2])

                self.req_write(params[1], getNumber(params[0]))
        
            elif(re.search(Pattern.READ, self._queue[0]) is not None):
                params = getParam(self._queue[0])
                if params[1] not in self._resource:                      
                    self._resource[params[1]] = Resource(params[1])
        
                # Read always succeed
                self.req_read(params[1], getNumber(params[0])-1)

            # Commit
            elif(re.search(Pattern.COMMIT, self._queue[0]) is not None):
                self._transaction[getNumber(self._queue[0])].set_status(Status.COMMIT) 
            self._queue.pop(0)
            
        self.print_resource()
    
    def result(self):
        for x in self._transaction:
            print(x)
