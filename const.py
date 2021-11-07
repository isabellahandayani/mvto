class Status:
    """
    Status Value of A transaction
    Active  : Not yet executed
    Commit  : Commited
    Abort   : Aborted
    Wait    : Wait for other txn
    """
    ABORT = 0
    COMMIT = 1
    WAIT = 2
    ACTIVE = 3

class Type:
    """
    Type of things a transaction can do
    """
    READ = "READ"
    WRITE = "WRITE"
    COMMIT = "COMMIT"

class Pattern:
    BEGIN = r"^begin[(]t\d+[)]$"
    WRITE = r"^w[(]t\d+[)]$"
    END = r"^end$"
    COMMIT = r"^c\d+$"
    READ = r"^r[(]t\d+[)]$"