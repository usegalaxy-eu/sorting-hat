import unittest

from sorting_hat import build_spec, _finalize_tool_spec, SPECIFICATIONS, TOOL_DESTINATIONS


class TestBuildSpecParam(unittest.TestCase):

    def test_pass_param_cores_with_default_destination(self):
        """
        Test tool with defined cores and destination by default
        'request_cpus' has to be in params with the same value provided by the tool
        """
        _tool_label = '_unittest_tool'

        _tool_spec = {_tool_label:
            {
                'cores': 3
            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]

        result = {
                'params': {'request_cpus': '3'}
        }
        
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, '', tools_spec=TOOL_DESTINATIONS)
        _, params, _, _, _ = build_spec(tool_spec, dest_spec=SPECIFICATIONS)


        self.assertEqual(params['request_cpus'], result['params']['request_cpus'])

    def test_pass_param_cores(self):
        """
        Test cores request for each tools.
        '*request_cpus' has to be in params with the same value provided by the tool.
        """
        for tool_label in TOOL_DESTINATIONS:
            if 'cores' in TOOL_DESTINATIONS[tool_label]:
                cores = str(TOOL_DESTINATIONS[tool_label]['cores'])
            else:
                cores = '1'
            
            result = {
                    'params': {'request_cpus': cores}
            }
            
            tool_id = tool_label
            tool_spec = _finalize_tool_spec(tool_id, '', tools_spec=TOOL_DESTINATIONS)
            _, params, dest, _, _ = build_spec(tool_spec, dest_spec=SPECIFICATIONS)

            if dest.startswith('remote_cluster_mq'):
                self.assertEqual(params['submit_request_cpus'], result['params']['submit_request_cpus'])
            if dest.startswith('condor'):
                self.assertEqual(params['request_cpus'], result['params']['request_cpus'])

    def test_pass_param_gpus_and_destination(self):
        """
        Test tool with undefined gpu and destination against all destinations.
        If destination starts with remote_cluster_mq, 'submit_request_gpus' hasn't 
        to be present in params.
        If destination starts with condor, 'request_gpus' hasn't 
        to be present in params.
        """
        _tool_label = '_unittest_tool'
        for dest in SPECIFICATIONS:   
            _tool_spec = {_tool_label:
                {
                    'runner':  dest,
                }
            }
            TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]

            tool_id = _tool_label
            tool_spec = _finalize_tool_spec(tool_id, '', tools_spec=TOOL_DESTINATIONS)
            _, params, _, _, _ = build_spec(tool_spec, dest_spec=SPECIFICATIONS)

            if dest.startswith('remote_cluster_mq'):
                self.assertFalse('submit_request_gpus' in params)
            if dest.startswith('condor'):
                self.assertFalse('request_gpus' in params)
  
    def test_pass_param_mem(self):
        """
        Test tool with defined mem
        """
        _tool_label = '_unittest_tool'

        _tool_spec = {_tool_label:
            {
                'mem': 32
            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]

        result = {
                'params': {'request_memory': '32.0G'}
        }
        
        tool_id = _tool_label

        tool_spec = _finalize_tool_spec(tool_id, '', tools_spec=TOOL_DESTINATIONS)
        _, params, _, _, _ = build_spec(tool_spec, dest_spec=SPECIFICATIONS)


        self.assertEqual(params['request_memory'], result['params']['request_memory'])


    def test_pass_docker_params(self):
        """
        Test if the tool's docker requirements are handled correctly
        """
        _tool_label = '_unittest_tool'
        for dest in SPECIFICATIONS:
            _tool_spec = {_tool_label: 
                {
                    'runner': dest,
                    'docker_set_user' : 1000,
                    'docker_run_extra_arguments': 'extra argument',
                }   
            }
            TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]
            result = {
                'params': {
                    'docker_set_user': '1000',
                    'docker_run_extra_arguments': 'extra argument',
                    },
            }

            tool_id = _tool_label
            tool_spec = _finalize_tool_spec(tool_id, '', tools_spec=TOOL_DESTINATIONS)
            _, params, _, _, _ = build_spec(tool_spec, dest_spec=SPECIFICATIONS)
        
            if 'docker_enabled' in params and params['docker_enabled']:
                for i in ['docker_set_user', 'docker_run_extra_arguments']:
                    self.assertEqual(params[i], result['params'][i])


if __name__ == '__main__':
    unittest.main()
