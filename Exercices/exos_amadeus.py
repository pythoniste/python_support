def almost_square(number: int) -> int:
    """
    Returns the product between the previous number by the next one.
    For instance, if the number is 5, the result is the product between 4 and 6.

    >>> almost_square(5)
    24
    >>> almost_square(20)
    399
    """


def area_and_perimeter_rectangle(longueur: int, largeur: int) -> tuple[int, int]:
    """
    Returns the area and the perimeter of a rectangle

    >>> area_and_perimeter_rectangle(4, 5)
    (20, 18)
    """


def rotate_list(data: list) -> list:
    """
    Move every element of the list to the right. The last element became the first.
    
    >>> rotate_list([1, 2, 3, 4, 5])
    [5, 1, 2, 3, 4]
    """


def memory_check(data: list, index1: int, index2: int) -> bool:
    """
    Returns True if the elements at index 1 and 2 are the same. Print the related values
    
    >>> memory_check([1, 2, 3, 2, 5, 1, 4, 4, 5, 3], 1, 3)
    (2, 2)
    True
    >>> memory_check([1, 2, 3, 2, 5, 1, 4, 4, 5, 3], 2, 8)
    (3, 5)
    False
    """


def insert_in_the_middle(data: list, new: list, index: int) -> None:
    """
    Insert a list of new elements in a list, at the specified index
    
    >>> insert_in_the_middle([1, 2, 3, 4, 5], ["a", "b", "c"], 2)
    [1, 2, "a", "b", "c", 3, 4, 5]
    """


def is_palindrome(word: str) -> bool:
    """
    Is this word a palindrome ?

    >>> is_palindrome("Anna")
    True
    >>> is_palindrome("Viviane")
    False
    """


def username_from_email(email: str) -> str:
    """
    Get the username from the email address (the part before the @)

    >>> username_from_email("pythoniste@protonmail.com")
    'pythoniste'
    """


def compute_email(first_name: str, last_name: str) -> str:
    """
    Compute the email of a person from its first and last names.
    For instance, the mail of Simone Simmons should be: simone.simmons@amadeus.net

    >>> compute_email("Simone", "Simmons")
    'simone.simmons@amadeus.net'
    """


def add_email_to_datum(datum: dict[str, str | int]) -> dict[str, str | int]:
    """
    Add the email information to the datum.

    >>> add_email_to_datum({
    ...     "first_name": "Simone",
    ...     "last_name": "Simons",
    ...     "team": "QA",
    ... })
    {
        "first_name": "Simone",
        "last_name": Simons",
        "team": "QA",
        "email": "simone.simmons@amadeus.net",
    }
    """


def add_email_to_data(data: list[dict[str, str | int]]) -> list[dict[str, str | int]]:
    """
    Add the email information to the datum.

    >>> add_email_to_datum([
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
    [
        {
            "first_name": "Simone",
            "last_name": Simons",
            "team": "QA",
            "email": "simone.simmons@amadeus.net",
        },
        {
            "first_name": "Tarja",
            "last_name": Turunen",
            "team": "PDA",
            "email": "tarja.turunen@amadeus.net",
        },
        {
            "first_name": "Floor",
            "last_name": Jansen",
            "team": "QA",
            "email": "floor.jansen@amadeus.net",
        },
    ]
    """


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


from datetime import datetime, date, time, timedelta
from random import choice


def compute_age(birthdate: date) -> int:
    """
    Compute the age from the datebirth

    >>> compute_age(date(2000, 1, 1))
    24
    >>> compute_age(date(2000, 12, 31))
    23
    """


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

