"""Commonly used helper functions."""


def parse_string(string: str):
    """Verifies an input is of type string.

    :param string:
    :param string: str:
    """
    if isinstance(string, str):
        return string
    raise Exception(
        f"Error, string type was:{type(string)} "
        + "whereas it should be of type string."
    )


def yes_or_no(question):
    """Get yes or no input.

    :param question:
    """
    reply = str(input(question + " (y/n): ")).lower().strip()
    if reply[0] == "y":
        return True
    if reply[0] == "n":
        return False
    return yes_or_no(f"Please enter y or n.\n{question}")


def todict(obj, classkey=None):
    """Convertes an object recursively to a dictionary.

    :param obj: The object that is converted to a dictionary.
    :param classkey:  (Default value = None)
    """
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = todict(v, classkey)
        return data
    if hasattr(obj, "_ast"):
        # pylint: disable=W0212
        return todict(obj._ast())
    if hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [todict(v, classkey) for v in obj]
    if hasattr(obj, "__dict__"):
        data = {
            key: todict(value, classkey)
            for key, value in obj.__dict__.items()
            if not callable(value) and not key.startswith("_")
        }
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    return obj
