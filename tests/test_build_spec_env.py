import unittest

from sorting_hat import build_spec, _finalize_tool_spec, SPECIFICATIONS, TOOL_DESTINATIONS


class TestBuildSpecEnv(unittest.TestCase):

    def test_pass_two_env(self):
        """
        Test that it pass two env variables correctly with undefined runner
        """
        _tool_label = '_unittest_tool'

        _tool_spec = {_tool_label:
            {
                'env': {
                    'name1': 'value1',
                    'name2': "value2"
                }
            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]

        result = [{'name': 'name1', 'value': 'value1'}, {'name': 'name2', 'value': 'value2'}]
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, '', tools_spec=TOOL_DESTINATIONS)
        env, params, runner, tags = build_spec(tool_spec, dest_spec=SPECIFICATIONS)

        d1 = {n['name']: n['value'] for n in env if n in ['name1', 'name2']}
        d2 = {n['name']: n['value'] for n in result}

        for k, v in d1.items():
            self.assertEqual(d1[k], d2[k])

    def test_pass_two_env_plus_runner(self):
        """
        Test that it pass two env variables correctly with defined runner
        """
        _tool_label = '_unittest_tool'
        _dest_label = '_unittest_destination'

        _tool_spec = {_tool_label:
            {
                'runner': _dest_label,
                'env': {
                    'name1': 'value1',
                    'name2': "value2"
                }
            }
        }
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

        result = [{'name': 'name1', 'value': 'value1'}, {'name': 'name2', 'value': 'value2'}]
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, '', tools_spec=TOOL_DESTINATIONS)
        env, params, runner, tags = build_spec(tool_spec, dest_spec=SPECIFICATIONS)

        d1 = {n['name']: n['value'] for n in env}
        d2 = {n['name']: n['value'] for n in result}
        for k, v in d1.items():
            self.assertEqual(d1[k], d2[k])

    def test_pass_two_env_plus_one_identical_from_runner(self):
        """
        Runner has defined the same env variable as tool, but the tool's one has a higher priority
        """
        _tool_label = '_unittest_tool'
        _dest_label = '_unittest_destination'

        _tool_spec = {_tool_label:
            {
                'runner': _dest_label,
                'env': {
                    'name1': 'value1',
                    'name2': "value2"
                }
            }
        }
        _dest_spec = {_dest_label:
            {
                'env': {
                    'name2': "value3"
                },
                'params':
                    {
                        'request_cpus': '{PARALLELISATION}',
                        'request_memory': '{MEMORY}'
                    }
            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]
        SPECIFICATIONS[_dest_label] = _dest_spec[_dest_label]

        result = [{'name': 'name2', 'value': 'value2'}, {'name': 'name1', 'value': 'value1'}]
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, '', tools_spec=TOOL_DESTINATIONS)
        env, params, runner, tags = build_spec(tool_spec, dest_spec=SPECIFICATIONS)

        d1 = {n['name']: n['value'] for n in env}
        d2 = {n['name']: n['value'] for n in result}
        for k, v in d1.items():
            self.assertEqual(d1[k], d2[k])

    def test_pass_three_env(self):
        """
        Test that it pass three env variables correctly.
        Two from the destination and one from the runner, all different.
        """
        _tool_label = '_unittest_tool'
        _dest_label = '_unittest_destination'

        _tool_spec = {_tool_label:
            {
                'runner': _dest_label,
                'env': {
                    'name1': 'value1',
                    'name2': "value2"
                }
            }
        }
        _dest_spec = {_dest_label:
            {
                'env': {
                    'name3': "value3"
                },
                'params':
                    {
                        'request_cpus': '{PARALLELISATION}',
                        'request_memory': '{MEMORY}'
                    }
            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]
        SPECIFICATIONS[_dest_label] = _dest_spec[_dest_label]

        result = [{'name': 'name3', 'value': 'value3'}, {'name': 'name1', 'value': 'value1'}, {'name': 'name2', 'value': 'value2'}]
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, '', tools_spec=TOOL_DESTINATIONS)
        env, params, runner, tags = build_spec(tool_spec, dest_spec=SPECIFICATIONS)

        self.assertEqual(len(env), len(result))
        d1 = {n['name']: n['value'] for n in env}
        d2 = {n['name']: n['value'] for n in result}
        for k, v in d1.items():
            self.assertEqual(d1[k], d2[k])


if __name__ == '__main__':
    unittest.main()
