"""Entry point of code, run it with: python -m src from the root directory of
this repository.

Checks if private data structures exist, and if not, creates a template
private data structure that you can adjust.
"""

from installation.install_sms_reader import get_sms_messages_from_phone
from src.helper import load_dict_from_file
from src.management.create_vcf import VCF_creator
from src.management.load_vcf2 import vcf_to_dict

output_dir = "sms_ie_output"
sms_ie_dict = {
    "private_dir": "private_data",
    # ensure_private_data_templates_exist(private_dir)
    "output_dir": output_dir,
    "output_dirpath": f"/sdcard/Download/{output_dir}/",
    "phone_xml_path": "/data/data/com.github.tmo1.sms_ie/shared_prefs/com."
    + "github.tmo1.sms_ie_preferences.xml",
    "local_xml_path": "installation/com.github.tmo1.sms_ie_preferences.xml",
    "package_name": "com.github.tmo1.sms_ie",
    "local_sms_messages_dir": "private_data/",
    "local_sms_filepath": "private_data/messages.json",
}

# Specify vcf in and output files.
output_vcf_filepath = "private_data/output.vcf"
input_vcf_filepath = "private_data/input.vcf"

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
vcf_to_dict(input_vcf_filepath)

sms_messages = get_sms_messages_from_phone(sms_ie_dict)
sms_messages = load_dict_from_file(sms_ie_dict["local_sms_filepath"])
