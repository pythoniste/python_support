def almost_square(number: int) -> int:
    """
    Returns the product between the previous number by the next one.
    For instance, if the number is 5, the result is the product between 4 and 6.

    >>> almost_square(5)
    24
    >>> almost_square(20)
    399
    """
    # previous_number = number - 1
    # next_number = number + 1
    # result = previous_number * next_number
    # return result
    return (number - 1) * (number + 1)

if __name__ == "__main__":
    print("Main module")
    print(almost_square(5))
    print(almost_square(20))
    while True:
        user_input = input("Type a number: ")
        if user_input.isdigit():
            number = int(user_input)
            break
    print(almost_square(number))
else:
    print("module is imported")