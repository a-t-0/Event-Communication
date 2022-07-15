"""Verifies The Supported_experiment_settings object catches invalid adaptation
specifications."""
# pylint: disable=R0801
import unittest
from pprint import pprint

from samples.sample_persons import get_sample_person_1_no_events
from src.helper import todict


class Test_person(unittest.TestCase):
    """Tests the person object can be converted to dict."""

    # Initialize test object
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_person_to_dict(self):
        """Verifies a person object can be converted to dict.."""

        person = get_sample_person_1_no_events()
        # print(person.__dict__)
        pprint(todict(person, classkey=None))

        # pylint: disable=W1503
        self.assertFalse(True)
