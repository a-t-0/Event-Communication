"""Commonly used helper functions."""
import json


def parse_string(string: str):
    """Verifies an input is of type string.

    :param string: param string: str:
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


def create_and_write_file(filepath, lines, overwrite=True):
    """

    :param filepath:
    :param lines:

    """

    if overwrite:
        write_style = "w"
    else:
        write_style = "a"  # append
    with open(filepath, write_style, encoding="utf-8") as some_file:
        for line in lines:
            some_file.write(line + "\n")
        some_file.close()


def read_file(filepath):
    """

    :param filepath:

    """
    # open and read the file after the appending:

    with open(filepath, "a", encoding="utf-8") as some_file:
        lines = some_file.read()
    return lines


def write_dict_to_file(filepath: str, some_dict: dict):
    """Writes a dict to file.

    :param filepath: str:
    :param some_dict: dict:
    """
    # TODO: verify file exists at filepath
    with open(filepath, "w", encoding="utf-8") as some_file:
        # some_file.write(json.dumps(some_dict))
        some_file.write(
            json.dumps(some_dict, indent=4, sort_keys=True, default=str)
        )


def load_dict_from_file(filepath: str) -> dict:
    """

    :param filepath: str:

    """
    # if not os.path.isfile(filepath):
    #    raise Exception(f"Error, dir_name={filepath} did not exist.")

    # reading the data from the file

    with open(
        filepath,
        encoding="utf-8",
    ) as f:
        data = f.read()

    # reconstructing the data as a dictionary
    the_dict = json.loads(data)

    return the_dict
