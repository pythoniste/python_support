from exo_8 import compute_email


def add_email_to_datum(datum: dict[str, str | int]) -> dict[str, str | int]:
    """
    Add the email information to the datum.

    >>> add_email_to_datum({
    ...     "first_name": "Simone",
    ...     "last_name": "Simons",
    ...     "team": "QA",
    ... })
    {'first_name': 'Simone', 'last_name': 'Simons', 'team': 'QA', 'email': 'simone.simons@amadeus.net'}
    """
    datum["email"] = compute_email(datum["first_name"], datum["last_name"])
    return datum

    # return datum | {
    #     "email": compute_email(datum["first_name"], datum["last_name"]),
    # }


if __name__ == "__main__":
    import doctest
    doctest.testmod()
