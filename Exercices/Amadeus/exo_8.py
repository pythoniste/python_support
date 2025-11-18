def compute_email(first_name: str, last_name: str) -> str:
    """
    Compute the email of a person from its first and last names.
    For instance, the mail of Simone Simmons should be: simone.simmons@amadeus.net

    >>> compute_email("Simone", "Simmons")
    'simone.simmons@amadeus.net'
    """
    # return first_name.lower() + "." + last_name.lower() + "@amadeus.net"
    return f"{first_name.lower()}.{last_name.lower()}@amadeus.net"


if __name__ == "__main__":
    import doctest
    doctest.testmod()
