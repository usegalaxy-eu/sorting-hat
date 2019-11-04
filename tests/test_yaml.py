import unittest
import collections
from string import ascii_letters

from sorting_hat import TOOL_DESTINATION_PATH, SPECIFICATIONS


class TestYamlFile(unittest.TestCase):

    def test_yaml_file_tool_destinations(self):
        """
        Check duplications in tools names
        """
        cnt = collections.Counter()
        with open(TOOL_DESTINATION_PATH, 'r') as fp:
            lines = fp.readlines()
        for l in lines:
            if l[0] in ascii_letters:
                cnt[l.split(':')[0]] += 1

        k, v = cnt.most_common(5)[0]
        self.assertEqual(1, v)

    def test_yaml_file_specifications(self):
        """
        Test if destinations are using allowed keys
        """
        allowed_keys = ['limits', 'env', 'params']
        for destination, value in SPECIFICATIONS.items():
            for k in value.keys():
                self.assertTrue(k in allowed_keys)


if __name__ == '__main__':
    unittest.main()
