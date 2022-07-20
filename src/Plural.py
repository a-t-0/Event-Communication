"""Contains object that stores groups."""


class Plural(dict):
    """Stores a list of unique objects."""

    def add_elem(self, hash_code, new_item):
        """Adds an element to the list of elements if it is not already in."""
        print(f"hash_code={hash_code}")
        if not isinstance(self, dict):
            raise Exception(
                "Error, the object is not a list, so cannot append."
            )
        # TODO: verify hash belongs to new_group
        for elem in self.values():

            if hasattr(elem, "name"):
                if elem.name == new_item.name:
                    raise Exception(
                        f"Error, can't add: {new_item.name}, it is already in "
                        + f"the list:{self}."
                    )
            elif hasattr(elem, "person_info") and hasattr(
                elem.person_info, "first_name"
            ):
                if (
                    elem.person_info.first_name
                    == new_item.person_info.first_name
                    and (
                        elem.person_info.last_name
                        == new_item.person_info.last_name
                    )
                ):
                    for some_hash, person in self.items():
                        print(
                            f"{some_hash} {person.person_info.first_name} "
                            + f"{person.person_info.last_name}"
                        )
                    merge_person(elem.__dict__, new_item.__dict__)
            else:
                raise Exception(
                    "Object type not supported, it does not have"
                    + " name, nor first_name. Meaning it is not a "
                    + "Group, nor an Event, neither a Person."
                    + f"type:{type(elem)}, {elem.person_info.first_name}"
                )
        self[hash_code] = new_item


def merge_person(old_person_dict: dict, new_person_dict: dict):
    """Merges the new person information into the old person information if
    there is a difference and the old person did not yet have that attribute.

    TODO: allow for overwriting blank/default values from new to old.
    """
    # Check if new person has different values.
    for attr, value in old_person_dict.items():
        if attr in new_person_dict.keys():
            if attr in ["person_info", "contact_info"]:
                merge_person(
                    old_person_dict[attr].__dict__,
                    new_person_dict[attr].__dict__,
                )
            elif isinstance(value, dict):
                merge_person(value, new_person_dict[attr])
            else:
                if value != new_person_dict[attr]:
                    raise Exception(
                        f"Error, new_person_dic has attr[{attr}]:"
                        + f"{new_person_dict.__dict__[attr]}, yet "
                        + f"old_person_dict has:{value}"
                    )
    # Check if new person has different attributes:
    print(f"new_person_dict={new_person_dict}")
    if isinstance(new_person_dict, dict):
        for attr, value in new_person_dict.items():
            if attr not in old_person_dict.keys():
                # TODO: verify if you can set attribute value by name like
                # this.
                old_person_dict.__dict__[attr] = value
