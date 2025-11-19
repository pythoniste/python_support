from datetime import time, timedelta, datetime, date


def compute_end_time(start_time: time, duration_hours: int | float) -> time:
    """
    Compute the end time of a meeting, from the start time and the duration in hour.

    >>> compute_end_time(time(10, 0, 0), 1)
    datetime.time(11, 0)
    >>> compute_end_time(time(9, 30, 0), 2.5)
    datetime.time(12, 0)
    >>> compute_end_time(time(23, 30, 0), 2)
    datetime.time(1, 30)
    """
    start_datetime = datetime.combine(date.today(), start_time)
    end_datetime = start_datetime + timedelta(hours=duration_hours)
    return end_datetime.time()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
