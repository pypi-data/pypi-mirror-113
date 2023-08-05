class VergleichsStammZahl:
    def __int__(self):
        return 0

    def __eq__(self, other):
        return self.__int__() == int(other)

    def __ne__(self, other):
        return self.__eq__(other) is False

    def __lt__(self, other):
        return self.__int__() < int(other)

    def __gt__(self, other):
        return self.__int__() > int(other)

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)
    pass
