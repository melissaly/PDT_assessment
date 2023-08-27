"""
Test functionality using shell commands
"""
import os
import unittest

import TestUtils


class IntegrationTest(unittest.TestCase):
    command_str = 'python3 ../src/main.py'
    test_dir, out_file, expected_file = TestUtils.create_test_dir_names('words_with_blanks')

    @classmethod
    def setUpClass(cls) -> None:
        # use script directory to ensure all files can be found
        os.chdir(os.path.dirname(__file__))

    def check_empty_dir(self):
        # failed calls should not create new files
        out_dir = os.path.join(os.getcwd(), 'test_files/out')
        all_files = os.listdir(out_dir)
        self.assertEqual(len(all_files), 0)

    def tearDown(self) -> None:
        # remove any output files after every test
        TestUtils.clean_out_dir('test_files/out')

    def test_expected(self):
        command = '{} {} {}'.format(self.command_str, self.test_dir, self.out_file)
        os.system(command)
        out_text = TestUtils.read_file(self.out_file)
        expected_text = TestUtils.read_file(self.expected_file)
        self.assertEqual(out_text, expected_text)

    def test_invalid_dir(self):
        try:
            os.system('{} {} {}'.format(self.command_str, 'invalid', self.out_file))
            self.fail('Expected exception for invalid dir')
        except Exception:
            self.check_empty_dir()
            pass

    def test_one_params(self):
        os.system('{} {}'.format(self.command_str, self.test_dir))
        self.check_empty_dir()

    def test_no_params(self):
        os.system('{}'.format(self.command_str))
        self.check_empty_dir()

    def test_many_params(self):
        os.system('{} {} {} {}'.format(
            self.command_str,
            self.test_dir,
            self.out_file,
            self.expected_file))
        self.check_empty_dir()


if __name__ == '__main__':
    unittest.main()
