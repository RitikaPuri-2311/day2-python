from packages.custom_exceptions import InvalidInputError


def write_file(filename, content):

    try:

        with open(filename, "w") as file:
            file.write(content)

        return "File written successfully"

    except Exception:
        raise InvalidInputError("Unable to write file")


def read_file(filename):

    try:

        with open(filename, "r") as file:
            return file.read()

    except FileNotFoundError:
        raise InvalidInputError("File not found")


def append_file(filename, content):

    try:

        with open(filename, "a") as file:
            file.write(content)

        return "Content appended"

    except Exception:
        raise InvalidInputError("Append failed")