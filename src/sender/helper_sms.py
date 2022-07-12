"""Helps the sms sending module to check if the device is ready and sends
messages."""
import os
import re


def found(text, substring):
    """test if substring exists in string.

    :param text:
    :param substring:
    """
    if text.find(substring) != -1:
        return True
    return False


# execute cmd and return response
def cmd_res(cmd):
    """Executes command and returns.

    :param cmd:
    """

    a = os.popen(cmd).read()  # nosec
    return a


# check if device connected
def device_ready():
    """Checks with adb through USB whether your device is connected."""
    a = cmd_res("adb devices").count("device")
    if a == 2:
        return True
    return False


# check android version
def get_android_version() -> int:
    """Checks with your phone what the android version is and returns an
    integer of that version."""
    version_response = cmd_res("adb shell getprop ro.build.version.release")
    print(f"version_response={version_response}")
    if found(version_response, "8."):

        return 8  # Oreo
    if found(version_response, "7."):
        return 7  # Nougat
    if found(version_response, "6."):

        return 6  # Marshmallow"
    if found(version_response, "5."):

        return 5  # Lollipop"
    if found(version_response, "10"):
        return 10
    raise Exception(
        "your device isn't compatible. Your device must be Android 5+"
    )


def get_sms_command(nr_receipient: str, sms: str, android_version: int):
    """Creates the correct sms command based on the android version.

    :param nr_receipient: str:
    :param sms: str:
    :param get_android_version(): int:
    """
    p0 = "adb shell service call isms "
    if android_version in [5]:
        p1 = """9 s16 "com.android.mms" s16 "."""
    elif android_version in [6, 7]:
        p1 = """7 i32 1 s16 "com.android.mms" s16 "."""
    elif android_version in [8, 10]:
        p1 = '7 i32 0 s16 "com.android.mms.service" s16 "'
    else:
        raise Exception(
            "Android version not supported, please add support at:"
            + "https://www.github.com/a-t-0/Event-Communication"
        )
    command = (
        p0
        + p1
        + nr_receipient
        + '" s16 "null" s16 "'
        + sms
        + '" s16 "null" s16 "null 7"'
    )
    return command


def send_sms(nr_receipient, formatted_sms, sms_command):
    """Sends an sms message and verifies the output indicates sending was
    successful.

    :param nr_receipient:
    :param formatted_sms:
    :param sms_command:
    """
    send_output = cmd_res(sms_command)
    if send_output != " Parcel(00000000    '....')":
        raise Exception(
            f"Error sending the message to:{nr_receipient}"
            f"SMS content:{formatted_sms}"
            f"The output was:{send_output}"
        )


# Replace space with "\ "
def formatSMS(SMS):
    """Formats the sms message to a valid format.

    :param SMS:
    """
    newSMS = re.escape(SMS.replace("\n", " "))
    return newSMS
