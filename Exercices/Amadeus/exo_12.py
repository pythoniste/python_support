from datetime import date, timedelta


def compute_age(birthdate: date) -> int:
    """
    Compute the age from the datebirth

    >>> compute_age(date(2000, 1, 1))
    25
    >>> compute_age(date(2000, 12, 31))
    24
    """
    today = date.today()
    diff = today - birthdate
    return int(diff.days / 365.25)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
