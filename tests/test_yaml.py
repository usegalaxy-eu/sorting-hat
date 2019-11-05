import unittest
import collections
from string import ascii_letters

from sorting_hat import TOOL_DESTINATION_PATH, TOOL_DESTINATION_ALLOWED_KEYS, TOOL_DESTINATIONS, \
                        SPECIFICATION_ALLOWED_KEYS, SPECIFICATIONS


class TestYamlFile(unittest.TestCase):

    def test_tool_destinations_names(self):
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

    def test_tool_destinations_keys(self):
        """
        Test if tools are using allowed keys
        """
        for tool, value in TOOL_DESTINATIONS.items():
            for k in value.keys():
                self.assertTrue(k in TOOL_DESTINATION_ALLOWED_KEYS, msg="{} in {} is not an allowed key".format(k, tool))

    def test_specifications_keys(self):
        """
        Test if destinations are using allowed keys
        """
        for destination, value in SPECIFICATIONS.items():
            for k in value.keys():
                self.assertTrue(k in SPECIFICATION_ALLOWED_KEYS)


if __name__ == '__main__':
    unittest.main()
