"""Entry point of code, run it with: python -m src from the root directory of
this repository.

Checks if private data structures exist, and if not, creates a template
private data structure that you can adjust.
"""

from pprint import pprint

from installation.install_sms_reader import get_sms_messages_from_phone
from src.helper import load_dict_from_file
from src.management.create_people import scan_input_vcfs
from src.management.create_vcf import VCF_creator

output_dir = "sms_ie_output"
private_dir = "private_data/"
sms_ie_dict = {
    # ensure_private_data_templates_exist(private_dir)
    "output_dir": output_dir,
    "output_dirpath": f"/sdcard/Download/{output_dir}/",
    "phone_xml_path": "/data/data/com.github.tmo1.sms_ie/shared_prefs/com."
    + "github.tmo1.sms_ie_preferences.xml",
    "local_xml_path": "installation/com.github.tmo1.sms_ie_preferences.xml",
    "package_name": "com.github.tmo1.sms_ie",
    "private_dir": private_dir,
    "local_sms_filepath": "private_data/messages.json",
    "persons_filepath": f"{private_dir}persons.json",
    "events_filepath": f"{private_dir}events.json",
    "groups_filepath": f"{private_dir}groups.json",
    "vcf_input_path": f"{private_dir}/input_vcf",
    "vcf_output_path": f"{private_dir}/output_vcf",
}
pprint(sms_ie_dict)


# Specify vcf in and output files.
# output_vcf_filepath = "private_data/output.vcf"
# input_vcf_filepath = "private_data/input.vcf"

scan_input_vcfs(sms_ie_dict)

# Create a vcf file.
folder_name = "private_data"
first_name = "firstname"
last_name = "lastname"
tel_mobile = "0612345678"
tel_home = ""
tel_work = ""
email_home = "something@something.com"
email_work = ""
email_mobile = ""
adr_work = "Some street 22 somecity somecountry"
adr_home = ""
website_url = "https://www.somesite.com"
VCF_creator(
    folder_name,
    first_name,
    last_name,
    tel_mobile,
    tel_home,
    tel_work,
    email_home,
    email_work,
    email_mobile,
    adr_work,
    adr_home,
    website_url,
)

# Load a vcf file to dict.

# TODO: change output to sms_messages.json in messages folder.
sms_messages = get_sms_messages_from_phone(sms_ie_dict)
sms_messages = load_dict_from_file(sms_ie_dict["local_sms_filepath"])
