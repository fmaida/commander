class UnknownCommand(Exception):
    """
    This exception handles unknown commands
    """

    def __init__(self, cmd):
        Exception.__init__(self, "Uknown command: {}".format(cmd))
