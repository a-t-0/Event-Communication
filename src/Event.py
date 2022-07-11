"""Stores event information."""
from datetime import datetime

from helper import parse_string


class Event:
    """Information on event."""

    # pylint: disable=R0903
    def __init__(self, name: str, location: str, date_and_time: datetime):
        # Person identification
        self.name: str = parse_string(name)
        self.location: str = parse_string(location)
        self.datetime: datetime = date_and_time
