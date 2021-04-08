import unittest

from copy import deepcopy
from sorting_hat import build_spec, _finalize_tool_spec, DEFAULT_DESTINATION, SPECIFICATIONS, TOOL_DESTINATIONS


class TestBuildSpecRunner(unittest.TestCase):
    def setUp(self):
        self.td = deepcopy(TOOL_DESTINATIONS)
        self.sp = deepcopy(SPECIFICATIONS)

    def test_runner_undefined(self):
        """
        Test no runner specification, should reply with the DEFAULT_DESTINATION
        """
        _tool_label = '_unittest_tool'
        _dest_label = 'condor_unittest_destination'

        _tool_spec = {
            _tool_label: {}
        }
        _dest_spec = {
            _dest_label: {
                'env': {},
                'params': {
                    'request_cpus': '{PARALLELISATION}',
                    'request_memory': '{MEMORY}'
                }
            }
        }

        self.td[_tool_label] = _tool_spec[_tool_label]
        self.sp[_dest_label] = _dest_spec[_dest_label]

        result = DEFAULT_DESTINATION
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, self.td, [])
        _, _, runner, _ = build_spec(tool_spec, dest_spec=self.sp)

        self.assertEqual(runner, result)

    def test_runner_pulsar(self):
        """
        Test Pulsar destination
        """
        _tool_label = '_unittest_tool'
        _dest_label = 'remote_cluster_mq_unittest_destination'

        _tool_spec = {
            _tool_label: {
                'runner': _dest_label
            }
        }
        _dest_spec = {
            _dest_label: {
                'env': {},
                'params': {
                    'submit_request_cpus': '{PARALLELISATION}',
                    'request_memory': '{MEMORY}',
                    'request_gpus': '{GPUS}'
                }
            }
        }

        self.td[_tool_label] = _tool_spec[_tool_label]
        self.sp[_dest_label] = _dest_spec[_dest_label]

        result = 'pulsar_eu_destination'
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, self.td, [])
        _, _, runner, _ = build_spec(tool_spec, dest_spec=self.sp)

        self.assertEqual(runner, result)

    def test_runner_unknown(self):
        """
        Test unknown runner value, should reply with the DEFAULT_DESTINATION
        """
        _tool_label = '_unittest_tool'
        _tool_spec = {
            _tool_label: {
                'runner': 'unknown'
            }
        }

        self.td[_tool_label] = _tool_spec[_tool_label]

        result = DEFAULT_DESTINATION
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, self.td, [])
        _, _, runner, _ = build_spec(tool_spec, dest_spec=self.sp)

        self.assertEqual(runner, result)

    def test_runner_from_joint_destination(self):
        """
        Test runner retrieved from joint destinations
        """
        _tool_label = '_unittest_tool'
        _dest_label = 'remote_condor_cluster_gpu_docker'

        _tool_spec = {
            _tool_label: {
                'runner': _dest_label
            }
        }
        _dest_spec = {
            _dest_label: {
                'env': {},
                'params': {
                    'submit_request_cpus': '{PARALLELISATION}',
                    'request_memory': '{MEMORY}',
                    'request_gpus': '{GPUS}'
                }
            }
        }

        self.td[_tool_label] = _tool_spec[_tool_label]

        result = ['pulsar_eu_de03', 'pulsar_eu_uk01']
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, self.td, [])
        _, _, runner, _ = build_spec(tool_spec, dest_spec=self.sp)

        self.assertIn(runner, result)


if __name__ == '__main__':
    unittest.main()
