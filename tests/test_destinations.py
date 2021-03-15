import unittest

from copy import deepcopy
from sorting_hat import _finalize_tool_spec, name_it, DEFAULT_DESTINATION, \
    SPECIFICATIONS, SPECIFICATION_PATH, TOOL_DESTINATIONS, FDID_PREFIX


class TestDestinations(unittest.TestCase):
    def setUp(self):
        self.td = deepcopy(TOOL_DESTINATIONS)

    def test_default_destination(self):
        """
        Check DEFAULT_DESTINATION is not an empty string
        """
        self.assertTrue(len(DEFAULT_DESTINATION),
                        msg="Default destination is empty".format())

    def test_default_destination_in_specification(self):
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

        self.td[_tool_label] = _tool_spec[_tool_label]

        result = FDID_PREFIX + DEFAULT_DESTINATION
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, self.td, [])
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

        self.td[_tool_label] = _tool_spec[_tool_label]

        result = FDID_PREFIX + _dest_label
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, self.td, [])
        name = name_it(tool_spec)

        self.assertEqual(name, result)

    def test_force_destination_id_false(self):
        """
        Test
        """
        _tool_label = '_unittest_tool'

        _tool_spec = {_tool_label:
            {
                'force_destination_id': False
            }

        }

        self.td[_tool_label] = _tool_spec[_tool_label]

        result = '1cores_4.0G'
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, self.td, [])
        name = name_it(tool_spec)

        self.assertEqual(name, result)

    def test_force_destination_id_default(self):
        """
        Test
        """
        _tool_label = '_unittest_tool'

        _tool_spec = {_tool_label: {}
                      }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]

        result = '1cores_4.0G'
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, self.td, [])
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

        self.td[_tool_label] = _tool_spec[_tool_label]

        result = '1cores_4.0G'
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, self.td, [])
        name = name_it(tool_spec)

        self.assertEqual(name, result)

    def test_condor_destination_has_default_requirements(self):
        """
        Usegalaxy.eu condor destinations need to have a specific requirements,
        unless otherwise specified.
        requirements: 'GalaxyGroup == "compute"'
        """
        for label, v in SPECIFICATIONS.items():
            if 'condor' in label:
                key = 'requirements'
                container = v.get('params')
                message = "'requirements' missing in {} destination".format(label)
                self.assertIn(key, container, message)
                self.assertEqual(v.get('params').get('requirements'), 'GalaxyGroup == "compute"')


if __name__ == '__main__':
    unittest.main()
