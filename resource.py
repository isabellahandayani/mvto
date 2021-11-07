
class Resource:

    def __init__(self, name, rts, wts, lock):
        self._name = name
        self._rts = rts
        self._wts = wts

    def set_rts(self, rts):
        self._rts = rts

    def set_wts(self, wts):
        self._wts = wts

    def get_rts(self):
        return self._rts

    def get_wts(self):
        return self._wts