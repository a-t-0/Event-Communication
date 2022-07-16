"""Ensures sms messages can be read through adb."""
import hashlib
import os
import time
from typing import List

import requests  # type: ignore[import]

from src.helper import create_and_write_file, load_dict_from_file
from src.sender.helper_sms import cmd_res, device_ready


def sms_ie_config_content(int_time: int, output_dir: str) -> List[str]:
    """Creates the sms_ie .xml config file content to schedule an export at the
    time: int time.

    int_time contains the number of minutes after midnight on which an
    sms export is scheduled.

    :param int_time: int:
    :param output_dir: str:
    :param int_time: int:
    :param output_dir: str:

    """

    content = [
        "<?xml version='1.0' encoding='utf-8' standalone='yes' ?>",
        "<map>",
        '    <boolean name="include_binary_data" value="true" />',
        '    <boolean name="mms" value="true" />',
        '    <string name="max_messages"></string>',
        '    <boolean name="schedule_export" value="true" />',
        '    <boolean name="sms" value="true" />',
        '    <boolean name="debugging" value="false" />',
        '    <boolean name="export_call_logs" value="true" />',
        f'    <int name="export_time" value="{int_time}" />',
        '    <boolean name="export_messages" value="true" />',
        '    <string name="export_dir">content://com.android.providers.'
        + "downloads.documents/tree/raw%3A%2Fstorage%2Femulated%2F0%2FDo"
        + f"wnload%2F{output_dir}</string>",
        "</map>",
    ]
    return content


def sha256(fname: str) -> str:
    """Computes the sha256 sum of a file.

    :param fname:
    """
    hash_sha256 = hashlib.sha256()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def get_file(url: str, filename: str, expected_hash: str) -> None:
    """Downloads a file and verifies its filecontent is as expected.

    :param url: param filename:
    :param expected_hash:
    :param filename:
    """
    if not sms_ie_apk_file_exists(filename, expected_hash):
        response = requests.get(url)
        with open(filename, "wb") as some_file:
            some_file.write(response.content)
    assert_sms_ie_apk_file_exists(filename, expected_hash)


def assert_sms_ie_apk_file_exists(filename: str, expected_hash: str) -> None:
    """Verifies a file exists and that its content is as expected. Throws error
    if file does not exist or if the content is not expected.

    :param filename: param expected_hash:
    :param expected_hash:
    """
    if not os.path.exists(filename):
        raise Exception(f"Error, filename={filename} did not exist.")
    if expected_hash is not None:
        if sha256(filename) != expected_hash:
            raise Exception(f"Download is corrupted, {sha256(filename)}.")


def sms_ie_apk_file_exists(filename: str, expected_hash: str) -> bool:
    """Returns True a file exists and that its content is as expected. Returns
    False otherwise.

    :param filename: param expected_hash:
    :param expected_hash:
    """
    if not os.path.exists(filename):
        return False
    if sha256(filename) != expected_hash:
        return False
    return True


def app_is_installed(package_name: str) -> bool:
    """Verifies an application is installed on the phone.

    :param package_name:
    """

    installation_response = cmd_res(
        f"adb shell pm list packages {package_name}"
    )
    return installation_response == f"package:{package_name}\n"


def adb_install_apk(filename: str, package_name: str) -> None:
    """Installs an application and verifies it is installed.

    :param filename: param package_name:
    :param package_name:
    """
    if not app_is_installed(package_name):
        installation_response = cmd_res(f"adb install {filename}")
        print(f"installation_response={installation_response}")
    if not app_is_installed(package_name):
        raise Exception(
            f"Error, after installation, package:{package_name} "
            + "was not found."
        )


def ensure_sms_ie_config_file_exists(xml_path: str) -> None:
    """Ensures the configuration for the SMS Import/Export applictation exists.

    :param xml_path:
    """
    # Ensure the app directory exists.
    assert_dir_exists_on_phone("/data/data/com.github.tmo1.sms_ie/")
    ensure_dir_exists_on_phone(
        "/data/data/com.github.tmo1.sms_ie/shared_prefs/"
    )

    ensure_file_exists_on_phone(xml_path)


def create_sms_ie_output_folder(output_path: str) -> None:
    """Creates the output directory on the phone to which the sms messages will
    be exported.

    :param output_path: str:
    :param output_path: str:
    """
    ensure_dir_exists_on_phone(output_path)


def ensure_dir_exists_on_phone(path: str) -> None:
    """Creates a directory if it does not yet exist on the phone.

    :param path:
    """
    command = f"adb shell mkdir -p {path}"
    cmd_res(command)

    assert_dir_exists_on_phone(path)


def assert_dir_exists_on_phone(path: str) -> None:
    """Throws error if a directory does not yet exist on the phone.

    :param path:
    """
    command = f'adb shell [ -d {path} ] && echo "exists."'
    output = cmd_res(command)
    if output != "exists.\n":
        raise Exception(f"Error, app dir:{path} is not found.")


def file_exists_on_phone(filepath: str) -> bool:
    """Returns True if a file exists on the phone. Returns False otherwise.

    :param filepath:
    """
    command = f'adb shell [ -f {filepath} ] && echo "exists."'
    output = cmd_res(command)
    if output != "exists.\n":
        return False
    return True


def remove_file_if_exists_on_phone(filepath: str) -> None:
    """Removes file from phone if it exists.

    :param filepath:
    """
    if file_exists_on_phone(filepath):
        command = f"adb shell rm {filepath}"
        cmd_res(command)
    assert_file_does_not_exists_on_phone(filepath)


def assert_file_does_not_exists_on_phone(filepath: str) -> None:
    """Throws error if file exists on phone.

    :param filepath:
    """
    if file_exists_on_phone(filepath):
        raise Exception("Error file:{filepath} still exists on phone.")


def assert_file_exists_on_phone(filepath: str) -> None:
    """Throws error if a file does not exist on the phone.

    # TODO: verify this is not a duplicate function.

    :param filepath:
    """
    if not file_exists_on_phone(filepath):
        raise Exception("Error file:{filepath} still exists on phone.")


def ensure_file_exists_on_phone(path: str) -> None:
    """Creates a file if it does not yet exist on the phone.

    # TODO: verify this is not a duplicate function.

    :param path:
    """
    command = f"adb shell touch {path}"
    cmd_res(command)
    assert_file_exists_on_phone(path)


def copy_file_from_pc_to_phone(
    local_filepath: str, phone_filepath: str
) -> None:
    """Copies a file from the pc to the phone.

    :param local_filepath: param phone_filepath:
    :param phone_filepath:
    """
    # Overwrite file content

    command = f"adb push {local_filepath} {phone_filepath}"
    print(f"command={command}")
    # TODO: verify mdf5 values are identical
    cmd_res(command)


def copy_file_from_phone_to_pc(
    phone_filepath: str, local_filepath: str
) -> None:
    """Copies a file from the phone to the pc.

    :param phone_filepath: param local_filepath:
    :param local_filepath:
    """
    # Overwrite file content

    command = f"adb pull {phone_filepath} {local_filepath}"
    print(f"command={command}")
    # TODO: verify mdf5 values are identical
    cmd_res(command)


def verify_app_is_in_foreground(package_name: str) -> None:
    """Verify an app is opened and into the foreground.

    :param package_name:
    """

    command = (
        "adb shell dumpsys activity recents | grep 'Recent #0' | cut -d="
        + " -f2 | sed 's| .*||' | cut -d '/' -f1"
    )
    output = cmd_res(command)
    if output != f"{package_name}\n":
        raise Exception(
            "Error, app is not running in the foreground. Please try again."
        )


def restart_application(package_name: str) -> None:
    """Restarts an application.

    :param package_name: str:
    :param package_name: str:
    """

    command = f"adb shell am force-stop {package_name}"
    cmd_res(command)
    # command=f"adb shell monkey -p '{package_name}' 1"
    # Works but does not export according to schedule.
    command = (
        f"adb shell am start -n {package_name}/{package_name}.MainActivity"
    )
    print(f"command={command}")
    cmd_res(command)
    time.sleep(2)


def screen_is_locked() -> bool:
    """Returns True if the screen is locked.

    Returns False if the screen is unlocked.
    """
    command = "adb shell dumpsys power | grep 'mHolding'"
    output = cmd_res(command)
    lines = output.split()
    if (
        lines[0] == "mHoldingWakeLockSuspendBlocker=true"
        and lines[1] == "mHoldingDisplaySuspendBlocker=true"
    ):
        return False
    if (
        lines[0] == "mHoldingWakeLockSuspendBlocker=true"
        and lines[1] == "mHoldingDisplaySuspendBlocker=false"
    ):
        return True
    raise Exception(f"Unexpected output in check if screen is locked:{output}")


def clear_app_data(package_name) -> None:
    """Deletes application data.

    :param package_name:
    """
    command = f"adb shell pm clear {package_name}"
    cmd_res(command)


def send_export_sms_inputs(
    package_name, keystrokes: List[int], pause_time: int
) -> None:
    """Sends keystrokes to phone.

    :param package_name: param keystrokes: List[int]:
    :param pause_time: int:
    :param keystrokes: List[int]:
    :param pause_time: int:
    """
    time.sleep(pause_time)
    for keystroke in keystrokes:
        verify_app_is_in_foreground(package_name)
        command = f"adb shell input keyevent {keystroke}"
        cmd_res(command)
        time.sleep(pause_time)


def get_phone_date():
    """Gets current date from phone in format yyyy-mm-dd."""
    command = "adb shell date +%F"
    date = cmd_res(command)
    return date.strip()  # removes newlines


def get_phone_time(buffer_sec: int) -> tuple[int, int]:
    """Gets the time from the phone, and computes whether the time up to the
    next whole minute is enough or whether the code should wait an additional
    minute.

    :param buffer_sec: int:
    :param buffer_sec: int:
    """
    # TODO: change to: date +%T for HH:MM:SS format without parsing
    command = "adb shell date"
    date_and_time = cmd_res(command)
    time_elements = date_and_time.split(" ")

    # Extract the 18:19:20 time from the date and time string.
    for element in time_elements:
        if ":" in element:
            time_str = element

    # Split 18:19:20 into hrs, mins and seconds
    if time_str is None:
        raise Exception("Phone time not found")
    [hrs, mins, secs] = list(map(int, time_str.split(":")))
    print(f"{hrs}:{mins}:{secs}")
    wait_time = 60 - secs

    # Ensure a buffer in when to export, is taken into account.
    if secs + buffer_sec > 60:
        mins = mins + 1
        wait_time = wait_time + 60

    # Expected time:
    return (
        hrs * 60 + mins + 1,
        wait_time,
    )  # Plus 1 because the export should happen at the next minute.


def get_sms_messages_from_phone(sms_ie_dict) -> dict:
    """Gets sms messages from phone and stores them locally in a .json file.

    :param sms_ie_dict:
    """
    # Get the sms_ie .apk file from the release page.
    url = (
        "https://github.com/tmo1/sms-ie/releases/download/v1.4.1/com.github"
        + ".tmo1.sms_ie-v1.4.1.apk"
    )
    filename = "sms_ie.apk"
    expected_hash = (
        "185afc567ea5fce2df4045925687a79a717bd31185cd944a4c80c51e64ce77ec"
    )

    get_file(url, filename, expected_hash=expected_hash)

    # Connect to phone through adb
    # check if device connected
    if device_ready():

        # Install sms_ie.apk file.
        adb_install_apk(filename, sms_ie_dict["package_name"])

        clear_app_data(sms_ie_dict["package_name"])

        # Verify sms_ie config file is found and exists.
        ensure_sms_ie_config_file_exists(sms_ie_dict["phone_xml_path"])

        # Specify output directory on android device.
        # Verify output directory exists on android device.
        create_sms_ie_output_folder(sms_ie_dict["output_dirpath"])

        # Delete sms_ie output file if it exists on phone.
        output_filepath = (
            f'{sms_ie_dict["output_dirpath"]}messages-{get_phone_date()}.json'
        )
        print(f"output_filepath={output_filepath}")
        remove_file_if_exists_on_phone(output_filepath)

        # Get the time on the phone and add buffer of 10 seconds.
        export_time, wait_time = get_phone_time(5)
        print(f"export_time={export_time}")
        print(f"wait_time={wait_time}")

        # Verify config file contains schedule, and if not overwrite config.
        config_content = sms_ie_config_content(
            export_time, sms_ie_dict["output_dir"]
        )

        # Create local copy of file content:
        create_and_write_file(sms_ie_dict["local_xml_path"], config_content)

        # Push config file to device.
        copy_file_from_pc_to_phone(
            sms_ie_dict["local_xml_path"], sms_ie_dict["phone_xml_path"]
        )

        if not screen_is_locked():
            clear_app_data(sms_ie_dict["package_name"])

            # Restart sms_ie application
            restart_application(sms_ie_dict["package_name"])

            # enter, enter
            time.sleep(2)
            print("pressing enter 4 times, to grant permissions")
            send_export_sms_inputs(
                sms_ie_dict["package_name"], [23, 23, 23, 23], 1
            )

            print("pressing enter,tab, enter to export sms output")
            # enter, tab, enter
            send_export_sms_inputs(
                sms_ie_dict["package_name"], [23, 61, 23], 1
            )
            print("Waiting 15 seconds for the export of data to be completed.")
            time.sleep(15)

            # Wait for wait time+file creation duration buffer
            print(
                f"Waiting for:{wait_time} seconds until sms data export file"
                + " is created."
            )
            time.sleep(wait_time)

            # Verify output file exists
            assert_file_exists_on_phone(output_filepath)

            # Copy file from phone to local storage
            copy_file_from_phone_to_pc(
                output_filepath, sms_ie_dict["local_sms_filepath"]
            )

            # Verify the sms messages file exists locally.
            if not os.path.exists(sms_ie_dict["local_sms_filepath"]):
                raise Exception(
                    f"Error, filename={sms_ie_dict['local_sms_filepath']} did"
                    + " not exist."
                )

        else:
            raise Exception("Error, please unlock screen and try again.")
    else:
        raise Exception("Please connect phone and enable adb, and try again.")

    # Load sms_ie output file content.
    sms_messages = load_dict_from_file(sms_ie_dict["local_sms_filepath"])
    return sms_messages
