"""
Test the main functionality
"""
import os
import unittest
import src.CollateFiles
import TestUtils


class TestCollateFiles(unittest.TestCase):
    @classmethod
    def tearDownClass(cls) -> None:
        TestUtils.clean_out_dir('test_files/out')

    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))

    # tests for collate_files function
    def general_test(self, test_type):
        test_dir, out_file, expected_file = TestUtils.create_test_dir_names(test_type)
        src.CollateFiles.collate_files(test_dir, out_file)
        out_text = TestUtils.read_file(out_file)
        expected_text = TestUtils.read_file(expected_file)
        self.assertEqual(out_text, expected_text)

    def test_no_blanks(self):
        self.general_test('no_blanks')

    def test_words_with_blanks(self):
        self.general_test('words_with_blanks')

    def test_blanks_only(self):
        self.general_test('blanks_only')

    def test_empty_files(self):
        self.general_test('empty_files')

    def test_zero_files(self):
        self.general_test('zero_files')

    def test_one_file(self):
        self.general_test('one_file')

    def test_csv(self):
        self.general_test('csv')

    def test_existing_out_file(self):
        # create existing file
        out_file_name = 'test_files/out/{}.txt'.format('existing')
        existing_file = open(os.path.join(os.getcwd(), out_file_name), 'x')
        existing_file.close()
        self.general_test('words_with_blanks')

    def test_wrong_types(self):
        self.general_test('wrong_types')

    def test_invalid_dir(self):
        try:
            self.general_test('invalid')
            self.fail('Expected error from invalid directory')
        except Exception:
            pass

    # tests for open_files function
    def test_valid_files(self):
        test_dir, out_name, expected = TestUtils.create_test_dir_names('words_with_blanks')
        test_files, out_file = src.CollateFiles.open_files(test_dir, out_name)
        for test_file in test_files:
            test_file.close()
        out_file.close()

        self.assertEqual(len(test_files), 2)

    def test_invalid_files(self):
        test_dir, out_name, expected = TestUtils.create_test_dir_names('invalid')
        test_files = None
        try:
            test_files, out_file = src.CollateFiles.open_files(test_dir, out_name)
            self.fail('Expected error from invalid directory')
        except Exception:
            self.assertIsNone(test_files)
            pass


if __name__ == '__main__':
    unittest.main()
