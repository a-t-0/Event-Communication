"""Verifies The Supported_experiment_settings object catches invalid adaptation
specifications."""
# pylint: disable=R0801
import datetime
import unittest
from pprint import pprint

from samples.sample_persons import get_sample_event_1
from src.Person import Contact_info, Person_information
from src.to_dict import to_dict

# Specify person information
person_information = Person_information(
    first_name="Jonna",
    states=["Walking"],
    known_from="Internet",
    last_name="Doe",
)
# Specify contact information
phone_nrs = {"mobile": "+32612345678"}
emails = {"primary": "some_email@some_email.com"}
github = "https://www.github.com/some_github_user"
linkedin = "https://www.github.com/linkedin_user"
facebook = "https://www.github.com/facebook_user"
other = "Some string"
contact_info = Contact_info(
    phone_nrs, emails, github, linkedin, facebook, other
)


class Test_person(unittest.TestCase):
    """Tests the person object can be converted to dict."""

    # Initialize test object
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def test_person_to_dict(self):
        """Verifies a person object can be converted to dict.."""

        event = get_sample_event_1()

        pprint(to_dict(event, classkey=None))

        expected_dict = {
            "end_date_and_time": datetime.datetime(2020, 2, 2, 6, 2, 2),
            "location": "Some street 2, some country, some planet, some "
            + "universe.",
            "name": "Event 1",
            "participants": [
                {
                    "contact_info": {
                        "emails": {"primary": "some_email@some_email.com"},
                        "facebook": "https://www.github.com/facebook_user",
                        "github": "https://www.github.com/some_github_user",
                        "linkedin": "https://www.github.com/linkedin_user",
                        "other": "Some string",
                        "phone_nrs": {"mobile": "+32612345678"},
                    },
                    "groups": [],
                    "person_info": {
                        "first_name": "One",
                        "known_from": "Internet",
                        "last_name": "Doe",
                        "states": ["Walking"],
                    },
                },
                {
                    "contact_info": {
                        "emails": {"primary": "some_email@some_email.com"},
                        "facebook": "https://www.github.com/facebook_user",
                        "github": "https://www.github.com/some_github_user",
                        "linkedin": "https://www.github.com/linkedin_user",
                        "other": "Some string",
                        "phone_nrs": {"mobile": "+32612345678"},
                    },
                    "groups": [],
                    "person_info": {
                        "first_name": "Two",
                        "known_from": "Internet",
                        "last_name": "Doe",
                        "states": ["Walking"],
                    },
                },
            ],
            "rsvp_deadline": datetime.datetime(2020, 2, 2, 2, 2, 2),
            "stage": {"stage": "planning"},
            "start_date_and_time": datetime.datetime(2020, 2, 5, 2, 2, 2),
        }

        self.assertEqual(expected_dict, to_dict(event, classkey=None))
