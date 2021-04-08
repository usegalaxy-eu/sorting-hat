import unittest

from copy import deepcopy
from sorting_hat import _gateway, TOOL_DESTINATIONS, SPECIFICATIONS, DEFAULT_DESTINATION, \
    SPECIAL_TOOLS


class TestRunnerHint(unittest.TestCase):
    def setUp(self):
        self.td = deepcopy(TOOL_DESTINATIONS)
        self.sp = deepcopy(SPECIFICATIONS)

        d_labels = ['condor_unittest_destination', 'remote_cluster_mq_ut01']
        for d in d_labels:
            _dest_label = d
            _dest_spec = {
                _dest_label: {
                    'limits': {},
                    'env': {},
                    'params': {}
                }
            }
            self.sp[_dest_label] = _dest_spec[_dest_label]

    def test_runner_hint(self):
        """
        A destination can be forced through the the user's preferences.
        Check if the _gateway function, fed with a proper user_roles dict, return the runner associated
        remote_cluster_mq_* > pulsar_eu_*
        condor_* > condor
        If None, return the expected runner from the tool's specification
        """
        up_labels = ['remote_cluster_mq_ut01', 'condor_unittest_destination', 'None']
        results = {
            up_labels[0]: 'pulsar_eu_ut01',
            up_labels[1]: 'condor',
            'condor': 'condor'
        }
        t_runner_labels = [DEFAULT_DESTINATION, 'condor_unittest_destination', 'remote_cluster_mq_ut01']
        for u in up_labels:
            for r in t_runner_labels:
                _tool_label = '_unittest_tool'
                _tool_spec = {
                    _tool_label: {
                        'runner': r
                    }
                }
                self.td[_tool_label] = _tool_spec[_tool_label]
                tool_id = _tool_label

                _user_preferences = {
                    'distributed_compute|remote_resources|unittest_remote_resource': u
                }

                _, _, runner, _, _ = _gateway(tool_id, _user_preferences, '', '', '', tools_spec=self.td, dest_spec=self.sp)

                if u == 'None':
                    self.assertEqual(runner, results[r])
                else:
                    self.assertEqual(runner, results[u])

    def test_skip_runner_hint(self):
        """
        Check if tools associated with the "skip_runner_hint" label are really skipped
        DEFAULT_DESTINATION is assumed to be the proper runner for these tools
        """
        up_labels = ['remote_cluster_mq_ut01', 'condor_unittest_destination', 'None']
        tools_to_skip = [k for k, v in SPECIAL_TOOLS.items() if v == 'skip_runner_hint']
        for t in tools_to_skip:
            for u in up_labels:
                _user_preferences = {
                    'distributed_compute|remote_resources|unittest_remote_resource': u
                }
                tool_id = t
                _, _, runner, _, _ = _gateway(tool_id, _user_preferences, '', '', '', dest_spec=self.sp)

                self.assertEqual(runner, DEFAULT_DESTINATION)
