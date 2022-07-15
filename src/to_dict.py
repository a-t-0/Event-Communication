"""Commonly used helper functions."""
import copy

from src.Event import Event
from src.Person import Person


def to_dict(obj, classkey=None, origin_type=None):
    """Convertes an object recursively to a dictionary.

    :param obj: The object that is converted to a dictionary.
    :param classkey:  (Default value = None)
    """
    if origin_type is None:
        origin_type = type(obj)

    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = to_dict(v, classkey, origin_type=origin_type)
        return data
    if hasattr(obj, "_ast"):
        # pylint: disable=W0212
        return to_dict(obj._ast(), origin_type=origin_type)
    if hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [to_dict(v, classkey, origin_type=origin_type) for v in obj]
    if hasattr(obj, "__dict__"):
        data = {}
        for key, value in obj.__dict__.items():
            if not callable(value) and not key.startswith("_"):
                convert_attributes_to_dict(
                    classkey, data, (key, value), obj, origin_type
                )

        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    return obj


def convert_attributes_to_dict(classkey, data, item, obj, origin_type):
    """Ensures a recursive loop between Persons attending Events, and Events
    containing Persons, is broken.

    Helps recursively converting objects and attributes to dict.
    """
    # unpack item
    key, value = item

    if origin_type == Event and not (
        isinstance(obj, Person) and (key == "events")
    ):
        data[key] = to_dict(value, classkey, origin_type)
    if (
        origin_type == Event
        and (isinstance(obj, Person))
        and (key == "events")
    ):
        for event in obj.events:
            # Prevent participants of event of participant of events from
            # being printed
            event_without_participants = copy.deepcopy(event)
            event_without_participants.participants = None
            to_dict(event_without_participants, classkey, origin_type)

    if origin_type == Person and not (
        isinstance(obj, Event) and (key == "participants")
    ):
        data[key] = to_dict(value, classkey, origin_type)

    if (
        origin_type == Person
        and (isinstance(obj, Event))
        and (key == "participants")
    ):
        for participant in obj.participants:
            # Prevent events of participants of events of person from
            # being printed.
            participant_without_events = copy.deepcopy(participant)
            participant_without_events.events = None
            to_dict(participant_without_events, classkey, origin_type)
