from datetime import datetime, timedelta


def backward( n_day = 5000 ):
    """
    yield a generator of datetime, moving backward, from yesterday.

    n_day: number of days, default 5000.
    """

    n = 0
    x = datetime.now() 

    while n < n_day:
      x = x - timedelta( days=1 )
      n += 1
      yield x
