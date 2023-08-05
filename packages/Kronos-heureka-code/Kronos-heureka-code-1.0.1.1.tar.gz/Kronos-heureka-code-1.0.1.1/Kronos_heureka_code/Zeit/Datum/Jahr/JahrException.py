try:
    from ..DatumException import DatumException
except ImportError:
    from Kronos_heureka_code.Zeit.Datum.DatumException import DatumException


class JahrException(DatumException):
    pass


class JahrKeineGanzeZahl(JahrException):
    """Wird geworfen, wenn etwas anderes als eine ganze Zahl als Jahr gegeben wird:

    z.B.: 1,234; 42,1337 bzw. 1.234; 42.1337 Je nach Notation"""
    pass
