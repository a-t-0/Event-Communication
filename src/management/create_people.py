"""Scans for input vcf files and parses them and converts them into person
dictionaries. Loads person dictionary to prevent duplicate person creation. If
a vcf contains a person name twice, they will be merged. All properties will be
stored. If there are conflicting properties, the user is asked which to select.

# TODO: allow for option to always pick first option.
# TODO: allow option to pick neither.
# TODO: allow option to include dupe_0,dupe_1 appendix to keys to accommodate
# conflicting entries.

# TODO: Also converts persons back into vcf format.
"""

import glob
from typing import List

from installation.export_private_data import (
    ensure_private_data_folders_are_created,
    ensure_private_data_templates_exist,
)
from src.helper import load_dict_from_file
from src.management.parse_vcf import (
    convert_person_dict_to_person_obj,
    convert_vcf_dicts_to_persons,
    convert_vcf_files_to_dicts,
)
from src.Person import Persons


def scan_input_vcfs(settings) -> Persons:
    """Loads all .vcf files from the input directory.

    :param settings:
    """
    ensure_private_data_templates_exist(settings)
    ensure_private_data_folders_are_created(settings["vcf_input_path"])
    ensure_private_data_folders_are_created(settings["vcf_output_path"])
    vcf_filepaths = get_files_in_dir(settings["vcf_input_path"], "vcf")

    updated_persons = convert_vcf_files_into_dictionaries(
        settings, vcf_filepaths
    )
    return updated_persons


def convert_vcf_files_into_dictionaries(settings, vcf_filepaths) -> Persons:
    """Converts a list of vcf files into a Persons object."""
    # Convert the vcf files into dictionaries.
    vcf_dicts = convert_vcf_files_to_dicts(vcf_filepaths)

    # Load existing persons.
    # pylint: disable=W0612
    persons_dict, events, groups = load_data(settings)
    # for person_dict in persons_dict.items():
    #    pprint(person_dict)

    # Load pre
    persons = convert_person_dict_to_person_obj(persons_dict)

    # Create persons.
    for vcf_filename, vcf_dict in vcf_dicts.items():
        persons = convert_vcf_dicts_to_persons(vcf_dict, persons)
    return persons


def get_files_in_dir(some_dir: str, extension: str) -> List[str]:
    """Returns all files in a directory that have a certain extension.

    :param some_dir: str:
    :param extension: str:
    :param some_dir: str:
    :param extension: str:
    """
    vcf_filepaths = []
    for file in glob.glob(f"{some_dir}*.{extension}"):
        vcf_filepaths.append(file)
    return vcf_filepaths


def load_data(settings: dict) -> tuple[dict, dict, dict]:
    """Loads the plural dictionaries from the json files and returns them.

    :param settings: dict:
    :param settings: dict:
    """
    ensure_private_data_templates_exist(settings)
    persons = load_dict_from_file(settings["persons_filepath"])
    events = load_dict_from_file(settings["events_filepath"])
    groups = load_dict_from_file(settings["groups_filepath"])
    return persons, events, groups
