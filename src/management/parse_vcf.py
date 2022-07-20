"""Parses vcf file to create dictionary."""


from pprint import pprint
from typing import List

from installation.export_private_data import add_object_to_dict
from src.Contact_info import Contact_info
from src.Event import Event, Events
from src.Group import Group, Groups
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
    """Converts a vcf dict to a person object.

    :param vcf_dicts: List[dict]:
    :param persons:
    :param vcf_dicts: List[dict]:
    """
    for vcf_dict in vcf_dicts:
        first_name, last_name = split_first_name_last_name(vcf_dict)
        print(f"first_name={first_name}")
        print(f"last_name={last_name}")

        phone_nrs = parse_tel(vcf_dict["tel_nrs"])

        person_information = Person_information(
            first_name=first_name,
            states=[],
            last_name=last_name,
        )

        contact_info = Contact_info(
            phone_nrs, emails={}, github="", linkedin="", facebook="", other=""
        )
        person = Person(person_information, contact_info, [], [])

        # TODO: see if person already in list, if yes, merge data
        print(f"before len(persons)={len(persons)}")
        add_object_to_dict(persons, person)
        print(f"after len(persons)={len(persons)}")
    return persons


def split_first_name_last_name(vcf_dict: dict) -> tuple[str, str]:
    """Splits a full name into a first name and last name, if they are
    available.

    :param vcf_dict: dict:
    :param vcf_dict: dict:
    """
    names = vcf_dict["full_name"].split(" ")
    if len(names) > 1:
        first_name = names[0]
        start_at = len(first_name) + 1
        last_name = vcf_dict["full_name"][start_at:]
        return first_name, last_name
    return vcf_dict["full_name"], ""


def parse_tel(vcf_tel_element):
    """Reads out the list of telephone numbers and converts them into a
    dictionary.

    :param vcf_tel_element:
    """
    phone_nrs = {}
    for phone in vcf_tel_element:
        description, phone_nr = phone.split(":")
        phone_nr.replace("-", "")
        phone_nrs[description] = phone_nr

    return phone_nrs


def convert_person_dict_to_person_obj(dict_with_hash: dict) -> Person:
    """Converts a person dict into a person object.

    :param dict_with_hash: dict:
    :param dict_with_hash: dict:
    """
    persons = Persons()
    for hashcode, person_dict in dict_with_hash.items():
        ci = person_dict["contact_info"]
        pi = person_dict["person_info"]

        # (self, phone_nrs: dict, emails, github, linkedin, facebook, other)
        contact_info = Contact_info(
            phone_nrs=ci["phone_nrs"],
            emails=ci["emails"],
            github=ci["github"],
            linkedin=ci["linkedin"],
            facebook=ci["facebook"],
            other=ci["other"],
        )
        person_info = Person_information(
            first_name=pi["first_name"],
            states=pi["states"],
            known_from=pi["known_from"],
            last_name=pi["last_name"],
        )

        events = convert_events_list_of_dicts_to_events(person_dict["events"])
        # TODO: add person to events

        groups = convert_group_list_groups(person_dict["groups"])

        person = Person(
            person_info, contact_info, events=events, groups=groups
        )
        # TODO: verify new person dict is identical to old person dict.
        if hashcode == "":
            print("TODO")
        add_object_to_dict(persons, person)
    return persons


def convert_events_list_of_dicts_to_events(incoming_events: dict) -> Events:
    """Converts a list with event dictionaries into an Events object.

    :param events_list: List:
    :param events_list: List:
    """
    events = Events()
    pprint(incoming_events)
    for hashcode, event_dict in incoming_events.items():
        end_date_and_time = event_dict["end_date_and_time"]
        location = event_dict["location"]
        name = event_dict["name"]
        rsvp_deadline = event_dict["rsvp_deadline"]
        stage = event_dict["stage"]  # TODO: change to str value iso dict val.
        start_date_and_time = event_dict["start_date_and_time"]
        event = Event(
            end_date_and_time=end_date_and_time,
            location=location,
            name=name,
            participants=[],
            rsvp_deadline=rsvp_deadline,
            stage=stage,
            start_date_and_time=start_date_and_time,
        )

        # TODO; verify hash in new event object is same as hash from dict.
        if hashcode == "":
            print("TODO")
        add_object_to_dict(events, event)

    return events


def convert_group_list_groups(group_list: List) -> Groups:
    """Converts a list of group dictionaries into a Groups object.

    :param group_list: List:
    :param group_list: List:
    """
    groups = Groups()
    for group_dict in group_list:
        group = Group(
            name=group_dict["name"], participants=group_dict["participants"]
        )
        # TODO; verify hash in new event object is same as hash from dict.
        add_object_to_dict(groups, group)

    return groups
