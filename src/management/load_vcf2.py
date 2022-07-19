"""Loads vcf from file into Python dict."""


from typing import List


def vcf_to_dict(vcf_filepath) -> List:
    """Loads a vcf file and converts it to a python dict.

    :param vcf_filepath:
    """
    vcf_dicts = []
    lines = load_vcf_lines(vcf_filepath)
    entries = separate_vcf_entries(lines)
    for entry in entries:
        # print(f"entry={entry}")
        vcf_dicts.append(parse_vcf_entry(entry))
    return vcf_dicts


def parse_vcf_entry(entry):
    """Parses a vcf entry of a single person and puts the information elements
    into a dictionary."""
    tel_nrs = []
    addresses = []
    vcf_dict = {}
    for element in entry:
        if element[:2] == "N:":
            vcf_dict["name"] = delete_leading_and_trailing_chrs(element[2:])
        elif element[:3] == "FN:":
            vcf_dict["full_name"] = delete_leading_and_trailing_chrs(
                element[3:]
            )
        elif element[:4] == "TEL;":
            tel_nrs.append(delete_leading_and_trailing_chrs(element[4:]))
        elif element[:8] == "VERSION:":
            pass
        elif element[:11] == "BEGIN:VCARD":
            pass
        elif element[:8] == "NICKNAME":
            vcf_dict["nickname"] = delete_leading_and_trailing_chrs(
                element[8:]
            )
        elif element[:4] == "BDAY":
            vcf_dict["birthday"] = delete_leading_and_trailing_chrs(
                element[4:]
            )
        elif element[:3] == "URL":
            vcf_dict["url"] = delete_leading_and_trailing_chrs(element[3:])
        elif element[:5] == "EMAIL":
            vcf_dict["email"] = delete_leading_and_trailing_chrs(element[5:])
        elif element[:3] == "ADR":
            vcf_dict["adr"] = delete_leading_and_trailing_chrs(element[3:])
        else:
            addresses.append(is_address_encoding(element, entry))

        vcf_dict["tel_nrs"] = tel_nrs
        vcf_dict["addresses"] = addresses
    return vcf_dict


def is_address_encoding(element: str, entry: List):
    """Checks whether the bytecode is an address that is encoded using ansi
    codes."""
    remainder = delete_leading_and_trailing_chrs(element)
    letters = ""
    while len(remainder) >= 3:
        if remainder[0] == "=" and remainder[1:3].isalnum():
            letters = f"{letters}{bytearray.fromhex(remainder[1:3]).decode()}"
            remainder = remainder[3:]
        else:
            raise Exception(
                f"leters={letters},element={element} from entry={entry} is not"
                + " yet supported."
            )
    print(f"letters={letters}")

    return letters


def delete_leading_and_trailing_chrs(name):
    """removes \n and ;;; characters from start and end of string."""
    name = name.rstrip("\n")
    name = name.rstrip(";")
    return name


def load_vcf_lines(vcf_filepath) -> List[str]:
    """Reads a .vcf file and returns the lines.

    :param vcf_filepath:
    """
    lines = []
    with open(vcf_filepath, encoding="utf-8") as ifile:
        for line in ifile:
            lines.append(line)
    return lines


def separate_vcf_entries(lines):
    """Converts the lines into individiual vcard entries/persons.

    :param lines:
    """
    entries = []
    in_entry = False
    for line in lines:
        if line == "BEGIN:VCARD\n":
            in_entry = True
            entry = []

        if line == "END:VCARD\n":
            in_entry = False
            entries.append(entry)
        if in_entry:
            entry.append(line)
    if in_entry:
        raise Exception("Error, no end of entry found.")
    return entries
