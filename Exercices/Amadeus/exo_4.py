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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
