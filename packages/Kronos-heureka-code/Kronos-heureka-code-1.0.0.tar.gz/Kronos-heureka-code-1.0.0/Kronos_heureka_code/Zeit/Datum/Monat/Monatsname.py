try:
    from .MonatsException import KeinGueltigerMonatscode, KeinGueltigerMonatsname
except ImportError:
    from Kronos_heureka_code.Zeit.Datum.Monat.MonatsException import KeinGueltigerMonatscode, KeinGueltigerMonatsname


class Monatsname:
    def __init__(self, monatsname: [str, "Monatsname"]):
        self.__monatsname: [str, None] = None
        self.monatsname = monatsname
        pass

    @property
    def monatsname(self) -> str:
        return self.__monatsname

    @monatsname.setter
    def monatsname(self, monatsname: str):
        if type(monatsname) != str:
            raise KeinGueltigerMonatsname(f"Der Name {monatsname} hat keinen gueltigen Typ")

        self.__monatsname = monatsname

    def __repr__(self):
        return f"<Monatsname {self.monatsname}>"

    def __str__(self):
        return self.monatsname
    pass
