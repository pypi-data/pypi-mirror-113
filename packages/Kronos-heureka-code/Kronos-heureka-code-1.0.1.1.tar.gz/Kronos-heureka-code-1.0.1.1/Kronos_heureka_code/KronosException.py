class KronosException(Exception):
    def __init__(self, msg: str):
        super(KronosException, self).__init__(msg)
        self.__msg = msg
        pass

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {self.__msg}>"
    pass
