"""Ensures a repository with private data is created."""

# Check if a private data folder exists. If not, create it.
# TODO: verify the private data does not get synced to this public repo.
# TODO: allow the private data folder to be synced to a private repo.

# Private data folder structure:

import os

from samples.sample_persons import (
    get_sample_event_1,
    get_sample_group_1,
    get_sample_person_two_events,
)
from src.Event import Events
from src.Group import Groups
from src.helper import write_dict_to_file
from src.Person import Persons
from src.Plural import Plural
from src.to_dict import add_hash_code, to_dict


def ensure_private_data_folders_are_created(private_dir):
    """Checks if the private data folders are created.

    Checks if they exist and creates them if they did not yet exist.
    """

    # thedirs = list(map(lambda x: f"{private_dir}/{x}", private_subdirs))
    # thedirs.append(private_dir)
    # for some_dir in thedirs:
    for some_dir in [private_dir]:
        if not os.path.exists(some_dir):
            create_dir_if_not_exists(some_dir)
        if not os.path.exists(some_dir):
            raise Exception("Error {some_dir} does not exist, it should.")


def create_dir_if_not_exists(dir_name):
    """Creates a directory if it does not exist.

    :param root_dir_name:
    :param dir_name:
    """
    if not os.path.exists(dir_name):
        os.makedirs(f"{dir_name}")
    if not os.path.exists(dir_name):
        raise Exception(f"Error, dir_name={dir_name} did not exist.")


def ensure_private_data_templates_exist(settings: dict):
    """Ensures the private data templates for the objects:Person, Event and
    Group are created, such that you can edit them.

    If the files already exist, this method will verify the formatting
    and do nothing else.
    """
    ensure_private_data_folders_are_created(settings["private_dir"])

    # TODO: add unique hashcodes and write them as dict.
    person = get_sample_person_two_events()
    persons = Persons()
    add_object_to_dict(persons, person)

    event = get_sample_event_1()
    events = Events()
    add_object_to_dict(events, event)

    group = get_sample_group_1()
    groups = Groups()
    add_object_to_dict(groups, group)

    for filepath, some_object in [
        (settings["persons_filepath"], persons),
        (settings["events_filepath"], events),
        (settings["groups_filepath"], groups),
    ]:
        print(f"filepath={filepath}")
        if not os.path.isfile(filepath):
            export_dict(filepath, some_object)


def add_object_to_dict(objs: Plural, new_obj):
    """Adds an object to a Plural dictionary.

    It computes the hash code of the dictionary of the object, and adds
    the dictionary of the object. Note the dictionary is created custom
    for the Event, Group and Person objects to eliminate recursive
    loops. (A Event contains persons, and a person attends Events,
    creating infinite loops).
    """
    hash_code = add_hash_code(new_obj)
    objs.add_elem(hash_code=hash_code, new_item=new_obj)


def export_dict(filepath, plural):
    """Writes custom dictionaries of a Plural object of type Person, Event, or
    Group, to file."""
    exported_dict = {}
    for key, value in plural.items():
        exported_dict[key] = to_dict(value)

    # if not os.path.exists(filepath):
    write_dict_to_file(filepath, exported_dict)
    if not os.path.exists(filepath):
        raise Exception(f"Error, dir_name={filepath} did not exist.")
