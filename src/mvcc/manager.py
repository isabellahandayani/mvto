from mvcc.resource import Resource
from mvcc.transaction import *
from const import *
from util import *
import re


class Manager:
    def __init__(self):
        self._transaction = []
        self._queue = []
        self._resource = {}
        self._read_logs = {}
        self._write_logs = {}
        self._ts = 1

    def is_rollback(self, txn):
        return self.get_txn(txn - 1)._status == Status.ABORT

    def set_read(self, txn, vers, res, ts):
        if res in self._read_logs:
            self._read_logs[res].append((txn, vers))

        self._read_logs[res] = [(txn, vers, ts)]

    def set_write(self, txn, vers, res, ts):
        if txn in self._write_logs:
            self._write_logs[txn].append((res, vers))

        self._write_logs[txn] = [(res, vers, ts)]

    def get_txn(self, key):
        try:
            return self._transaction[key - 1]
        except:
            return False

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

    def check_write(self, txn):
        written = []
        for x in self._write_logs[txn + 1]:
            written.append(x)
        return written

    def check_read(self, written):
        read = []
        for res, vers, ts in written:
            for txn, read_vers, ts_read in self._read_logs[res]:
                if read_vers == vers and ts_read >= ts:
                    read.append(txn)

        return read

    def get_aborted(self):
        arr = []
        for x in self._transaction:
            if x._status == Status.ABORT:
                arr.append(x._ts)
        return arr

    def rollback(self, read):

        if len(read) == 0:
            return

        for txn in read:
            txn.abort()
            self.rollback(self.check_read(self.check_write(txn)))

    def get_max(self, res, txn):
        curr = None
        TS = self.get_txn(txn).get_ts()
        for vers in self.get_vers(res):
            res_ts = self.get_vers(res)[vers]
            if res_ts[1] <= TS:
                curr = res_ts[1]

        return curr

    def req_write(self, res, txn, val):
        TS = self.get_txn(txn).get_ts()
        qk = self.get_max(res, txn)
        # Rollback
        if qk is None or TS < self.get_vers(res)[qk][0]:
            self.get_txn(txn).abort()
            self.rollback(self.check_read(self.check_write(txn)))
        # Overwrite
        elif TS == self.get_vers(res)[qk][1]:
            self._resource[res]._version[TS][2] = val
            self.set_write(txn, qk, res, TS)
        # Add new version
        else:
            self._resource[res]._version[TS] = [TS, TS, val]
            self.set_write(txn, TS, res, TS)

    def req_read(self, res, txn):
        TS = self.get_txn(txn).get_ts()
        qk = self.get_max(res, txn)
        if qk is not None:
            self.get_vers(res)[qk][0] = TS
        self.set_read(txn, qk, res, TS)

    def run(self):
        while len(self._queue) > 0:
            if int(getTrans(self._queue[0])) in self.get_aborted():
                self._queue.pop(0)
            else:
                # Begin
                if not self.get_txn(getNumber(self._queue[0])):
                    txn = Transaction(
                        self.get_last_idx(), getNumber(self._queue[0]), self._ts
                    )
                    self._ts += 1
                    self._transaction.append(txn)

                # W/R
                if re.search(Pattern.WRITE, self._queue[0]) is not None:
                    params = getParam(self._queue[0])
                    params = [s.strip() for s in params]
                    if params[1] not in self._resource:
                        self._resource[params[1]] = Resource(params[1], params[2])

                    self.req_write(params[1], getNumber(params[0]), params[2])

                elif re.search(Pattern.READ, self._queue[0]) is not None:
                    params = getParam(self._queue[0])
                    params = [s.strip() for s in params]
                    if params[1] not in self._resource:
                        self._resource[params[1]] = Resource(params[1])

                    # Read always succeed
                    self.req_read(params[1], getNumber(params[0]))

                # Commit
                elif re.search(Pattern.COMMIT, self._queue[0]) is not None:
                    self._transaction[getNumber(self._queue[0]) - 1].commit()
                self._queue.pop(0)

    def result(self):
        for x in self._transaction:
            print(x)
