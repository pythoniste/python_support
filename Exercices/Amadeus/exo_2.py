def area_and_perimeter_rectangle(length: int, width: int) -> tuple[int, int]:
    """
    Returns the area and the perimeter of a rectangle

    >>> area_and_perimeter_rectangle(4, 5)
    (20, 18)
    """
    return length * width, 2 * (length + width)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
