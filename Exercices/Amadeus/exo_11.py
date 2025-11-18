def print_users(users: list[dict[str, str | int]]):
    """
    Should print a table with the first name and last name of the user and his team name

    >>> print_users([
    ...     {
    ...         "first_name": "Simone",
    ...         "last_name": "Simons",
    ...         "team": "QA",
    ...     },
    ...     {
    ...         "first_name": "Tarja",
    ...         "last_name": "Turunen",
    ...         "team": "PDA",
    ...     },
    ...     {
    ...         "first_name": "Floor",
    ...         "last_name": "Jansen",
    ...         "team": "QA",
    ...     },
    ... ])
    +------------+-----------+------+
    | First name | Last name | Team |
    +------------+-----------+------+
    |     Simone | Simons    |  QA  |
    |      Tarja | Turunen   |  QA  |
    |      Floor | Jansen    |  QA  |
    +------------+-----------+------+
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
