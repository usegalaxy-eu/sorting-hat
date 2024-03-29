import unittest
import collections
from string import ascii_letters

from sorting_hat import sh_conf, TOOL_DESTINATION_PATH, TOOL_DESTINATIONS, SPECIFICATIONS

SPECIFICATION_ALLOWED_KEYS = sh_conf.get('allowed_keys', 'destination_specifications')
TOOL_DESTINATION_ALLOWED_KEYS = sh_conf.get('allowed_keys', 'tool_destinations')


class TestYamlFile(unittest.TestCase):

    def test_tool_destinations_names(self):
        """
        Check duplications in tools names
        """
        cnt = collections.Counter()
        with open(TOOL_DESTINATION_PATH, 'r') as fp:
            lines = fp.readlines()
        for line in lines:
            if line[0] in ascii_letters:
                cnt[line.split(':')[0]] += 1

        k, v = cnt.most_common(1)[0]
        self.assertEqual(1, v, msg="Duplication found: {} is present {} times".format(k, v))

    def test_tool_destinations_keys(self):
        """
        Test if tools are using allowed keys
        """
        for tool, value in TOOL_DESTINATIONS.items():
            for k in value.keys():
                with self.subTest(k=k):
                    self.assertTrue(k in TOOL_DESTINATION_ALLOWED_KEYS,
                                    msg="{} in {} tool is not an allowed key".format(k, tool))

    def test_specifications_keys(self):
        """
        Test if destinations are using allowed keys
        """
        for destination, value in SPECIFICATIONS.items():
            for k in value.keys():
                with self.subTest(k=k):
                    self.assertTrue(k in SPECIFICATION_ALLOWED_KEYS,
                                    msg="{} in {} destination is not an allowed key".format(k, destination))

    def test_specification_needed_keys(self):
        """
        Test if destinations have the needed keys
        """
        needed_keys = ['info', 'env', 'limits', 'params']
        for k in needed_keys:
            for destination, value in SPECIFICATIONS.items():
                if 'unittest' not in destination:
                    with self.subTest(destination=destination, value=value.keys()):
                        self.assertTrue(k in value,
                                        msg="{} is not defined into {} destination".format(k, destination))


if __name__ == '__main__':
    unittest.main()
