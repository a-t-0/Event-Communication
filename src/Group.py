"""Contains object that stores groups."""


from ast import List

from src.helper import parse_string


class Group:
    """Stores details of a group of people."""

    # pylint: disable=R0903
    def __init__(
        self,
        name: str,
        participants: List,
    ):
        self.name: str = parse_string(name)
        self.participants = self.add_participants(participants)

    def add_participants(self, participants):
        """Ensures the group is added to participant, and verifies list
        elements are of type person."""
        for participant in participants:
            # if not isinstance(participant,Person):
            #    raise Exception(
            # f"Event particpiants are expected to be of"
            # f"type:{Person}."
            # )
            if self in participant.groups:
                raise Exception(
                    "Error, event is already added to participant."
                )
            participant.groups.append(self)
        return participants
