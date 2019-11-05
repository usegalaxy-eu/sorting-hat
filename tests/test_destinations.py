import unittest

from sorting_hat import DEFAULT_DESTINATION, SPECIFICATIONS, SPECIFICATION_PATH


class TestDestinations(unittest.TestCase):

    def test_default_destination(self):
        """
        Test DEFAULT_DESTINATION exists in SPECIFICATIONS
        """
        self.assertTrue(DEFAULT_DESTINATION in SPECIFICATIONS,
                        msg="{} not in {}".format(DEFAULT_DESTINATION, SPECIFICATION_PATH))


if __name__ == '__main__':
    unittest.main()
