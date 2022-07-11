"""Verifies The Supported_experiment_settings object catches invalid adaptation
specifications."""
# pylint: disable=R0801
import unittest

from src.helper import parse_string


class Test_helper(unittest.TestCase):
    """Tests whether the get_networkx_graph_of_2_neurons of the get_graph file
    returns a graph with 2 nodes."""

    # Initialize test object
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_invalid_input_type_is_detected(self):
        """Verifies an error is thrown if configuration settings object is of
        type None."""

        with self.assertRaises(Exception) as context:
            parse_string(5)
            self.assertEqual(
                f"Error, string type was:{type(int)} "
                + "whereas it should be of type string.",
                str(context.exception),
            )

    def test_valid_input_type_yields_valid_return_file(self):
        """Verifies an a string is returned, if a string is put in."""

        self.assertEqual(parse_string("hi"), "hi")
