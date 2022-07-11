"""Commonly used helper functions."""


def parse_string(string: str):
    """Verifies an input is of type string.

    :param string:
    """
    if isinstance(string, str):
        return string
    raise Exception(
        f"Error, string type was:{type(string)} "
        + "whereas it should be of type string."
    )


def yes_or_no(question):
    """Get yes or no input."""
    reply = str(input(question + " (y/n): ")).lower().strip()
    if reply[0] == "y":
        return True
    if reply[0] == "n":
        return False
    return yes_or_no(f"Please enter y or n.\n{question}")
