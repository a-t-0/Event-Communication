"""Contains details of a person."""
from typing import List

from src.Contact_info import Contact_info
from src.Event import Event
from src.Group import Group
from src.Person_information import Person_information
from src.Plural import Plural

# TODO: support VCF importing and exporting.
# https://vcfpy.readthedocs.io/en/stable/


# pylint: disable=R0903
class Persons(Plural):
    """Stores the Person objects."""


class Person:
    """Contains details of a person."""

    # pylint: disable=R0903
    def __init__(
        self,
        person_info: Person_information,
        contact_info: Contact_info,
        events: List[Event],
        groups: List[Group],
    ):
        self.person_info = person_info
        self.contact_info = contact_info
        self.events: List[Event] = events
        self.groups: List[Event] = groups
        # self.__dict__

    def add_event(self, event: Event):
        """Adds an event to the event list that person attends.

        Throws error if the event already is in the list of events of
        that person.
        """
        if event in self.events:
            raise Exception(f"Error, {event.name} is already in the events.")
        self.events.append(event)

    def add_group(self, group: Group):
        """Adds an group to the group list that person attends.

        Throws error if the group already is in the list of groups of
        that person.
        """
        if group in self.groups:
            raise Exception(f"Error, {group.name} is already in the groups.")
        self.groups.append(group)
