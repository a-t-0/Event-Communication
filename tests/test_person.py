"""Verifies The Supported_experiment_settings object catches invalid adaptation
specifications."""
# pylint: disable=R0801
import unittest

from src.helper import todict
from src.Person import Contact_info, Person, Person_information

# Specify person information
person_information = Person_information(
    first_name="Jonna", known_from="Internet", last_name="Doe", state="Walking"
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

    def test_person_to_dict(self):
        """Verifies a person object can be converted to dict.."""

        person = Person(person_information, contact_info, [])
        print(person.__dict__)
        print(todict(person, classkey=None))

        # pylint: disable=W1503
        self.assertFalse(True)
