import unittest
import random

from sorting_hat import _special_case


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


if __name__ == '__main__':
    unittest.main()
