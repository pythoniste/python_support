def insert_in_the_middle(data: list, new: list, index: int) -> list:
    """
    Insert a list of new elements in a list, at the specified index

    >>> insert_in_the_middle([1, 2, 3, 4, 5], ['a', 'b', 'c'], 2)
    [1, 2, 'a', 'b', 'c', 3, 4, 5]
    >>> insert_in_the_middle([1, 2, 3, 4, 5], [], 2)
    [1, 2, 3, 4, 5]
    >>> insert_in_the_middle([1, 2, 3, 4, 5], ['a', 'b', 'c'], 42)
    [1, 2, 3, 4, 5, 'a', 'b', 'c']
    >>> insert_in_the_middle([1, 2, 3, 4, 5], ['a', 'b', 'c'], 0)
    ['a', 'b', 'c', 1, 2, 3, 4, 5]
    """
    # # Solution 1
    # for value in new[::-1]:
    #     data.insert(index, value)
    # return data
    #
    # # Solution 2
    # for i, value in enumerate(new):
    #     data.insert(index + i, value)
    # return data
    #
    # # Solution 3
    # for i, value in enumerate(new, start=index):
    #     data.insert(i, value)
    # return data

    # Solution 4
    return data[:index] + new + data[index:]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
