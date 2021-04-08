import unittest

from copy import deepcopy
from sorting_hat import _gateway, DEFAULT_DESTINATION, SPECIFICATIONS, TOOL_DESTINATIONS


class TestSpecialTools(unittest.TestCase):
    def setUp(self):
        self.td = deepcopy(TOOL_DESTINATIONS)
        self.sp = deepcopy(SPECIFICATIONS)

    def test_tool_upload1(self):
        """
        Test that it pass default values if no specifications
        """
        result = {
            'env': [{'name': 'NUMBA_CACHE_DIR', 'value': '/data/2/galaxy_db/tmp'},
                    {'name': 'GALAXY_MEMORY_MB', 'value': '307'},
                    {'name': 'GALAXY_SLOTS', 'value': '1'},
                    {'name': 'TEMP', 'value': '/data/1/galaxy_db/tmp'}],
            'params': {'priority': '-128', 'request_memory': '0.3G', 'request_cpus': '1',
                       'requirements': 'GalaxyTraining == false', 'rank': 'GalaxyGroup == "upload"',
                       'tmp_dir': 'True', 'accounting_group_user': '', 'description': 'upload1'},
            'runner': DEFAULT_DESTINATION,
            'tool_spec': {'cores': 1, 'mem': 0.3, 'gpus': 0, 'runner': 'condor',
                          'env': {'TEMP': '/data/1/galaxy_db/tmp'},
                          'params': {'rank': 'GalaxyGroup == "upload"',
                                     'requirements': 'GalaxyTraining == false'
                                     },
                          }
        }
        tool_id = 'upload1'

        env, params, runner, tool_spec, tags = _gateway(tool_id, '', '', '', '')

        self.assertEqual(env, result['env'])
        self.assertEqual(params, result['params'])
        self.assertEqual(runner, result['runner'])
        self.assertEqual(tool_spec, result['tool_spec'])

    def test_tool_data_fetch_(self):
        """
        Test that it pass default values if no specifications
        """
        result = {
            'env': [{'name': 'NUMBA_CACHE_DIR', 'value': '/data/2/galaxy_db/tmp'},
                    {'name': 'GALAXY_MEMORY_MB', 'value': '307'},
                    {'name': 'GALAXY_SLOTS', 'value': '1'},
                    {'name': 'TEMP', 'value': '/data/1/galaxy_db/tmp'}],
            'params': {'priority': '-128', 'request_memory': '0.3G', 'request_cpus': '1',
                       'requirements': 'GalaxyTraining == false', 'rank': 'GalaxyGroup == "upload"',
                       'accounting_group_user': '', 'tmp_dir': 'True', 'description': '__DATA_FETCH__'},
            'runner': DEFAULT_DESTINATION,
            'tool_spec': {'cores': 1, 'mem': 0.3, 'gpus': 0, 'runner': 'condor',
                          'env': {'TEMP': '/data/1/galaxy_db/tmp'},
                          'params': {'rank': 'GalaxyGroup == "upload"',
                                     'requirements': 'GalaxyTraining == false'
                                     },
                          }
        }
        tool_id = '__DATA_FETCH__'

        env, params, runner, tool_spec, tags = _gateway(tool_id, '', '', '', '')

        self.assertEqual(env, result['env'])
        self.assertEqual(params, result['params'])
        self.assertEqual(runner, result['runner'])
        self.assertEqual(tool_spec, result['tool_spec'])

    def test_tool_set_metadata_(self):
        """
        Test that it pass default values if no specifications
        """
        result = {
            'env': [{'name': 'NUMBA_CACHE_DIR', 'value': '/data/2/galaxy_db/tmp'},
                    {'name': 'GALAXY_MEMORY_MB', 'value': '307'},
                    {'name': 'GALAXY_SLOTS', 'value': '1'}],
            'params': {'priority': '-128', 'request_cpus': '1', 'request_memory': '0.3G', 'tmp_dir': 'True',
                       'requirements': 'GalaxyTraining == false', 'rank': 'GalaxyGroup == "metadata"',
                       'accounting_group_user': '', 'description': '__SET_METADATA__'},
            'runner': DEFAULT_DESTINATION,
            'tool_spec': {'cores': 1, 'mem': 0.3, 'gpus': 0, 'runner': 'condor',
                          'params': {'rank': 'GalaxyGroup == "metadata"',
                                     'requirements': 'GalaxyTraining == false',
                                     }
                          }
        }
        tool_id = '__SET_METADATA__'

        env, params, runner, tool_spec, tags = _gateway(tool_id, '', '', '', '')

        self.assertEqual(env, result['env'])
        self.assertEqual(params, result['params'])
        self.assertEqual(runner, result['runner'])
        self.assertEqual(tool_spec, result['tool_spec'])

    def test_tool_interactive_tool_(self):
        """
        Test that it pass default values if called without specifications
        """
        result = {
            'params': {'request_cpus': '1', 'request_memory': '4.0G', 'docker_enabled': 'True',
                       'requirements': 'GalaxyDockerHack == True && GalaxyGroup == "compute"',
                       'accounting_group_user': '', 'description': 'interactive_tool_unittest_tool'}
        }
        _tool_label = 'interactive_tool_unittest_tool'
        _dest_label = 'docker_unittest_destination'

        _tool_spec = {
            _tool_label:
            {
                'runner': _dest_label
            }
        }
        _dest_spec = {
            _dest_label:
            {
                'env': {},
                'params':
                {
                    'request_cpus': '{PARALLELISATION}',
                    'request_memory': '{MEMORY}',
                    'docker_enabled': True,
                    'requirements': 'GalaxyDockerHack == True && GalaxyGroup == "compute"'
                }
            }
        }

        self.td[_tool_label] = _tool_spec[_tool_label]
        self.sp[_dest_label] = _dest_spec[_dest_label]
        tool_id = _tool_label

        _, params, _, _, _ = _gateway(tool_id, '', '', '', '', tools_spec=self.td, dest_spec=self.sp)

        self.assertEqual(params, result['params'])


if __name__ == '__main__':
    unittest.main()
