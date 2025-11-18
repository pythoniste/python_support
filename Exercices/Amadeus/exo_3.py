def rotate_list(data: list) -> list:
    """
    Move every element of the list to the right. The last element became the first.

    >>> rotate_list([1, 2, 3, 4, 5])
    [5, 1, 2, 3, 4]
    """
    # Idea 1
    # first = data.pop()
    # data.insert(0, first)
    # return data

    # Idea 2
    # first = data.pop()
    # return [first] + data

    # Idea 3
    return data[-1:] + data[:-1]


def rotate_right(data: list, number=1) -> list:
    """
    Move every element of the list to the right. The last element became the first.

    >>> rotate_right([1, 2, 3, 4, 5])
    [5, 1, 2, 3, 4]
    >>> rotate_right([1, 2, 3, 4, 5], 2)
    [4, 5, 1, 2, 3]
    >>> rotate_right([1, 2, 3, 4, 5], 5)
    [1, 2, 3, 4, 5]
    >>> rotate_right([])
    []
    """
    return data[-number:] + data[:-number]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
