"""Parses CLI arguments that specify on which platform to simulate the spiking
neural network (SNN)."""
import argparse


def parse_cli_args() -> argparse.Namespace:
    """Reads command line arguments and converts them into python arguments."""
    # Instantiate the parser
    parser = argparse.ArgumentParser(
        description="Optional description for arg" + " parser"
    )

    # Include argument parsing for default code.
    # Allow user to load a graph from file.
    parser.add_argument(
        "--signal-cli",
        dest="install_signal_cli",
        action="store_true",
        help="boolean flag, determines whether signal-cli is installed.",
    )

    parser.add_argument(
        "--sms-cli",
        dest="install_sms_cli",
        action="store_true",
        help="boolean flag, determines whether sms-cli is installed.",
    )

    parser.add_argument(
        "--get-vcfs",
        dest="get_vcf_contacts",
        action="store_true",
        help="boolean flag, determines whether vcf contacts are loaded to "
        + " person objects",
    )

    parser.add_argument(
        "--create-vcf",
        dest="create_vcf_file_sample",
        action="store_true",
        help="boolean flag, determines whether two .vcf files are created.",
    )

    # TODO:
    parser.add_argument(
        "--load-vcf-file",
        dest="load_vcf_file_sample",
        action="store_true",
        help="boolean flag, determines whether two .vcf files are created.",
    )

    # Load the arguments that are given.
    args = parser.parse_args()
    return args
