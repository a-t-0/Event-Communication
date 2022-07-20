"""Entry point of code, run it with: python -m src from the root directory of
this repository.

Checks if private data structures exist, and if not, creates a template
private data structure that you can adjust.
"""


from pprint import pprint

from installation.export_private_data import export_dict
from installation.install_sms_reader import get_sms_messages_from_phone
from src.arg_parser import parse_cli_args
from src.helper import load_dict_from_file
from src.management.create_minimal_vcf import create_minimal_vcf_file
from src.management.create_people import (
    convert_vcf_files_into_dictionaries,
    scan_input_vcfs,
)
from src.management.create_vcf import VCF_creator
from src.sender.helper_sms import cmd_res
from src.to_dict import to_dict

output_dir = "sms_ie_output"
private_dir = "private_data/"
settings = {
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
    "vcf_input_path": f"{private_dir}input_vcf/",
    "vcf_output_path": f"{private_dir}output_vcf/",
}

args = parse_cli_args()
print(args)
if args.install_signal_cli:
    output = cmd_res(
        "cd installation && chmod +x install_signal_cli.sh "
        + "&& ./install_signal_cli.sh"
    )
if args.install_sms_cli:
    # TODO: change output to sms_messages.json in messages folder.
    sms_messages = get_sms_messages_from_phone(settings)
    sms_messages = load_dict_from_file(settings["local_sms_filepath"])
if args.get_vcf_contacts:
    persons = scan_input_vcfs(settings)
    for hashcode, person in persons.items():
        print(f"hashcode={hashcode}")
        pprint(to_dict(person))
    export_dict(settings["persons_filepath"], persons)
if args.create_vcf_file_sample:
    # Create a detailed vcf file.
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

    # Create minimal vcf file
    create_minimal_vcf_file(
        f'{settings["private_dir"]}]minimal.vcf',
    )
if args.load_vcf_file_sample:
    # Load a vcf file to dict.
    convert_vcf_files_into_dictionaries(settings, [])
