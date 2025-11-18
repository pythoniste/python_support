def username_from_email(email: str) -> str:
    """
    Get the username from the email address (the part before the @)

    >>> username_from_email("pythoniste@protonmail.com")
    'pythoniste'
    """
    return email.split("@")[0]
    # return email[:email.index("@")]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
