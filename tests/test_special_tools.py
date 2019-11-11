import unittest

from sorting_hat import _gateway, DEFAULT_DESTINATION


class TestSpecialTools(unittest.TestCase):

    def test_tool_upload1(self):
        """
        Test that it pass default values if no specifications
        """
        result = {
            'env': [{'name': 'NUMBA_CACHE_DIR', 'value': '/data/2/galaxy_db/tmp'}, {'name': 'TEMP', 'value': '/data/1/galaxy_db/tmp/'}],
            'params': {'priority': '-128', 'request_memory': '0.3G', 'tmp_dir': 'True', 'requirements':
                       'GalaxyTraining == false', 'rank': 'GalaxyGroup == "upload"',
                       'accounting_group_user': '', 'description': 'upload1'},
            'runner': DEFAULT_DESTINATION,
            'tool_spec': {'mem': 0.3, 'runner': 'condor', 'rank': 'GalaxyGroup == "upload"',
                          'requirements': 'GalaxyTraining == false', 'env': {'TEMP': '/data/1/galaxy_db/tmp/'}
                          }
            }
        tool_id = 'upload1'

        env, params, runner, tool_spec, tags = _gateway(tool_id, '', '', '')
        self.assertEqual(env, result['env'])
        self.assertEqual(params, result['params'])
        self.assertEqual(runner, result['runner'])
        self.assertEqual(tool_spec, result['tool_spec'])

    def test_tool_data_fetch_(self):
        """
        Test that it pass default values if no specifications
        """
        result = {
            'env': [{'name': 'NUMBA_CACHE_DIR', 'value': '/data/2/galaxy_db/tmp'}, {'name': 'TEMP', 'value': '/data/1/galaxy_db/tmp/'}],
            'params': {'priority': '-128', 'request_memory': '0.3G', 'tmp_dir': 'True', 'requirements':
                       'GalaxyTraining == false', 'rank': 'GalaxyGroup == "upload"',
                       'accounting_group_user': '', 'description': '__DATA_FETCH__'},
            'runner': DEFAULT_DESTINATION,
            'tool_spec': {'mem': 0.3, 'runner': 'condor', 'rank': 'GalaxyGroup == "upload"',
                          'requirements': 'GalaxyTraining == false', 'env': {'TEMP': '/data/1/galaxy_db/tmp/'}
                          }
        }
        tool_id = '__DATA_FETCH__'

        env, params, runner, tool_spec, tags = _gateway(tool_id, '', '', '')

        self.assertEqual(env, result['env'])
        self.assertEqual(params, result['params'])
        self.assertEqual(runner, result['runner'])
        self.assertEqual(tool_spec, result['tool_spec'])

    def test_tool_set_metadata_(self):
        """
        Test that it pass default values if no specifications
        """
        result = {
            'env': [{'name': 'NUMBA_CACHE_DIR', 'value': '/data/2/galaxy_db/tmp'}],
            'params': {'priority': '-128', 'request_memory': '0.3G', 'tmp_dir': 'True', 'requirements':
                       'GalaxyTraining == false', 'rank': 'GalaxyGroup == "metadata"',
                       'accounting_group_user': '', 'description': '__SET_METADATA__'},
            'runner': DEFAULT_DESTINATION,
            'tool_spec': {'mem': 0.3, 'runner': 'condor', 'rank': 'GalaxyGroup == "metadata"',
                          'requirements': 'GalaxyTraining == false'}
        }
        tool_id = '__SET_METADATA__'

        env, params, runner, tool_spec, tags = _gateway(tool_id, '', '', '')

        self.assertEqual(env, result['env'])
        self.assertEqual(params, result['params'])
        self.assertEqual(runner, result['runner'])
        self.assertEqual(tool_spec, result['tool_spec'])


if __name__ == '__main__':
    unittest.main()
