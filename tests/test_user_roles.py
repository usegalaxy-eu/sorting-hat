import unittest

from sorting_hat import _gateway, build_spec, _finalize_tool_spec, SPECIFICATIONS, TOOL_DESTINATIONS


class TestPulsarDestinationHint(unittest.TestCase):

    def test_destination_in_user_role(self):
        """
        Test if the runner hint works without runner in tool_spec
        """
        _tool_label = '_unittest_tool'
        _user_roles = ['destination-pulsar-de01']

        _tool_spec = {_tool_label:
            {

            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]

        result = _user_roles[0].replace('destination-pulsar-', 'pulsar_eu_')
        tool_id = _tool_label

        env, params, runner, tool_spec, tags = _gateway(tool_id, _user_roles, '', '')
        self.assertEqual(runner, result)

    def test_destination_in_user_rolewith_tool_runner(self):
        """
        Test if the runner hint works with runner in tool_spec
        """
        _tool_label = '_unittest_tool'
        _dest_label = '_unittest_destination'
        _user_roles = ['destination-pulsar-de01']

        _tool_spec = {_tool_label:
            {
                'runner': _dest_label
            }
        }

        _dest_spec = {_dest_label:
            {
                'env': {},
                'params': {}
            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]
        SPECIFICATIONS[_dest_label] = _dest_spec[_dest_label]

        result = _user_roles[0].replace('destination-pulsar-', 'pulsar_eu_')
        tool_id = _tool_label

        env, params, runner, tool_spec, tags = _gateway(tool_id, _user_roles, '', '')
        self.assertEqual(runner, result)
