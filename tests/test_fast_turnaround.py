import unittest

from copy import deepcopy
from sorting_hat import _gateway, build_spec, _finalize_tool_spec, FAST_TURNAROUND, TOOL_DESTINATIONS, SPECIFICATIONS


class TestFastTurnaround(unittest.TestCase):
    def setUp(self):
        self.ft = deepcopy(FAST_TURNAROUND)
        self.td = deepcopy(TOOL_DESTINATIONS)
        self.sp = deepcopy(SPECIFICATIONS)

        _tool_label = '_unittest_tool'
        _dest_label = 'condor_unittest_destination'

        _tool_spec = {
            _tool_label: {
                'runner': _dest_label
            }
        }
        _dest_spec = {
            _dest_label: {
                'env': {},
                'params': {
                    'requirements': 'GalaxyGroup == "to_be_updated"'
                }
            }
        }

        self.td[_tool_label] = _tool_spec[_tool_label]
        self.sp[_dest_label] = _dest_spec[_dest_label]
        self.tool_id = _tool_label

    def test_ft_enabled_requirements(self):
        """
        Check if enabling FastTurnaround, requirements are properly updated
        """
        self.ft['enabled'] = True
        self.ft['mode'] = 'all_jobs'

        result = {'requirements': self.ft.get('requirements')}

        _, params, _, _, _ = _gateway(self.tool_id, '', '', '', '', ft=self.ft)

        self.assertEqual(params['requirements'], result['requirements'])

    def test_ft_disabled_requirements(self):
        """
        Check if disabling FastTurnaround, requirements are not updated
        """
        self.ft['enabled'] = False
        self.ft['mode'] = 'all_jobs'

        tool_spec = _finalize_tool_spec(self.tool_id, self.td, [])
        _, params_b, _, _ = build_spec(tool_spec, dest_spec=self.sp)
        _, params_g, _, _, _ = _gateway(self.tool_id, '', '', '', '', ft=self.ft, dest_spec=self.sp, tools_spec=self.td)

        self.assertEqual(params_b['requirements'], params_g['requirements'])
