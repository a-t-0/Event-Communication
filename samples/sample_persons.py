"""Returns sample data containing persons, for testing purposes."""
# Specify person information
from src.Contact_info import Contact_info
from src.Person import Person
from src.Person_information import Person_information


def get_sample_person_information(first_name: str = "Jonna"):
    """Returns sample person information.

    :param first_name: str:  (Default value = "Jonna")
    """
    person_information = Person_information(
        first_name=first_name,
        known_from="Internet",
        last_name="Doe",
        state="Walking",
    )
    return person_information


def get_sample_contact_information():
    """Returns sample contact information."""
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
    return contact_info


def get_sample_person_1_no_events():
    """Returns sample person 1 that does not contain any events."""
    person_information = get_sample_person_information(first_name="One")
    contact_info = get_sample_contact_information()

    person = Person(person_information, contact_info, [])
    return person


def get_sample_person_2_no_events():
    """Returns sample person 2 that does not contain any events."""
    person_information = get_sample_person_information(first_name="Two")
    contact_info = get_sample_contact_information()

    person = Person(person_information, contact_info, [])
    return person


def get_sample_person_two_events():
    """Returns a sample person that attends 2 events."""
    person_information = get_sample_person_information()
    contact_info = get_sample_contact_information()

    person = Person(person_information, contact_info, [])
    return person
