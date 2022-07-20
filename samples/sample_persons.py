"""Returns sample data containing persons, for testing purposes."""
# Specify person information
import datetime

from src.Contact_info import Contact_info
from src.Event import Event, Event_stage
from src.Group import Group
from src.Person import Person
from src.Person_information import Person_information


def get_sample_person_information(first_name: str = "Jonna"):
    """Returns sample person information.

    :param first_name: str:  (Default value = "Jonna")
    """
    person_information = Person_information(
        first_name=first_name,
        states=["Walking"],
        known_from="Internet",
        last_name="Doe",
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

    person = Person(person_information, contact_info, [], [])
    return person


def get_sample_person_2_no_events():
    """Returns sample person 2 that does not contain any events."""
    person_information = get_sample_person_information(first_name="Two")
    contact_info = get_sample_contact_information()

    person = Person(person_information, contact_info, [], [])
    return person


def get_sample_person_two_events():
    """Returns a sample person that attends 2 events."""
    person_information = get_sample_person_information()
    contact_info = get_sample_contact_information()

    person = Person(
        person_information,
        contact_info,
        [get_sample_event_1(), get_sample_event_2()],
        [],
    )
    return person


def get_sample_person_two_groups():
    """Returns a sample person that attends 2 groups.

    # TODO: test
    """
    person_information = get_sample_person_information()
    contact_info = get_sample_contact_information()

    person = Person(
        person_information,
        contact_info,
        [get_sample_group_1(), get_sample_group_2()],
    )
    return person


def get_sample_event_1():
    """Returns a sample event named: Event 1."""

    rsvp_deadline = datetime.datetime(
        year=2020, month=2, day=2, hour=2, minute=2, second=2
    )
    start_date_and_time = rsvp_deadline + datetime.timedelta(days=3)
    end_date_and_time = rsvp_deadline + datetime.timedelta(hours=4)
    location = "Some street 2, some country, some planet, some universe."
    name = "Event 1"
    participants = [
        get_sample_person_1_no_events(),
        get_sample_person_2_no_events(),
    ]
    stage = Event_stage("planning")

    event = Event(
        end_date_and_time=end_date_and_time,
        location=location,
        name=name,
        participants=participants,
        rsvp_deadline=rsvp_deadline,
        stage=stage,
        start_date_and_time=start_date_and_time,
    )
    return event


def get_sample_group_1():
    """Returns a sample group named: Group 1."""
    participants = [
        get_sample_person_1_no_events(),
        get_sample_person_2_no_events(),
    ]
    group = Group(name="Group 1", participants=participants)
    return group


def get_sample_group_2():
    """Returns a sample group named: Group 2."""
    participants = [
        get_sample_person_1_no_events(),
        get_sample_person_2_no_events(),
    ]
    group = Group(name="Group 2", participants=participants)
    return group


def get_sample_event_2():
    """Returns a sample event named: Event 1."""

    rsvp_deadline = datetime.datetime(
        year=2020, month=1, day=1, hour=1, minute=1, second=1
    )
    start_date_and_time = rsvp_deadline + datetime.timedelta(days=3)
    end_date_and_time = rsvp_deadline + datetime.timedelta(hours=4)
    location = "Some street 1, some country, some planet, some universe."
    name = "Event 2"
    participants = [
        get_sample_person_1_no_events(),
        get_sample_person_2_no_events(),
    ]
    stage = Event_stage("planning")

    event = Event(
        end_date_and_time=end_date_and_time,
        location=location,
        name=name,
        participants=participants,
        rsvp_deadline=rsvp_deadline,
        stage=stage,
        start_date_and_time=start_date_and_time,
    )
    return event
