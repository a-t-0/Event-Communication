"""Returns sample data containing events, for testing purposes."""
# Specify person information
import datetime

from samples.sample_persons import (
    get_sample_person_1_no_events,
    get_sample_person_2_no_events,
)
from src.Event import Event, Event_stage


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
