try:
    from .Datum import Datum
    from .Jahr import *
    from .Monat import Monate
    from .Tag import Tag
except ImportError:
    from Kronos_heureka_code.Zeit.Datum import Datum
    from Kronos_heureka_code.Zeit.Datum.Jahr import *
    from Kronos_heureka_code.Zeit.Datum.Monat import Monate
    from Kronos_heureka_code.Zeit.Datum.Tag import Tag
