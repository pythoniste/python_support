from exo_9 import add_email_to_datum

def add_email_to_data(data: list[dict[str, str | int]]) -> list[dict[str, str | int]]:
    """
    Add the email information to the datum.

    >>> add_email_to_data([
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
    ... ])
    [{'first_name': 'Simone', 'last_name': 'Simons', 'team': 'QA', 'email': 'simone.simons@amadeus.net'}, {'first_name': 'Tarja', 'last_name': 'Turunen', 'team': 'PDA', 'email': 'tarja.turunen@amadeus.net'}]
    """
    # result = []
    # for datum in data:
    #     new_datum = add_email_to_datum(datum)
    #     result.append(new_datum)
    # return result

    return [add_email_to_datum(datum) for datum in data]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
