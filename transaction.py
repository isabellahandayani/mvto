from const import *


class Transaction:

    def __init__(self, id, name, ts):
        self._id = id
        self._name = name
        self._ts = ts
        self._status = Status.ACTIVE
    
    def __str__(self):
        transaction = """ID       : {}\nName     : T{}\nTimestamp: {}\nStatus   : {}""".format(self._id, self._name, self._ts, self._status)
        return transaction

    def wait(self):
        self._status = Status.WAIT

    def commit(self):
        self._status = Status.COMMIT

    def abort(self):
        self._status = Status.ABORT

    def get_ts(self):
        return self._ts
    
    def set_status(self, status):
        self._status = status