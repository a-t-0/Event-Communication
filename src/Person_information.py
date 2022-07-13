"""Contains details of a person."""
from typing import List

from src.helper import parse_string

# import phonenumbers


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
