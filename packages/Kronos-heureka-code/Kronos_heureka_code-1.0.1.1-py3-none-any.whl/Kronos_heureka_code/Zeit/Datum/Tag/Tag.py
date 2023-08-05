try:
    from .TagException import *
except ImportError:
    from Kronos_heureka_code.Zeit.Datum.Tag.TagException import *


class Tag:
    def __init__(self, tag: int):
        self.__tag: [int, None] = None
        self.tag = tag
        pass

    @property
    def tag(self):
        return self.__tag

    @tag.setter
    def tag(self, tag: int):
        if type(tag) == float:
            raise TagKeineGanzeZahl(f"Ein Tag darf keine Kommazahl sein. ({tag})")
        try:
            tag = int(tag)
        except ValueError:
            raise TagKeineGanzeZahl(f"{tag} ist kein gueltiger Tag, da es keine ganze Zahl ist")
        if tag < 1:
            raise TagKleinerAlsEins(f"{tag} ist kleiner als 1 uns kein gueltiger Tag")

        self.__tag = tag
        pass

    def monats_pruefung(self, monat, schaltjahr: bool):
        if (
                (self.tag > int(monat.anzahl_tage)) and (schaltjahr is False) or
                (self.tag > int(monat.anzahl_tage_im_schaltjahr)) and schaltjahr
        ):
            raise TagZuGross(f"Der Tag {self.tag} ist zu gross fuer den {monat.name} mit maximal "
                             f"{int(monat.anzahl_tage_im_schaltjahr) if schaltjahr else int(monat.anzahl_tage)} Tagen")

    def __str__(self):
        return str(self.tag)

    def __repr__(self):
        return f"<Tag {self.tag}>"

    def __int__(self):
        return self.tag

    def __eq__(self, other):
        return self.tag == int(other)

    def __ne__(self, other):
        return self.__eq__(other) is False

    def __lt__(self, other):
        return self.tag < int(other)

    def __gt__(self, other):
        return self.tag > int(other)

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)
    pass
