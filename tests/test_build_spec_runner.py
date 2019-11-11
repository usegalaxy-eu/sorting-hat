import unittest

from sorting_hat import build_spec, _finalize_tool_spec, DEFAULT_DESTINATION, SPECIFICATIONS, TOOL_DESTINATIONS


class TestBuildSpecRunner(unittest.TestCase):

    def test_runner_undefined(self):
        """
        Test no runner specification, should reply with the DEFAULT_DESTINATION
        """
        _tool_label = '_unittest_tool'
        _dest_label = 'condor_unittest_destination'

        _tool_spec = {_tool_label: {}}
        _dest_spec = {_dest_label:
            {
                'env': {},
                'params':
                    {
                        'request_cpus': '{PARALLELISATION}',
                        'request_memory': '{MEMORY}'
                    }
            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]
        SPECIFICATIONS[_dest_label] = _dest_spec[_dest_label]

        result = DEFAULT_DESTINATION
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, '', tools_spec=TOOL_DESTINATIONS)
        env, params, runner, _, tags = build_spec(tool_spec, dest_spec=SPECIFICATIONS)

        self.assertEqual(runner, result)

    def test_runner_pulsar(self):
        """
        Test Pulsar destination
        """
        _tool_label = '_unittest_tool'
        _dest_label = 'remote_cluster_mq_unittest_destination'

        _tool_spec = {_tool_label:
            {
                'runner': _dest_label
            }
        }
        _dest_spec = {_dest_label:
            {
                'env': {},
                'params':
                    {
                        'submit_request_cpus': '{PARALLELISATION}',
                        'request_memory': '{MEMORY}',
                        'request_gpus': '{GPUS}'
                    }
            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]
        SPECIFICATIONS[_dest_label] = _dest_spec[_dest_label]

        result = 'pulsar_eu_unittest_destination'
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, '', tools_spec=TOOL_DESTINATIONS)
        env, params, runner, _, tags = build_spec(tool_spec, dest_spec=SPECIFICATIONS)

        self.assertEqual(runner, result)

    def test_runner_unknown(self):
        """
        Test unknown runner value, should reply with the DEFAULT_DESTINATION
        """
        _tool_label = '_unittest_tool'
        _tool_spec = {_tool_label:
            {
                'runner': 'unknown'
            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]

        result = DEFAULT_DESTINATION
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, '', tools_spec=TOOL_DESTINATIONS)
        env, params, runner, _, tags = build_spec(tool_spec, dest_spec=SPECIFICATIONS)

        self.assertEqual(runner, result)


if __name__ == '__main__':
    unittest.main()
