"""
Common functionality needed across the tests
"""
import logging
import os

logger = logging.getLogger(__name__)


def read_file(filename):
    """
    Reads the file from the name given
    :param filename: does not need to be absolute
    :return: the entire text of the file
    """
    file = open(os.path.join(os.getcwd(), filename), 'r')
    try:
        text = file.read()
        file.close()
        return text
    except Exception as e:
        file.close()
        logger.error('Unable to read file %s', filename)
        logger.error(e)
        raise IOError(e)


def create_test_dir_names(test_type):
    """
    Automatically fills the path names given the test type
    :param test_type: name of test under test_files
    :return: relative path names
    """
    test_dir_name = "test_files/" + test_type
    out_file_name = "test_files/out/{}.txt".format(test_type)
    expected_file_name = "test_files/expected/{}_expected.txt".format(test_type)
    return test_dir_name, out_file_name, expected_file_name


def clean_out_dir(dir_name):
    """
    For cleaning up test files
    :param dir_name: the directory to be cleared of all files
    :return:
    """
    out_dir = os.path.join(os.getcwd(), dir_name)
    all_files = os.listdir(out_dir)
    for file in all_files:
        os.remove(os.path.join(out_dir, file))
