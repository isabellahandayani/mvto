class Status:
    """
    Status Value of A transaction
    Active  : Not yet executed
    Commit  : Commited
    Abort   : Aborted
    Wait    : Wait for other txn
    """

    ABORT = "ABORTED"
    COMMIT = "COMMITED"
    ACTIVE = "NOT COMMITED"


class Pattern:
    """
    Cry
    """

    BEGIN = r"^begin[(]t\d+[)]$"
    WRITE = r"^w[(]t\d+,.*[)]$"
    END = r"^end$"
    COMMIT = r"^c\d+$"
    READ = r"^r[(]t\d+,.*[)]$"
    VALID = r"^^((begin)[(]t\d+[)])|(w|r)[(]t\d+,.*[)]$"
    BETWEEN = r"[(](.+?)[)]$"
