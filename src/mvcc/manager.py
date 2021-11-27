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
        """
        Check if txn already aborted
        """
        return self.get_txn(txn)._status == Status.ABORT

    def set_read(self, txn, vers, res):
        """
        Insert to read logs format {<res>: [(<txn>, <vers>, <timestamp>)]}
        """
        if res not in self._read_logs:
            self._read_logs[res] = []
        self._read_logs[res].append((txn, vers))

    def set_write(self, txn, res):
        """
        Insert to write logs format {<txn>: [(<res>, <vers>. <ts>)]}
        """
        if txn in self._write_logs:
            self._write_logs[txn].append((res, txn))

        self._write_logs[txn] = [(res, txn)]

    def get_txn(self, key):
        """
        Get Transaction
        """
        try:
            return self._transaction[key]
        except:
            return False

    def get_vers(self, key):
        """
        Get list of version of resources
        """
        return self._resource[key]._version

    def print_transaction(self):
        """
        Outputs list of transactions
        """
        for key in self._transaction:
            print(self._transaction[key])

    def check_write(self, txn):
        """
        Return write logs of a transaction
        """
        written = []
        try:
            for x in self._write_logs[txn]:
                written.append(x)
        except:
            pass
        return written

    def check_read(self, written):
        """
        Get list of transaction whose
        read logs and write logs intersect
        """
        read = []
        for res, vers in written:
            for txn, read_vers in self._read_logs[res]:
                if read_vers == vers:
                    read.append(txn)
        return read

    def get_aborted(self):
        """
        Get list of aborted transaction
        """
        arr = []
        for key in self._transaction:
            if self._transaction[key]._status == Status.ABORT:
                arr.append(key)
        return arr

    def rollback(self, read):
        """
        Recursively rollback transaction
        """
        if len(read) == 0:
            return

        for txn in read:
            logging.info(f"[ABORT] T{txn} Cascading Rollback")
            self._transaction[txn].abort()
            self.rollback(self.check_read(self.check_write(txn)))

    def get_max(self, res, txn):
        """
        Get QK(version of resource whose
        write timestamp is the largest writestamp
        less than or equal to TS(txn)
        )
        """
        curr = None
        for vers in self.get_vers(res):
            res_ts = self.get_vers(res)[vers]
            if res_ts[1] <= txn:
                curr = res_ts[0], res_ts[1], vers
        return curr

    def req_write(self, res, txn, val):
        """
        Checks for issuing a write
        """
        qk = self.get_max(res, txn)
        # Rollback
        if txn < qk[0]:
            logging.info(f"[ABORT] T{txn}")
            self.get_txn(txn).abort()
            self.rollback(self.check_read(self.check_write(txn)))
        # Overwrite
        elif txn == qk[1]:
            logging.info(f"[OVERWRITE] {res} Version {txn}")
            self._resource[res]._version[qk[2]][2] = val
            self.set_write(txn, res)
        # Add new version
        else:
            logging.info(f"[WRITE] {res} Version {txn}")
            self._resource[res]._version[txn] = [txn, txn, val]
            self.set_write(txn, res)

    def req_read(self, res, txn):
        """
        Request Read
        """

        qk = self.get_max(res, txn)
        logging.info(f"[READ] T{txn} {res}")

        # If TS > R-TS QK
        if txn > qk[0]:
            self.get_vers(res)[qk[2]][0] = txn
        self.set_read(txn, qk[2], res)

    def run(self):
        logging.basicConfig(
            format=" %(message)s", datefmt="[%H:%M:%S]", level=logging.INFO
        )
        while len(self._queue) > 0:
            logging.info(f"[!] {self._queue[0]}")

            # Check if query already executed
            if int(getNumber(self._queue[0])) in self.get_aborted():
                logging.info(
                    f"[Warning]: T{getNumber(self._queue[0])} already rollbacked, skipped "
                )
                self._queue.pop(0)
            else:

                # Initialize Transaction
                if not self.get_txn(getNumber(self._queue[0])):
                    txn = Transaction(
                        getNumber(self._queue[0]),
                        getNumber(self._queue[0]),
                    )
                    self._transaction[getNumber(self._queue[0])] = txn

                # Write
                if re.search(Pattern.WRITE, self._queue[0], re.IGNORECASE) is not None:
                    params = getParam(self._queue[0])
                    params = [s.strip() for s in params]
                    if params[1] not in self._resource:
                        self._resource[params[1]] = Resource(params[1], params[2])

                    self.req_write(params[1], getNumber(params[0]), params[2])

                # Read
                elif re.search(Pattern.READ, self._queue[0], re.IGNORECASE) is not None:
                    params = getParam(self._queue[0])
                    params = [s.strip() for s in params]

                    # Initialize Resource
                    if params[1] not in self._resource:
                        self._resource[params[1]] = Resource(params[1])

                    self.req_read(params[1], getNumber(params[0]))

                # Commit
                elif (
                    re.search(Pattern.COMMIT, self._queue[0], re.IGNORECASE) is not None
                ):
                    self._transaction[getNumber(self._queue[0])].commit()
                self._queue.pop(0)
        for txn in self._transaction:
            print(self._transaction[txn])
