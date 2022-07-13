"""Ensures a repository with private data is created."""

# Check if a private data folder exists. If not, create it.
# TODO: verify the private data does not get synced to this public repo.
# TODO: allow the private data folder to be synced to a private repo.

# Private data folder structure:

import os


def ensure_private_data_folders_are_created():
    """Checks if the private data folders are created.

    Checks if they exist and creates them if they did not yet exist.
    """
    private_dir = "private_data"
    private_subdirs = ["communications", "contact_info", "events"]
    thedirs = list(map(lambda x: f"{private_dir}/{x}", private_subdirs))
    for some_dir in thedirs.append(private_dir):
        if not os.path.exists(some_dir):
            create_dir_if_not_exists(some_dir)


def create_dir_if_not_exists(dir_name):
    """Creates a directory if it does not exist.

    :param root_dir_name:
    :param dir_name:
    """
    if not os.path.exists(dir_name):
        os.makedirs(f"{dir_name}")
    if not os.path.exists(dir_name):
        raise Exception(f"Error, dir_name={dir_name} did not exist.")
