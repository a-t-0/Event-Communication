"""Sends an sms to a recipient."""
from src.sender.helper_sms import (
    device_ready,
    formatSMS,
    get_android_version,
    get_sms_command,
    send_sms,
)


def send_sms_to_nr(sms_text, nr_receipient):
    """Sends an sms to a number."""
    if device_ready():
        if len(nr_receipient) <= 2:
            raise Exception(
                f"\n[Error] : Your nr_receipient is not valid:{nr_receipient}"
            )
        formatted_sms = formatSMS(sms_text)
        if formatted_sms == "":
            raise Exception(
                "Error, your sms message does not contain any text."
            )

        sms_command = get_sms_command(
            nr_receipient, formatted_sms, get_android_version()()
        )
        send_sms(nr_receipient, formatted_sms, sms_command)

    else:
        print(
            "Error, please connect phone to USB,"
            + "check if you have ADB Installed on this device, and "
            + "verify you have enabled Android Debugging Mode on your phone"
        )
