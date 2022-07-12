"""Contains details of a person."""
import re
from typing import List

import phonenumbers

from Event import Event
from helper import parse_string, yes_or_no

# TODO: support VCF importing and exporting.
# https://vcfpy.readthedocs.io/en/stable/


class Person_information:
    """Information of person in context to you."""

    # pylint: disable=R0903
    def __init__(
        self, first_name: str, known_from=None, last_name=None, state=None
    ):
        # Person identification
        self.first_name: str = parse_string(first_name)
        self.last_name: str = parse_string(last_name)
        self.known_from: str = parse_string(known_from)

        # Person states, e.g. travelling, solid, liquid.
        self.states: List[str] = []
        self.states.append(parse_string(state))

    def add_state(self, state: str):
        """Adds an state to the state list that person attends.

        Throws error if the state already is in the list of states of
        that person.
        """
        if state in self.states:
            raise Exception(f"Error, {state} is already in the states.")
        self.states.append(state)


class Contact_info:
    """Contact information."""

    # pylint: disable=R0913
    # pylint: disable=R0903
    def __init__(self, phone_nrs, emails, github, linkedin, facebook, other):
        # Person contact information
        self.phone_nrs: dict = phonenumbers.parse(phone_nrs, None)
        self.emails: dict = valid_email(emails)
        self.github: str = parse_string(github)
        self.linkedin: str = parse_string(linkedin)
        self.facebook: str = parse_string(facebook)
        self.other: str = parse_string(other)

    def parse_phone_nrs(self, phone_nrs: dict):
        """Ensures phone nr is valid and then adds it to the dictionary with
        phone numbers, if it was not in yet.

        Otherwise asks user what to do.
        """
        valid_phone_nrs: dict = {}
        for nr_description, phone_nr in phone_nrs.items():

            # If phone number already in, ask user for verification.
            if nr_description in self.phone_nrs.keys():
                if yes_or_no(
                    f"{nr_description} is already in the phone nr list, with "
                    + f"nr: {self.phone_nrs[nr_description]}. Do you want to "
                    + f"overwrite  this with:{phone_nr}?"
                ):
                    valid_phone_nrs[nr_description] = phonenumbers.parse(
                        phone_nr, None
                    )
                else:
                    print(f"Nr ignored:{phone_nr}")

            # Add number if it was not yet found
            valid_phone_nrs[nr_description] = phonenumbers.parse(
                phone_nr, None
            )
        return valid_phone_nrs


class Person:
    """Contains details of a person."""

    # pylint: disable=R0903
    def __init__(
        self,
        person_info: Person_information,
        contact_info: Contact_info,
        events: List[Event],
    ):
        self.person_info = person_info
        self.contact_info = contact_info
        self.events: List[Event] = events
        # self.__dict__

    def add_event(self, event: Event):
        """Adds an event to the event list that person attends.

        Throws error if the event already is in the list of events of
        that person.
        """
        if event in self.events:
            raise Exception(f"Error, {event.name} is already in the events.")
        self.events.append(event)


def valid_email(email: str):
    """Verifies email address is valid.

    :param email:
    """
    if isinstance(email, type(None)):
        return None
    if isinstance(email, str):
        return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))
    raise Exception(
        f"Error, string type was:{type(email)} "
        + "whereas it should be of type None or string."
    )
