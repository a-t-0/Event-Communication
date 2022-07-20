"""Commonly used helper functions."""
import copy
from pprint import pprint

from src.Event import Event
from src.Group import Group
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

    if origin_type == Group and not (
        isinstance(obj, Person) and (key == "groups")
    ):
        data[key] = to_dict(value, classkey, origin_type)
    if (
        origin_type == Group
        and (isinstance(obj, Person))
        and (key == "groups")
    ):
        for group in obj.groups:
            # Prgroup participants of group of participant of groups from
            # being printed
            group_without_participants = copy.deepcopy(group)
            group_without_participants.participants = None
            to_dict(group_without_participants, classkey, origin_type)

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


def add_hash_code(obj):
    """Adds a hash code based on the event dictionary."""
    the_dict = to_dict(obj)
    pprint(the_dict)
    if "hash_code" in the_dict.keys():
        raise Exception(f"Error, hash code already set for event:{the_dict}")

    # obj.unique_hash = hash(frozenset(the_dict))
    # obj.unique_hash = dict_hash(the_dict)
    obj.unique_hash = make_hash(the_dict)
    # obj.unique_hash = sha256(frozenset(the_dict))
    return obj.unique_hash


def make_hash(o):

    """Makes a hash from a dictionary, list, tuple or set to any level, that
    contains only other hashable types (including any lists, tuples, sets, and
    dictionaries)."""

    if isinstance(o, (set, tuple, list)):

        return tuple(make_hash(e) for e in o)

    if not isinstance(o, dict):

        return hash(o)

    new_o = copy.deepcopy(o)
    for k, v in new_o.items():
        new_o[k] = make_hash(v)

    return hash(tuple(frozenset(sorted(new_o.items()))))
