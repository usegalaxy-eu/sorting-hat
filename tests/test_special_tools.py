import unittest

from sorting_hat import _gateway, DEFAULT_DESTINATION


class TestSpecialTools(unittest.TestCase):

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
                          'requirements': 'GalaxyTraining == false', 'rank': 'GalaxyGroup == "upload"',
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
                          'requirements': 'GalaxyTraining == false', 'rank': 'GalaxyGroup == "upload"',
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
                          'requirements': 'GalaxyTraining == false', 'rank': 'GalaxyGroup == "metadata"'
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
            'tool_spec': {'cores': 1, 'mem': 4.0, 'gpus': 0, 'force_destination_id': False, 'runner': 'condor',
                          'requirements': 'GalaxyDockerHack == True && GalaxyGroup == "compute"'}
        }
        tool_id = 'interactive_tool_unittest_tool'

        env, params, runner, tool_spec, tags = _gateway(tool_id, '', '', '', '')

        self.assertEqual(tool_spec, result['tool_spec'])


if __name__ == '__main__':
    unittest.main()
