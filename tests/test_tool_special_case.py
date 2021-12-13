import unittest
import random

from sorting_hat import _special_case, _compute_memory_for_hifiasm


class TestToolsSpecialCases(unittest.TestCase):

    def test_it_authorization(self):
        """
        IT tool can be used only by registered users, otherwise an exception must be raised
        IT label starts with 'interactive_tool' and unregistered user id is -1
        """
        tool_id = "interactive_tool_testunittest"
        user_id = -1
        with self.assertRaises(Exception):
            _special_case(None, tool_id, user_id, None)

        user_id = random.randint(0, 100000)
        self.assertEqual(None, _special_case(None, tool_id, user_id, None))

    def test_it_ml_authorization(self):
        """
        interactive_tool_ml_jupyter_notebook tool can be used only by users enrolled into the
        interactive-tool-ml-jupyter-notebook role. A request by a user not enrolled has to raise
        an exception.
        """
        tool_id = "interactive_tool_ml_testunittest"
        user_role = 'interactive-tool-ml-jupyter-notebook'

        user_roles = [user_role]
        self.assertEqual(None, _special_case(None, tool_id, None, user_roles))

        user_roles = ['not_' + user_role]
        with self.assertRaises(Exception):
            _special_case(None, tool_id, None, user_roles)

    def test_gmx_sim_limit(self):
        """
        If md_step parameter of tool 'gmx_sim is bigger than md_steps_limit
        and the user is not enrolled into the role 'gmx_sim_powerusers',
        an exception has to be raised.
        """
        md_steps_limit = 1000000
        tool_id = 'gmx_sim'
        user_role = 'gmx_sim_powerusers'
        param_dict = {}
        param_dict.setdefault('sets', {})['mdp'] = {'md_steps': md_steps_limit + 1}

        user_roles = [user_role]
        self.assertEqual(None, _special_case(param_dict, tool_id, None, user_roles))

        user_roles = ['not_' + user_role]
        with self.assertRaises(Exception):
            _special_case(param_dict, tool_id, None, user_roles)

    def test_compute_memory_for_hifiasm(self):
        """
        this function returns a number, rounded upward to its nearest integer,
        as result of this formula:
        (hg_size*(kcov*2) * 1.75
        hg_size can have suffix like m,M,k,K,g,G and is a float
        kcov is an integer
        """
        test_array = [
            {'kcov': 40, 'hg_size': '3g', 'result': 420},
            {'kcov': 40, 'hg_size': '3G', 'result': 420},
            {'kcov': 40, 'hg_size': '3.1g', 'result': 434},
            {'kcov': 40, 'hg_size': '3.1G', 'result': 434},
            {'kcov': 40, 'hg_size': '3,1g', 'result': 434},
            {'kcov': 40, 'hg_size': '3,1G', 'result': 434},
            {'kcov': 40, 'hg_size': '2.6g', 'result': 364},
            {'kcov': 40, 'hg_size': '100m', 'result': 14},
            {'kcov': 36, 'hg_size': '100m', 'result': 13},
        ]
        param_dict = {}
        param_dict.setdefault('advanced_options', {})
        for t in test_array:
            param_dict['advanced_options']['hg_size'] = t['hg_size']
            param_dict['advanced_options']['kcov'] = t['kcov']
            with self.subTest(hg_size=t['hg_size'], kcov=t['kcov']):
                self.assertEqual(t['result'], _compute_memory_for_hifiasm(param_dict))


if __name__ == '__main__':
    unittest.main()
