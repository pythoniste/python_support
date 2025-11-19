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
    |      Tarja | Turunen   | PDA  |
    |      Floor | Jansen    |  QA  |
    +------------+-----------+------+
    """
    sep = "+" + "-" * 12 + "+" + "-" * 11 + "+" + "-" * 6 + "+"
    print(sep)
    print("| First name | Last name | Team |")
    print(sep)
    for user in users:
        print(f"| {user['first_name'].rjust(10)} | {user['last_name'].ljust(9)} | {user['team'].center(4)} |")
        # print("| ", end="")
        # print(user["first_name"].rjust(10), end="")
        # print(" | ", end="")
        # print(user["last_name"].ljust(9), end="")
        # print(" | ", end="")
        # print(user["team"].center(4), end="")
        # print(" |")
    print(sep)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
