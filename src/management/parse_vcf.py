"""Parses vcf file to create dictionary."""


from pprint import pprint
from typing import List

from src.Contact_info import Contact_info
from src.management.load_vcf2 import vcf_to_dict
from src.Person import Person, Persons
from src.Person_information import Person_information


def convert_vcf_files_to_dicts(vcf_files):
    """Loads all incoming vcf file from a filepath, converts them into
    dictionaries.

    :param vcf_files:
    """
    vcf_dicts = {}
    for vcf_filepath in vcf_files:
        vcf_dicts[vcf_filepath] = vcf_to_dict(vcf_filepath)
    return vcf_dicts


def convert_vcf_dicts_to_persons(vcf_dicts: List[dict], persons) -> Persons:
    """Converts a vcf dict to a person object."""
    pprint(vcf_dicts)
    print(persons)
    for vcf_dict in vcf_dicts:
        first_name, last_name = split_first_name_last_name(vcf_dict)
        print(f"first_name={first_name}")
        print(f"last_name={last_name}")

        phone_nrs = parse_tel(vcf_dict["tel_nrs"])

        print("done parsing, now creating person information")
        person_information = Person_information(
            first_name=first_name,
            last_name=last_name,
        )

        contact_info = Contact_info(
            phone_nrs, emails={}, github="", linkedin="", facebook="", other=""
        )
        person = Person(person_information, contact_info, [], [])
        persons.add_elem(person)
        return persons


def split_first_name_last_name(vcf_dict: dict) -> tuple[str, str]:
    """Splits a full name into a first name and last name, if they are
    available."""
    print(f"vcf_dict={vcf_dict}")
    names = vcf_dict["full_name"].split(" ")
    if len(names) > 1:
        first_name = names[0]
        start_at = len(first_name) + 1
        last_name = vcf_dict["full_name"][start_at:]
        return first_name, last_name
    return vcf_dict["full_name"], ""


def parse_tel(vcf_tel_element):
    """Reads out the list of telephone numbers and converts them into a
    dictionary."""
    print(f"vcf_tel_element={vcf_tel_element}")
    phone_nrs = {}
    for phone in vcf_tel_element:
        description, phone_nr = phone.split(":")
        phone_nr.replace("-", "")
        phone_nrs[description] = phone_nr

    return phone_nrs
