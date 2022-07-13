"""Contains details of a person."""
from typing import List

from src.Contact_info import Contact_info
from src.Event import Event
from src.Person_information import Person_information

# TODO: support VCF importing and exporting.
# https://vcfpy.readthedocs.io/en/stable/


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
