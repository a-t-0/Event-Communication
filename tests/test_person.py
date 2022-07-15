"""Verifies The Supported_experiment_settings object catches invalid adaptation
specifications."""
# pylint: disable=R0801
import datetime
import unittest
from pprint import pprint

from samples.sample_persons import (
    get_sample_person_1_no_events,
    get_sample_person_two_events,
)
from src.to_dict import to_dict


class Test_person(unittest.TestCase):
    """Tests the person object can be converted to dict."""

    # Initialize test object
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_person_to_dict(self):
        """Verifies a person object can be converted to dict.."""

        person = get_sample_person_1_no_events()
        # print(person.__dict__)
        pprint(to_dict(person, classkey=None))

        expected_dict = {
            "contact_info": {
                "emails": {"primary": True},
                "facebook": "https://www.github.com/facebook_user",
                "github": "https://www.github.com/some_github_user",
                "linkedin": "https://www.github.com/linkedin_user",
                "other": "Some string",
                "phone_nrs": {"mobile": "+32612345678"},
            },
            "events": [],
            "person_info": {
                "first_name": "One",
                "known_from": "Internet",
                "last_name": "Doe",
                "states": ["Walking"],
            },
        }

        self.assertEqual(expected_dict, to_dict(person, classkey=None))

    def test_person_to_dict_with_event(self):
        """Verifies a person object can be converted to dict.."""

        person = get_sample_person_two_events()
        # print(person.__dict__)
        pprint(to_dict(person, classkey=None))
        expected_dict = {
            "contact_info": {
                "emails": {"primary": True},
                "facebook": "https://www.github.com/facebook_user",
                "github": "https://www.github.com/some_github_user",
                "linkedin": "https://www.github.com/linkedin_user",
                "other": "Some string",
                "phone_nrs": {"mobile": "+32612345678"},
            },
            "events": [
                {
                    "end_date_and_time": datetime.datetime(
                        2020, 2, 2, 6, 2, 2
                    ),
                    "location": "Some street 2, some country, some planet,"
                    + " some universe.",
                    "name": "Event 1",
                    "rsvp_deadline": datetime.datetime(2020, 2, 2, 2, 2, 2),
                    "stage": {"stage": "planning"},
                    "start_date_and_time": datetime.datetime(
                        2020, 2, 5, 2, 2, 2
                    ),
                },
                {
                    "end_date_and_time": datetime.datetime(
                        2020, 1, 1, 5, 1, 1
                    ),
                    "location": "Some street 1, some country, some planet, "
                    + "some universe.",
                    "name": "Event 2",
                    "rsvp_deadline": datetime.datetime(2020, 1, 1, 1, 1, 1),
                    "stage": {"stage": "planning"},
                    "start_date_and_time": datetime.datetime(
                        2020, 1, 4, 1, 1, 1
                    ),
                },
            ],
            "person_info": {
                "first_name": "Jonna",
                "known_from": "Internet",
                "last_name": "Doe",
                "states": ["Walking"],
            },
        }

        self.assertEqual(expected_dict, to_dict(person, classkey=None))
