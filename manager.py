

class Manager:

    def __init__(self):
        self._transaction = []

    def get_last_idx(self):
        return len(self._transaction)