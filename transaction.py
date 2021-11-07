from const import *


class Transaction:

    def __init__(self, id, name, ts):
        self._id = id
        self._name = name
        self._ts = ts
        self._status = Status.ACTIVE

    def wait(self):
        self._status = Status.WAIT

    def commit(self):
        self._status = Status.COMMIT

    def abort(self):
        self._status = Status.ABORT

