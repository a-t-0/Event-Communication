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
                    raise Exception(
                        f"Error, can't add: {new_item.person_info.first_name},"
                        + f" {new_item.person_info.last_name}"
                        + " it is already in "
                        + f"the list:{self}."
                    )
            else:
                raise Exception(
                    "Object type not supported, it does not have"
                    + " name, nor first_name. Meaning it is not a "
                    + "Group, nor an Event, neither a Person."
                    + f"type:{type(elem)}, {elem.person_info.first_name}"
                )
        self[hash_code] = new_item
