import unittest

from jira_tool_edit.__main__ import get_replace_image


class MyTestCase(unittest.TestCase):

    def test_should_return_labels_in_first_line_when_get_labels_from_markdown_given_label_in_first_line(self):
        get_replace_image('OTRT-288', '/Users/shiwei.fu/Documents/WorkFlow/AR/i1', 'OTRT-288.md')


if __name__ == '__main__':
    unittest.main()
