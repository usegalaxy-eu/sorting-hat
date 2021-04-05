import unittest

from sorting_hat import _gateway, DEFAULT_DESTINATION, TOOL_DESTINATIONS, SPECIFICATIONS


class TestSpecialTools(unittest.TestCase):

    def test_tool_scanpy_suite(self):
        """
        Test that it pass default values if no specifications
        """
        tools_id = ['scanpy_inspect', 'scanpy_filter', 'scanpy_cluster_reduce_dimension',
                    'scanpy_normalize', 'scanpy_remove_confounders', 'scanpy_plot']
        for tool_id in tools_id:
            result = {
                'env': [{'name': 'NUMBA_CACHE_DIR', 'value': '/data/2/galaxy_db/tmp'},
                        {'name': 'OMP_NUM_THREADS', 'value': '4'},
                        {'name': 'OPENBLAS_NUM_THREADS', 'value': '4'},
                        {'name': 'MKL_NUM_THREADS', 'value': '4'},
                        {'name': 'VECLIB_MAXIMUM_THREADS', 'value': '4'},
                        {'name': 'NUMEXPR_NUM_THREADS', 'value': '4'},
                        {'name': 'NUMBA_NUM_THREADS', 'value': '4'},
                        {'name': 'GALAXY_MEMORY_MB', 'value': '4096'},
                        {'name': 'GALAXY_SLOTS', 'value': '4'}],
                'params': {'priority': '-128', 'request_cpus': '4', 'request_memory': '4.0G',
                           'tmp_dir': 'True', 'requirements': 'GalaxyGroup == "compute"',
                           'accounting_group_user': '', 'description': tool_id},
                'runner': DEFAULT_DESTINATION,
                'tool_spec': {'cores': 4,
                              'env': {'NUMBA_CACHE_DIR': '/data/2/galaxy_db/tmp', 'OMP_NUM_THREADS': 4,
                                      'OPENBLAS_NUM_THREADS': 4, 'MKL_NUM_THREADS': 4,
                                      'VECLIB_MAXIMUM_THREADS': 4, 'NUMEXPR_NUM_THREADS': 4,
                                      'NUMBA_NUM_THREADS': 4},
                              'mem': 4.0,
                              'gpus': 0,
                              'runner': DEFAULT_DESTINATION}
                }

            env, params, runner, tool_spec, tags = _gateway(tool_id, '', '', '', '')

            d1 = {n['name']: n['value'] for n in env}
            d2 = {n['name']: n['value'] for n in result['env']}
            for k, v in d1.items():
                self.assertEqual(d1[k], d2[k])
            self.assertEqual(params, result['params'])
            self.assertEqual(runner, result['runner'])
            self.assertEqual(tool_spec, result['tool_spec'])

    def test_docker_tools(self):
        """
        Test tools using local docker destination
        These tools need to have requirements allowing them to run on docker nodes only
        """
        result = {
            'params': {'requirements': 'GalaxyDockerHack == True && GalaxyGroup == "compute"'}
        }
        for tool_id, spec in TOOL_DESTINATIONS.items():
            with self.subTest(tool_id=tool_id):
                # remove permission to test admin tools also
                if 'permissions' in spec:
                    del spec['permissions']

                ts = {tool_id: spec}
                destination = spec['runner'] if 'runner' in spec else DEFAULT_DESTINATION
                env, params, runner, tool_spec, tags = _gateway(tool_id, '', '', '', '', tools_spec=ts)

                if 'condor' in destination:
                    if 'docker_enabled' in params and params['docker_enabled'] in ('true', 'True'):
                        self.assertEqual(params['requirements'], result['params']['requirements'])


if __name__ == '__main__':
    unittest.main()
