import unittest

from sorting_hat import _get_limits, _finalize_tool_spec, build_spec, SPECIFICATIONS, TOOL_DESTINATIONS


class TestGetLimits(unittest.TestCase):

    def test_defaults(self):
        """
        Test that it pass default values if no specifications
        """
        _dest_label = '_unittest_destination'
        _dest_spec = {_dest_label: {}}
        SPECIFICATIONS[_dest_label] = _dest_spec[_dest_label]

        result = {'cores': 1, 'mem': 4, 'gpus': 0}
        destination = _dest_label

        limits = _get_limits(destination, dest_spec=SPECIFICATIONS)

        self.assertIsInstance(limits['cores'], int)
        self.assertIsInstance(limits['mem'], int)
        self.assertIsInstance(limits['gpus'], int)
        self.assertEqual(limits, result)

    def test_get_values_from_destination(self):
        """
        Check that it updates the default values with the destination ones
        """
        _dest_label = '_unittest_destination'
        _dest_spec = {_dest_label:
            {
                'limits':
                    {
                        'cores': 40,
                        'mem': 1000
                    }
            }
        }
        SPECIFICATIONS[_dest_label] = _dest_spec[_dest_label]

        result = {'cores': 40, 'mem': 1000, 'gpus': 0}
        destination = _dest_label

        limits = _get_limits(destination, dest_spec=SPECIFICATIONS)

        self.assertIsInstance(limits['cores'], int)
        self.assertIsInstance(limits['mem'], int)
        self.assertIsInstance(limits['gpus'], int)
        self.assertEqual(limits, result)

    def test_get_values_from_destination2(self):
        """
        Check that it updates the default values with the destination ones
        """
        _dest_label = '_unittest_destination'
        _dest_spec = {_dest_label:
            {
                'limits':
                    {
                        'gpus': 10
                    }
            }
        }
        SPECIFICATIONS[_dest_label] = _dest_spec[_dest_label]

        result = {'cores': 1, 'mem': 4, 'gpus': 10}
        destination = _dest_label

        limits = _get_limits(destination, dest_spec=SPECIFICATIONS)

        self.assertIsInstance(limits['cores'], int)
        self.assertIsInstance(limits['mem'], int)
        self.assertIsInstance(limits['gpus'], int)
        self.assertEqual(limits, result)


class TestLimits(unittest.TestCase):

    def test_boundaries(self):
        """
        Test that it pass boundary values if ones from the destination are too high
        """
        _tool_label = '_unittest_tool'
        _dest_label = '_unittest_destination'

        _tool_spec = {_tool_label:
            {
                'runner': _dest_label,
                'cores': 100,
                'mem': 2000,
                'gpus': 100
            }
        }
        _dest_spec = {_dest_label:
            {
                'limits':
                    {
                        'cores': 10,
                        'mem': 10
                    },
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

        result = {'request_cpus': '10', 'request_memory': '10G'}
        tool_id = '_unittest_tool'

        tool_spec = _finalize_tool_spec(tool_id, '', tools_spec=TOOL_DESTINATIONS)
        env, params, runner, _, tags = build_spec(tool_spec, dest_spec=SPECIFICATIONS)

        for k, v in result.items():
            self.assertIn(k, params)
            self.assertEqual(params[k], result[k])

    def test_boundaries2(self):
        """
        Test that it pass boundary values if ones from the destination are too high
        Add gpus
        """
        _tool_label = '_unittest_tool'
        _dest_label = '_unittest_destination'

        _tool_spec = {_tool_label:
            {
                'runner': _dest_label,
                'cores': 100,
                'mem': 2000,
                'gpus': 100
            }
        }
        _dest_label = '_unittest_destination'
        _dest_spec = {_dest_label:
            {
                'limits':
                    {
                        'cores': 10,
                        'mem': 10,
                        'gpus': 10
                    },
                'env': {},
                'params':
                    {
                        'request_cpus': '{PARALLELISATION}',
                        'request_memory': '{MEMORY}',
                        'request_gpus': '{GPUS}'
                    }
            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]
        SPECIFICATIONS[_dest_label] = _dest_spec[_dest_label]

        result = {'request_cpus': '10', 'request_memory': '10G', 'request_gpus': '10'}
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, '', tools_spec=TOOL_DESTINATIONS)
        env, params, runner, _, tags = build_spec(tool_spec, dest_spec=SPECIFICATIONS)

        for k, v in result.items():
            self.assertIn(k, params)
            self.assertEqual(params[k], result[k])


if __name__ == '__main__':
    unittest.main()
