import unittest

from sorting_hat import _finalize_tool_spec, TOOL_DESTINATIONS, DEFAULT_TOOL_SPEC


class TestToolSpec(unittest.TestCase):

    def test_default_values_setup(self):
        """
        Test if default values will be assigned in case of a tool without specifications
        :return:
        """
        _tool_label = '_unittest_tool'
        _tool_spec = {_tool_label: {}}

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]

        result = {
            'cores': DEFAULT_TOOL_SPEC['cores'],
            'mem': DEFAULT_TOOL_SPEC['mem'],
            'gpus': DEFAULT_TOOL_SPEC['gpus'],
            'force_destination_id': DEFAULT_TOOL_SPEC['force_destination_id'],
            'runner': DEFAULT_TOOL_SPEC['runner']
        }
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, '', tools_spec=TOOL_DESTINATIONS)

        for i in result:
            self.assertEqual(tool_spec[i], result[i],
                             msg="for {}, actual {} value ({}) is different form expected result ({}) ".format(tool_id,
                                                                                                    i,
                                                                                                    tool_spec[i],
                                                                                                    result[i]))
