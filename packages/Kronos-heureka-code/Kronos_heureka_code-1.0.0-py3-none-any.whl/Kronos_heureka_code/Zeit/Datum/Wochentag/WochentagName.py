try:
    from .WochentagException import *
except ImportError:
    from Kronos_heureka_code.Zeit.Datum.Wochentag.WochentagException import *


class WochentagName:
    def __init__(self, name: str):
        self.__name: [str, None] = None
        self.wochentag_name = name
        pass

    @property
    def wochentag_name(self) -> str:
        return self.__name

    @wochentag_name.setter
    def wochentag_name(self, name: str):
        if type(name) != str:
            raise UngueltigerWochentagname(f"{name} ist keine Zeichenkette und darum kein gueltiger Wochentagsname")
        self.__name = name
        pass

    def __repr__(self):
        return f"<Wochentag {self.wochentag_name}>"

    def __str__(self):
        return self.wochentag_name

    def __eq__(self, other):
        return self.wochentag_name == str(other)

    def __ne__(self, other):
        return self.__eq__(other) is False
    pass
