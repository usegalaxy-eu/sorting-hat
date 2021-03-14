import unittest

from copy import deepcopy
from sorting_hat import _finalize_tool_spec, TOOL_DESTINATIONS, DEFAULT_TOOL_SPEC


class TestToolSpec(unittest.TestCase):
    def setUp(self):
        self.td = deepcopy(TOOL_DESTINATIONS)

    def test_default_values_setup(self):
        """
        Test if default values will be assigned in case of a tool without specifications
        :return:
        """
        _tool_label = '_unittest_tool'
        _tool_spec = {_tool_label: {}}

        self.td[_tool_label] = _tool_spec[_tool_label]

        result = {
            'cores': DEFAULT_TOOL_SPEC['cores'],
            'mem': DEFAULT_TOOL_SPEC['mem'],
            'gpus': DEFAULT_TOOL_SPEC['gpus'],
            'force_destination_id': DEFAULT_TOOL_SPEC['force_destination_id'],
            'runner': DEFAULT_TOOL_SPEC['runner']
        }
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, self.td, '')

        for i in result:
            if i in ['cores', 'gpus']:
                self.assertIsInstance(tool_spec[i], int)
            elif i == 'mem':
                self.assertIsInstance(tool_spec[i], float)
            elif i == 'force_destination_id':
                self.assertIsInstance(tool_spec[i], bool)
            elif i == 'runner':
                self.assertIsInstance(tool_spec[i], str)
            self.assertEqual(tool_spec[i], result[i],
                             msg="for {}, actual {} value ({}) is different form expected "
                                 "result ({}) ".format(tool_id, i, tool_spec[i], result[i]))

    def test_default_keys(self):
        """
        Test default keys from TOOL_DESTINATIONS
        """
        for tool_id in TOOL_DESTINATIONS:
            result = TOOL_DESTINATIONS[tool_id]

            tool_spec = _finalize_tool_spec(tool_id, TOOL_DESTINATIONS, [])

            for i in result:
                if i in ['cores', 'gpus']:
                    self.assertIsInstance(tool_spec[i], int)
                elif i == 'mem':
                    self.assertIsInstance(tool_spec[i], float)
                elif i == 'force_destination_id':
                    self.assertIsInstance(tool_spec[i], bool)
                elif i == 'runner':
                    self.assertIsInstance(tool_spec[i], str)
                self.assertEqual(tool_spec[i], result[i],
                                 msg="for {}, actual {} value ({}) is different form expected "
                                     "result ({}) ".format(tool_id, i, tool_spec[i], result[i]))
