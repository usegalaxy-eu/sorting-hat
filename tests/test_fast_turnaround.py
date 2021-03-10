import unittest
import copy

from sorting_hat import _gateway, build_spec, _finalize_tool_spec, FAST_TURNAROUND, TOOL_DESTINATIONS, SPECIFICATIONS


class TestFastTurnaround(unittest.TestCase):

    def test_ft_enabled_requirements(self):
        """
        Check if enabling FastTurnaround requirements are properly updated
        """
        _tool_label = '_unittest_tool'
        _dest_label = 'condor_unittest_destination'

        _tool_spec = {_tool_label:
                          {
                              'runner': _dest_label
                          }
        }
        _dest_spec = {_dest_label:
          {
            'env': { },
            'params':
              {
                'requirements': 'GalaxyGroup == "to_be_updated"'
              }
          }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]
        SPECIFICATIONS[_dest_label] = _dest_spec[_dest_label]
        ft = copy.deepcopy(FAST_TURNAROUND)
        ft['enabled'] = True
        ft['mode'] = 'all_jobs'

        result = {'requirements': FAST_TURNAROUND.get('requirements')}
        tool_id = _tool_label

        _, params, _, _, _ = _gateway(tool_id, '', '', '', '', ft=ft)

        self.assertEqual(params['requirements'], result['requirements'])
