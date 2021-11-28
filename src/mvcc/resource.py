class Resource:
    def __init__(self, name, content="Init"):
        """
        Resource requested
        - name is name
        - self._version[key] = [rts, wts]
        """
        self._name = name
        self._version = {}
        self._version[0] = [0, 0, content]

    def add_version(self, id, rts, wts):
        """
        Add version of resource
        """
        self._version[id] = [rts, wts]

    def update_rts(self, id, rts):
        """
        Update Read Time stamp
        """
        self._version[id][0] = rts

    def update_wts(self, id, wts):
        """
        Update Write Time Stamp
        """
        self._version[id][1] = wts

    def update_content(self, id, content):
        """
        Update Content
        """
        self._version[id][2] = content

    def get_version(self):
        return self._version

    def __str__(self):
        resource = """Name : {}\nVers : {}
        """.format(
            self._name, self._version
        )
        return resource
