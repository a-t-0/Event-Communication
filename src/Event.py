"""Stores event information."""
from datetime import datetime

from src.helper import parse_string

# from src.Person import Person


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


class Event:
    """Information on event."""

    # pylint: disable=R0903
    # pylint: disable=R0913
    def __init__(
        self,
        date_and_time: datetime,
        location: str,
        name: str,
        # participants: List[Person],
        participants,
        stage: Event_stage,
    ):
        # Person identification
        self.name: str = parse_string(name)
        self.location: str = parse_string(location)
        self.datetime: datetime = date_and_time
        # self.participants: List[Person] = participants
        self.participants = participants
        self.stage: Event_stage = stage
