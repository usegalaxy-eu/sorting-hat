import unittest

from sorting_hat import _gateway, SPECIFICATIONS, TOOL_DESTINATIONS


class TestBuildSpecTags(unittest.TestCase):

    def test_no_tags(self):
        """
        Test tags is None if not present in tool or destination
        see: https://docs.galaxyproject.org/en/master/_modules/galaxy/jobs.html#JobDestination
        """
        _tool_label = '_unittest_tool'
        _dest_label = '_unittest_destination'

        _tool_spec = {_tool_label:
            {
                'runner': _dest_label
            }
        }

        _dest_spec = {_dest_label:
            {
                'env': {},
                'params': {}
            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]
        SPECIFICATIONS[_dest_label] = _dest_spec[_dest_label]

        result = None
        tool_id = _tool_label

        env, params, runner, tool_spec, tags = _gateway(tool_id, '', '', '')
        self.assertEqual(tags, result)

    def test_get_tags_from_tool(self):
        """
        Test if tags string is collected from tool's specification
        """
        _tool_label = '_unittest_tool'
        _tool_tags = 'unittest_tool_tag'

        _tool_spec = {_tool_label:
            {
                'tags': _tool_tags
            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]

        result = _tool_tags
        tool_id = _tool_label

        env, params, runner, tool_spec, tags = _gateway(tool_id, '', '', '')
        self.assertEqual(tags, result)

    def test_get_tags_from_destination(self):
        """
        Test if tags string is collected from destination's specification
        """
        _tool_label = '_unittest_tool'
        _dest_label = '_unittest_destination'
        _dest_tags = 'unittest_destination_tag'

        _tool_spec = {_tool_label:
            {
                'runner': _dest_label
            }
        }

        _dest_spec = {_dest_label:
            {
                'env': {},
                'params': {},
                'tags': _dest_tags
            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]
        SPECIFICATIONS[_dest_label] = _dest_spec[_dest_label]

        result = _dest_tags
        tool_id = _tool_label

        env, params, runner, tool_spec, tags = _gateway(tool_id, '', '', '')
        self.assertEqual(tags, result)

    def test_get_tags_from_tool_and_destination(self):
        """
        Test if tags string is collected from tool and destination specifications
        """
        _tool_label = '_unittest_tool'
        _tool_tags = 'unittest_tool_tag'
        _dest_label = '_unittest_destination'
        _dest_tags = 'unittest_destination_tag'

        _tool_spec = {_tool_label:
            {
                'runner': _dest_label,
                'tags': _tool_tags
            }
        }

        _dest_spec = {_dest_label:
            {
                'env': {},
                'params': {},
                'tags': _dest_tags
            }
        }

        TOOL_DESTINATIONS[_tool_label] = _tool_spec[_tool_label]
        SPECIFICATIONS[_dest_label] = _dest_spec[_dest_label]

        tool_id = _tool_label

        env, params, runner, tool_spec, tags = _gateway(tool_id, '', '', '')

        self.assertIn(_tool_tags, tags)
        self.assertIn(_dest_tags, tags)


if __name__ == '__main__':
    unittest.main()
