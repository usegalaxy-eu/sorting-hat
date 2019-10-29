import unittest

from sorting_hat import _gateway, _finalize_tool_spec, build_spec, SPECIFICATIONS, TOOL_DESTINATIONS


class TestGalaxyVars(unittest.TestCase):

    def test_galaxy_slots(self):
        """
        Test that it pass cores value to GALAXY_SLOTS env vars
        """
        _tool_label = '_unittest_tool'
        _dest_label = '_unittest_destination'

        _tool_spec = {_tool_label:
            {
                'runner': _dest_label,
                'cores': 4
            }
        }
        _dest_spec = {_dest_label:
            {
                'limits':
                    {
                        'cores': 8
                    },
                'env':
                    {
                        'GALAXY_SLOTS': '{PARALLELISATION}'
                    },
                'params': {}
            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]
        SPECIFICATIONS[_dest_label] = _dest_spec[_dest_label]

        result = {'env': [{'name': 'GALAXY_SLOTS', 'value': _tool_spec[_tool_label]['cores']}]}
        tool_id = '_unittest_tool'

        env, params, runner, tool_spec = _gateway(tool_id, '', '', '')

        d1 = {n['name']: n['value'] for n in env}
        d2 = {n['name']: n['value'] for n in result['env']}
        for k, v in d1.items():
            self.assertEqual(d1[k], d2[k]) if k == 'name' else self.assertEqual(int(d1[k]), d2[k])

    def test_galaxy_slots_upper_boundary(self):
        """
        Test that it pass boundary value if one from the tool is too high
        """
        _tool_label = '_unittest_tool'
        _dest_label = '_unittest_destination'

        _tool_spec = {_tool_label:
            {
                'runner': _dest_label,
                'cores': 40
            }
        }
        _dest_spec = {_dest_label:
            {
                'limits':
                    {
                        'cores': 8
                    },
                'env':
                    {
                        'GALAXY_SLOTS': '{PARALLELISATION}'
                    },
                'params': {}
            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]
        SPECIFICATIONS[_dest_label] = _dest_spec[_dest_label]

        result = {'env': [{'name': 'GALAXY_SLOTS', 'value': _dest_spec[_dest_label]['limits']['cores']}]}
        tool_id = '_unittest_tool'

        env, params, runner, tool_spec = _gateway(tool_id, '', '', '')

        d1 = {n['name']: n['value'] for n in env}
        d2 = {n['name']: n['value'] for n in result['env']}
        for k, v in d1.items():
            self.assertEqual(d1[k], d2[k]) if k == 'name' else self.assertEqual(int(d1[k]), d2[k])

    def test_galaxy_memory_mb(self):
        """
        Test that it pass cores value to GALAXY_MEMORY_MB env vars
        """
        _tool_label = '_unittest_tool'
        _dest_label = '_unittest_destination'

        _tool_spec = {_tool_label:
            {
                'runner': _dest_label,
                'mem': 0.3
            }
        }
        _dest_spec = {_dest_label:
            {
                'limits':
                    {
                        'mem': 8
                    },
                'env':
                    {
                        'GALAXY_MEMORY_MB': '{MEMORY_MB}'
                    },
                'params': {}
            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]
        SPECIFICATIONS[_dest_label] = _dest_spec[_dest_label]

        result = {'env': [{'name': 'GALAXY_MEMORY_MB', 'value': int(_tool_spec[_tool_label]['mem'] * 1024)}]}
        tool_id = '_unittest_tool'

        env, params, runner, tool_spec = _gateway(tool_id, '', '', '')

        d1 = {n['name']: n['value'] for n in env}
        d2 = {n['name']: n['value'] for n in result['env']}
        for k, v in d1.items():
            self.assertEqual(d1[k], d2[k]) if k == 'name' else self.assertEqual(int(d1[k]), d2[k])

    def test_galaxy_memory_mb_upper_boundary(self):
        """
        Test that it pass boundary value if one from the tool is too high
        """
        _tool_label = '_unittest_tool'
        _dest_label = '_unittest_destination'

        _tool_spec = {_tool_label:
            {
                'runner': _dest_label,
                'mem': 30
            }
        }
        _dest_spec = {_dest_label:
            {
                'limits':
                    {
                        'mem': 8
                    },
                'env':
                    {
                        'GALAXY_MEMORY_MB': '{MEMORY_MB}'
                    },
                'params': {}
            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]
        SPECIFICATIONS[_dest_label] = _dest_spec[_dest_label]

        result = {'env': [{'name': 'GALAXY_MEMORY_MB', 'value': _dest_spec[_dest_label]['limits']['mem'] * 1024}]}
        tool_id = '_unittest_tool'

        env, params, runner, tool_spec = _gateway(tool_id, '', '', '')

        d1 = {n['name']: n['value'] for n in env}
        d2 = {n['name']: n['value'] for n in result['env']}
        for k, v in d1.items():
            self.assertEqual(d1[k], d2[k]) if k == 'name' else self.assertEqual(int(d1[k]), d2[k])


if __name__ == '__main__':
    unittest.main()
