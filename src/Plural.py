"""Contains object that stores groups."""


class Plural(dict):
    """Stores the Group objects."""

    def add_elem(self, hash_code, new_group):
        """Adds an element to the list of elements if it is not already in."""
        if not isinstance(self, dict):
            raise Exception(
                "Error, the object is not a list, so cannot append."
            )
        # TODO: verify hash belongs to new_group
        for elem in self.values():
            if elem.name == new_group.name:
                raise Exception(
                    "Error, can't add group, it is already in "
                    + f"the list:{self}."
                )
        self[hash_code] = new_group
