"""Short method to create vcf file."""

import vobject


def create_minimal_vcf_file(vcf_filepath):
    """Creates a .vcf file from a dictionary."""
    person = {
        "n": "Forrest Gump",
        "fn": "Forrest Gump",
        "tel": "(111) 555-1212",
        "email": "forrestgump@example.com",
        "photo": ";http://www.example.com/dir_photos/my_photo.gif",
        "adr": "Kathmandu, Nepal",
    }

    vcard = vobject.readOne("\n".join([f"{k}:{v}" for k, v in person.items()]))
    vcard.name = "VCARD"
    vcard.useBegin = True
    vcard.prettyPrint()

    with open(vcf_filepath, "w", newline="", encoding="utf-8") as f:
        f.write(vcard.serialize())
