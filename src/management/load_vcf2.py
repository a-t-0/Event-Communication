"""Loads vcf from file into Python dict."""


from typing import List


def vcf_to_dict(vcf_filepath) -> dict:
    """Loads a vcf file and converts it to a python dict.

    :param vcf_filepath:
    """
    lines = load_vcf_lines(vcf_filepath)
    entries = separate_vcf_entries(lines)
    for entry in entries:
        print(f"entry={entry}")
    return {}


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
