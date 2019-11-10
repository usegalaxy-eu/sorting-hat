import unittest

from sorting_hat import _finalize_tool_spec, name_it, DEFAULT_DESTINATION, SPECIFICATIONS, SPECIFICATION_PATH, TOOL_DESTINATIONS


class TestDestinations(unittest.TestCase):

    def test_default_destination(self):
        """
        Test DEFAULT_DESTINATION exists in SPECIFICATIONS
        """
        self.assertTrue(DEFAULT_DESTINATION in SPECIFICATIONS,
                        msg="{} not in {}".format(DEFAULT_DESTINATION, SPECIFICATION_PATH))

    def test_force_destination_id_true(self):
        """
        Test that it use the id from destination_id
        """
        _tool_label = '_unittest_tool'

        _tool_spec = {_tool_label:
            {
                'force_destination_id': True
            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]

        result = 'so_' + DEFAULT_DESTINATION
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, '', tools_spec=TOOL_DESTINATIONS)
        name = name_it(tool_spec)

        self.assertEqual(name, result)

    def test_force_destination_id_true_with_runner(self):
        """
        Test that it use the id from destination_id
        """
        _tool_label = '_unittest_tool'
        _dest_label = '_unittest_destination'

        _tool_spec = {_tool_label:
            {
                'force_destination_id': True,
                'runner': _dest_label
            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]

        result = 'so_' + _dest_label
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, '', tools_spec=TOOL_DESTINATIONS)
        name = name_it(tool_spec)

        self.assertEqual(name, result)

    def test_force_destination_id_false(self):
        """
        Test that it use the id from destination_id
        """
        _tool_label = '_unittest_tool'

        _tool_spec = {_tool_label:
            {
                'force_destination_id': False
            }

        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]

        result = '1cores_4.0G'
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, '', tools_spec=TOOL_DESTINATIONS)
        name = name_it(tool_spec)

        self.assertEqual(name, result)

    def test_force_destination_id_false_with_runner(self):
        """
        Test that it use the id from destination_id
        """
        _tool_label = '_unittest_tool'
        _dest_label = '_unittest_destination'

        _tool_spec = {_tool_label:
            {
                'force_destination_id': False,
                'runner': _dest_label
            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]

        result = '1cores_4.0G'
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, '', tools_spec=TOOL_DESTINATIONS)
        name = name_it(tool_spec)

        self.assertEqual(name, result)


if __name__ == '__main__':
    unittest.main()
