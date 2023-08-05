try:
    from .WochentagException import *
except ImportError:
    from Kronos_heureka_code.Zeit.Datum.Wochentag.WochentagException import *


class WochentagPosition:
    def __init__(self, position: int):
        self.__position: [int, None] = None
        self.wochentag_position = position
        pass

    @property
    def wochentag_position(self) -> int:
        return self.__position

    @wochentag_position.setter
    def wochentag_position(self, position: int):
        if type(position) != int:
            raise UngueltigeWochentagposition(f"{position} ist keine Zahl und keine erlaubte Position")
        if position < 0:
            raise UngueltigeWochentagposition(f"Die Position {position} ist kleiner als Null")
        self.__position = position
        pass

    def __int__(self):
        return self.wochentag_position

    def __repr__(self):
        return f"<Wochentagsposition {self.wochentag_position}>"

    def __eq__(self, other):
        return self.wochentag_position == int(other)

    def __ne__(self, other):
        return self.__eq__(other) is False

    def __lt__(self, other):
        return self.wochentag_position < int(other)

    def __gt__(self, other):
        return self.wochentag_position > int(other)

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)
    pass
