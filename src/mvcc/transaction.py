from const import *


class Transaction:
    def __init__(self, id, name, ts):
        self._name = name
        self._ts = ts
        self._status = Status.ACTIVE

    def __str__(self):
        transaction = """Name     : T{}\nTimestamp: {}\nStatus   : {}""".format(
            self._name, self._ts, self._status
        )
        return transaction

    def commit(self):
        self._status = Status.COMMIT

    def abort(self):
        self._status = Status.ABORT

    def get_ts(self):
        return self._ts
