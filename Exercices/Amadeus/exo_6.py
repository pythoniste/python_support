def is_palindrome(word: str) -> bool:
    """
    Is this word a palindrome ?

    >>> is_palindrome("Anna")
    True
    >>> is_palindrome("Viviane")
    False
    """
    return (word_lower := word.lower()) == word_lower[::-1]


if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    word = input("Type a word to test is this is a palindrome: ")
    print(is_palindrome(word))
