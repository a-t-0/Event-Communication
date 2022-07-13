"""Contains details of a person."""
import re

import phonenumbers

from src.helper import parse_string, yes_or_no

# TODO: support VCF importing and exporting.
# https://vcfpy.readthedocs.io/en/stable/


class Contact_info:
    """Contact information."""

    # pylint: disable=R0913
    # pylint: disable=R0903
    def __init__(self, phone_nrs, emails, github, linkedin, facebook, other):
        # Person contact information
        # self.phone_nrs: dict = phonenumbers.parse(phone_nrs, None)
        self.phone_nrs: dict = phone_nrs
        self.emails: dict = self.parse_emails(emails)
        self.github: str = parse_string(github)
        self.linkedin: str = parse_string(linkedin)
        self.facebook: str = parse_string(facebook)
        self.other: str = parse_string(other)

    def parse_emails(self, emails: dict) -> dict:
        """Verifies the emails are valid and then returns the dictionary with
        email descriptions as key and email addresses as values."""
        for description, email in emails.items():
            emails[description] = self.valid_email(email)
        return emails

    def parse_phone_nrs(self, phone_nrs: dict):
        """Ensures phone nr is valid and then adds it to the dictionary with
        phone numbers, if it was not in yet.

        Otherwise asks user what to do.
        """
        valid_phone_nrs: dict = {}
        for nr_description, phone_nr in phone_nrs.items():

            # If phone number already in, ask user for verification.
            if nr_description in self.phone_nrs.keys():
                if yes_or_no(
                    f"{nr_description} is already in the phone nr list, with "
                    + f"nr: {self.phone_nrs[nr_description]}. Do you want to "
                    + f"overwrite  this with:{phone_nr}?"
                ):
                    valid_phone_nrs[nr_description] = phonenumbers.parse(
                        phone_nr, None
                    )
                else:
                    print(f"Nr ignored:{phone_nr}")

            # Add number if it was not yet found
            valid_phone_nrs[nr_description] = phonenumbers.parse(
                phone_nr, None
            )
        return valid_phone_nrs

    def valid_email(self, email: str):
        """Verifies email address is valid.

        :param email:
        """
        if isinstance(email, type(None)):
            return None
        if isinstance(email, str):
            return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))
        raise Exception(
            f"Error, string type was:{type(email)} "
            + "whereas it should be of type None or string."
        )
