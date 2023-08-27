"""
Test the performance of the program
"""
import logging
import os
import string
import sys
import random
import configparser
import time

import TestUtils

logger = logging.getLogger(__name__)


def read_config(test_type):
    """
    Transforms the configuration file into a dict
    :param test_type: the section to look for in the cfg
    :return: a dict of the parameters
    """
    config_reader = configparser.ConfigParser()
    config_reader.read('perf.cfg')

    fields = ['file_count_start',
              'file_count_end',
              'file_count_step',
              'avg_file_size_start',
              'avg_file_size_end',
              'avg_file_size_step',
              'num_iterations']
    values = [config_reader.getint(test_type, field) for field in fields]
    return dict(zip(fields, values))


def generate_files(file_count, file_size):
    """
    Create the files needed for the test
    :param file_count: number of files to be created
    :param file_size: average number of lines per file
    :return: none, but creates files
    """
    # arbitrary parameters
    min_word_size = 5
    max_word_size = 20
    file_size_range = int(file_size / 5)
    min_file_size = file_size - file_size_range
    max_file_size = file_size + file_size_range

    for i in range(file_count):
        file_name = 'test_files/perf_files/file{}'.format(i)
        file = None
        try:
            file = open(os.path.join(os.getcwd(), file_name), 'w')
            file_size = random.randint(min_file_size, max_file_size)
            for j in range(file_size):
                word_length = random.randint(min_word_size, max_word_size)
                word = ''.join(random.choices(string.ascii_letters, k=word_length))
                file.write(word + '\n')
        except Exception as e:
            if file is not None:
                file.close()
            logger.error('error creating file')
            logger.error(e)


def run_test(test_type):
    """
    Main test body
    :param test_type: LOAD or STRESS
    :return: none, but creates perf_results.csv
    """
    # create output file
    try:
        result_file = open(os.path.join(os.getcwd(), 'perf_results.csv'), 'w')
        file_header = 'file_count,avg_file_size,avg_time_ms\n'
        result_file.write(file_header)
    except Exception as e:
        logger.error('Unable to create results file')
        logger.error(e)
        raise Exception(e)

    # set up input test files
    file_parameters = read_config(test_type)
    file_count_steps = range(
        file_parameters['file_count_start'],
        file_parameters['file_count_end']+1,
        file_parameters['file_count_step']
    )
    file_size_steps = range(
        file_parameters['avg_file_size_start'],
        file_parameters['avg_file_size_end']+1,
        file_parameters['avg_file_size_step']
    )

    # set up test
    iterations = file_parameters['num_iterations']
    test_dir, out_file, expected = TestUtils.create_test_dir_names('perf_files')
    command = "python3 ../src/main.py {} {}".format(test_dir, out_file)

    try:
        # iterate through all file count and file size steps
        for file_count in file_count_steps:
            for file_size in file_size_steps:
                # create the correct size and number of files for test
                generate_files(file_count, file_size)

                # run test
                start = time.time()
                for i in range(iterations):
                    os.system(command)

                # calculate average time of runs
                end = time.time()
                avg = (end - start) / iterations
                rounded_ms = round(avg*1000)

                # write results to csv
                result_file.write('{},{},{}\n'.format(
                    file_count,
                    file_size,
                    rounded_ms
                ))

                # delete files created (besides the csv)
                TestUtils.clean_out_dir("test_files/perf_files")
                TestUtils.clean_out_dir("test_files/out")
    except Exception as e:
        logger.error(e)

    result_file.close()


if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    logging.basicConfig(filename='perf.log')
    args = sys.argv
    if len(args) != 2:
        print("Expected parameter: 'LOAD' or 'STRESS' test. Aborting.")
    elif args[1] != 'LOAD' and args[1] != 'STRESS':
        print("Unrecognized test type. Please choose LOAD or STRESS test. Aborting.")
    else:
        run_test(args[1])
