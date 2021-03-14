import unittest

from copy import deepcopy
from sorting_hat import _gateway, TOOL_DESTINATIONS


class TestBuildSpecRunner(unittest.TestCase):
    def setUp(self):
        self.td = deepcopy(TOOL_DESTINATIONS)

        _tool_label = '_unittest_tool'
        _tool_spec = {_tool_label: {}}

        self.td[_tool_label] = _tool_spec[_tool_label]
        self.tool_id = _tool_label

    def test_reroute(self):
        """
        Given a user's role starting with "training-" label, the function has to return two
        parameters, requirements and +Group, updated with the training label
        """
        _user_roles = ['training-unittest_training1', 'training-unittest_training2']

        result = {
                'params': {
                    'requirements': '(GalaxyGroup == "compute") || ((GalaxyGroup == "{}") || (GalaxyGroup == "{}"))'.format(_user_roles[0], _user_roles[1]),
                    '+Group': '"{}, {}"'.format(_user_roles[0], _user_roles[1]),
                    },
            }

        _, params, _, _, _ = _gateway(self.tool_id, '', _user_roles, '', '', tools_spec=self.td)

        self.assertEqual(params['requirements'], result['params']['requirements'])
        self.assertEqual(params['+Group'], result['params']['+Group'])

    def test_reroute_aliasing(self):
        """
         Some particular events can have contemporary trainings (like GCC) and we want to collect
         them under the same label (e.g. to assign the the same computing cluster)
         Given a user's roles with several training like "training-gcc-*" label,
         the gateway function has to append the "training-gcc" label to the others
        """
        _user_roles = ['training-gcc-unittest_training1', 'training-gcc-unittest_training2']

        result = {
                'params': {
                    'requirements': '(GalaxyGroup == "compute") || ((GalaxyGroup == "{}") || (GalaxyGroup == "{}") || (GalaxyGroup == "{}"))'.format(_user_roles[0], _user_roles[1], "training-gcc"),
                    '+Group': '"{}, {}, {}"'.format(_user_roles[0], _user_roles[1], "training-gcc"),
                    },
            }

        _, params, _, _, _ = _gateway(self.tool_id, '', _user_roles, '', '', tools_spec=self.td)

        self.assertEqual(params['requirements'], result['params']['requirements'])
        self.assertEqual(params['+Group'], result['params']['+Group'])
