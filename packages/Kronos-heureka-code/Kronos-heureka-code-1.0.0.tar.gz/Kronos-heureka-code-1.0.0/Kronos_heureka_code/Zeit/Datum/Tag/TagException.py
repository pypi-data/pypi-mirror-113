try:
    from ..DatumException import DatumException
except ImportError:
    from Kronos_heureka_code.Zeit.Datum.DatumException import DatumException


class TagException(DatumException):
    pass


class TagKeineGanzeZahl(TagException):
    pass


class TagKleinerAlsEins(TagException):
    pass


class TagZuGross(TagException):
    pass
