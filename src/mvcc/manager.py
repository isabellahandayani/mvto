from mvcc.resource import Resource
from mvcc.transaction import *
from const import *
from util import *

import re
import logging


class Manager:
    def __init__(self):
        self._transaction = {}
        self._queue = []
        self._resource = {}
        self._read_logs = {}
        self._write_logs = {}

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
            return self._transaction[key]
        except:
            return False

    def get_vers(self, key):
        return self._resource[key]._version

    def get_last_idx(self):
        return len(self._transaction)

    def print_transaction(self):
        for key in self._transaction:
            print(self._transaction[key])

    def print_resource(self):
        for x in self._resource:
            print(self._resource[x])

    def check_write(self, txn):
        written = []
        for x in self._write_logs[txn]:
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
        for key in self._transaction:
            if self._transaction[key]._status == Status.ABORT:
                arr.append(key)
        return arr

    def rollback(self, read):

        if len(read) == 0:
            return

        for txn in read:
            txn.abort()
            self.rollback(self.check_read(self.check_write(txn)))

    def get_max(self, res, txn):
        curr = None
        for vers in self.get_vers(res):
            res_ts = self.get_vers(res)[vers]
            if res_ts[1] <= txn:
                curr = res_ts[0], res_ts[1], vers
        return curr

    def req_write(self, res, txn, val):
        logging.info(f"[WRITE] T{txn} {res} {val}")
        TS = self.get_txn(txn).get_ts()
        qk = self.get_max(res, txn)
        # Rollback
        if TS < qk[0]:
            logging.info(f"[ABORT] T{TS}")
            self.get_txn(txn).abort()
            self.rollback(self.check_read(self.check_write(txn)))
        # Overwrite
        elif TS == qk[1]:
            logging.info(f"[Overwrite] {res} Version{TS}")
            self._resource[res]._version[qk[3]][2] = val
            self.set_write(txn, qk, res, TS)
        # Add new version
        else:
            logging.info(f"[WRITE] {res} Version {TS}")
            self._resource[res]._version[TS] = [TS, TS, val]
            self.set_write(txn, TS, res, TS)

    def req_read(self, res, txn):
        """
        Request Read 
        """
        
        qk = self.get_max(res, txn)
        logging.info(f"[READ] T{txn} {res}")
        
        # If TS > R-TS QK 
        if txn > qk[0]:
            self.get_vers(res)[qk[2]][0] = txn
        self.set_read(txn, qk, res, txn)

    def run(self):
        logging.basicConfig(
            format=" %(message)s", datefmt="[%H:%M:%S]", level=logging.INFO
        )
        while len(self._queue) > 0:
            logging.info(f"[!] {self._queue[0]}")
            if int(getTrans(self._queue[0])) in self.get_aborted():
                logging.info(f"[Warning]: Transaction already rollbacked, skipped ")
                self._queue.pop(0)
            else:
                if not self.get_txn(getNumber(self._queue[0])):
                    txn = Transaction(
                        self.get_last_idx(),
                        getNumber(self._queue[0]),
                        getNumber(self._queue[0]),
                    )
                    self._transaction[getNumber(self._queue[0])] = txn

                # W/R
                if re.search(Pattern.WRITE, self._queue[0], re.IGNORECASE) is not None:
                    params = getParam(self._queue[0])
                    params = [s.strip() for s in params]
                    if params[1] not in self._resource:
                        self._resource[params[1]] = Resource(params[1], params[2])

                    self.req_write(params[1], getNumber(params[0]), params[2])

                elif re.search(Pattern.READ, self._queue[0], re.IGNORECASE) is not None:
                    params = getParam(self._queue[0])
                    params = [s.strip() for s in params]
                    if params[1] not in self._resource:
                        self._resource[params[1]] = Resource(params[1])

                    # Read always succeed
                    self.req_read(params[1], getNumber(params[0]))

                # Commit
                elif (
                    re.search(Pattern.COMMIT, self._queue[0], re.IGNORECASE) is not None
                ):
                    self._transaction[getNumber(self._queue[0])].commit()
                self._queue.pop(0)
        self.print_resource()