import unittest

from sorting_hat import _finalize_tool_spec, name_it, DEFAULT_DESTINATION, SPECIFICATIONS, SPECIFICATION_PATH, TOOL_DESTINATIONS


class TestDestinations(unittest.TestCase):

    def test_default_destination(self):
        """
        Test DEFAULT_DESTINATION exists in SPECIFICATIONS
        """
        self.assertTrue(DEFAULT_DESTINATION in SPECIFICATIONS,
                        msg="{} not in {}".format(DEFAULT_DESTINATION, SPECIFICATION_PATH))

    def test_force_destination_id(self):
        """
        Test that it use the id from destination_id
        """
        _tool_label = '_unittest_tool'
        _dest_label = '_unittest_destination'
        _dest_id = '_unittest_destination_id'

        _tool_spec = {_tool_label:
            {
                'destination_id': _dest_id
            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]

        result = _dest_id
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, '', tools_spec=TOOL_DESTINATIONS)
        name = name_it(tool_spec)

        self.assertEqual(name, result)


if __name__ == '__main__':
    unittest.main()
