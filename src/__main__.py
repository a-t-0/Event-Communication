"""Entry point of code, run it with: python -m src from the root directory of
this repository.

Checks if private data structures exist, and if not, creates a template
private data structure that you can adjust.
"""

from installation.load_private_data import ensure_private_data_templates_exist

private_dir = "private_data"
ensure_private_data_templates_exist(private_dir)
