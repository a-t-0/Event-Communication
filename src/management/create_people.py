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
from pprint import pprint

from installation.export_private_data import (
    ensure_private_data_folders_are_created,
    ensure_private_data_templates_exist,
)
from src.helper import load_dict_from_file
from src.management.load_vcf2 import vcf_to_dict


def scan_input_vcfs(settings):
    """Loads all .vcf files from the input directory.

    :param settings:
    """
    ensure_private_data_templates_exist(settings)
    ensure_private_data_folders_are_created(settings["vcf_input_path"])
    ensure_private_data_folders_are_created(settings["vcf_output_path"])
    vcf_files = get_files_in_dir(settings["vcf_input_path"], "vcf")
    print("vcf_files")
    print(vcf_files)

    # Convert the vcf files into dictionaries.
    vcf_dicts = convert_vcf_files_to_dicts(vcf_files)
    print("vcf_dicts=")
    pprint(vcf_dicts)

    # Load existing persons.
    # pylint: disable=W0612
    persons, events, groups = load_data(settings)

    # Create persons.
    convert_vcf_dicts_to_persons(vcf_dicts, persons)


def convert_vcf_files_to_dicts(vcf_files):
    """Loads all incoming vcf file from a filepath, converts them into
    dictionaries.

    :param vcf_files:
    """
    vcf_dicts = {}
    for vcf_filepath in vcf_files:
        vcf_dicts[vcf_filepath] = vcf_to_dict(vcf_filepath)
    return vcf_dicts


def get_files_in_dir(some_dir: str, extension: str):
    """Returns all files in a directory that have a certain extension.

    :param some_dir: str:
    :param extension: str:
    :param some_dir: str:
    :param extension: str:
    """
    vcf_files = []
    print(f"some_dir={some_dir}, extension={extension}")
    for file in glob.glob(f"{some_dir}*.{extension}"):
        vcf_files.append(file)
    return vcf_files


def load_data(settings: dict) -> tuple[dict, dict, dict]:
    """Loads the plural dictionaries from the json files and returns them.

    :param settings: dict:
    :param settings: dict:
    """
    persons = load_dict_from_file(settings["persons_filepath"])
    events = load_dict_from_file(settings["events_filepath"])
    groups = load_dict_from_file(settings["groups_filepath"])
    return persons, events, groups


def convert_vcf_dicts_to_persons(vcf_dicts, persons):
    """Converts a vcf dict to a person object."""
    pprint(vcf_dicts)
    print(persons)
