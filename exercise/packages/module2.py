from packages.custom_exceptions import InvalidInputError

def reverse_string(text):

    try:

        if not isinstance(text, str):
            raise InvalidInputError("Input must be string")

        return text[::-1]

    except Exception as e:
        raise InvalidInputError(e)


def count_vowels(text):

    try:

        vowels = "aeiouAEIOU"

        return sum(1 for char in text if char in vowels)

    except Exception:
        raise InvalidInputError("Invalid string input")


def is_palindrome(text):

    try:

        text = text.lower()

        return text == text[::-1]

    except Exception:
        raise InvalidInputError("Palindrome check failed")