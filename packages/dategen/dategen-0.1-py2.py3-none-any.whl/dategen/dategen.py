from datetime import datetime, timedelta


def backward( my_n_day = 4000 ):
    """A datetime generator, backward from yesterday."""

    __version__ = '0.1'
    n = 0
    x = datetime.now() 

    while n < my_n_day:
      x = x - timedelta( days=1 )
      n += 1
      yield x
