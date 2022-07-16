"""Stores event information."""
from datetime import datetime
from typing import List

from src.helper import parse_string
from src.Plural import Plural

# from src.Person import Person


# pylint: disable=R0903
class Events(Plural):
    """Stores the Event objects."""


class Event_stage:
    """Stage of event."""

    # pylint: disable=R0903
    def __init__(self, stage):
        if stage == "planning":
            self.stage = "planning"
        elif stage == "contacting":
            self.stage = "contacting"
        elif stage == "confirmed":
            self.stage = "confirmed"
        elif stage == "preparation":
            self.stage = "preparation"
        elif stage == "active":
            self.stage = "active"
        elif stage == "ended":
            self.stage = "ended"
        elif stage == "completed":
            self.stage = "completed"
        else:
            raise Exception(f"Unsupported event stage:{stage}")


class Event:
    """Information on event."""

    # pylint: disable=R0903
    # pylint: disable=R0913
    def __init__(
        self,
        end_date_and_time: datetime,
        location: dict,
        name: str,
        # participants: List[Person],
        participants: List,
        rsvp_deadline: datetime,
        stage: Event_stage,
        start_date_and_time: datetime,
    ):
        # Person identification
        self.name: str = parse_string(name)
        self.location: str = parse_string(location)
        self.start_date_and_time: datetime = start_date_and_time
        self.end_date_and_time: datetime = end_date_and_time
        self.rsvp_deadline: datetime = rsvp_deadline
        # self.participants: List[Person] = participants
        self.participants = self.add_participants(participants)
        self.stage: Event_stage = stage
        # TODO: assert error is thrown if event is not included in person
        # afterwards.

    def add_participants(self, participants):
        """Ensures the event is added to participant, and verifies list
        elements are of type person."""
        for participant in participants:
            # if not isinstance(participant,Person):
            #    raise Exception(
            # f"Event particpiants are expected to be of"
            # f"type:{Person}."
            # )
            if self in participant.events:
                raise Exception(
                    "Error, event is already added to participant."
                )
            participant.events.append(self)
        return participants

    def verify_location(self, location):
        """Verifies the location dictionary contains valid data types."""
        if "address" in location.keys():
            if not isinstance(location["address"], str):
                raise Exception("Address was not of type string.")
        raise Exception("Other location types are not yet supported.")
