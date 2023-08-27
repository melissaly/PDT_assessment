"""
Functions for collating files.
"""
import logging
import os

logger = logging.getLogger(__name__)


def collate_files(input_dir_name, output_file_name):
    """
    :param input_dir_name: directory where the files are read
    :param output_file_name: path of file where result is written
    :return: none
    """
    input_files, output_file = open_files(input_dir_name, output_file_name)
    try:
        # create a list of the first lines of every file
        next_words = list()
        prev_word = None
        for i in range(len(input_files)):
            next_words.append(input_files[i].readline())
        # continue reading as long as you haven't reached all EOFs
        while len(input_files) > 0:
            min_word = min(next_words)
            min_idx = next_words.index(min_word)
            min_file = input_files[min_idx]
            # for repeats and empty lines, keep reading
            while min_word == '\n' or min_word == prev_word:
                next_words[min_idx] = min_file.readline()
                min_word = min(next_words)
                min_idx = next_words.index(min_word)
                min_file = input_files[min_idx]
            # at end of file, remove from file list and close
            if min_word == '':
                min_file.close()
                input_files.pop(min_idx)
                next_words.pop(min_idx)
            else:
                # write line into output file
                output_file.write(min_word.strip() + '\n')
                next_words[min_idx] = min_file.readline()
                prev_word = min_word
        output_file.close()
        logger.info('Completed successfully')
    except Exception as e:
        # be sure to always close files
        for input_file in input_files:
            input_file.close()
        output_file.close()
        logger.error(e)
        raise Exception(e) from None


def open_files(input_dir_name, output_file_name):
    """
    Helper method for collate_files. Opens the first files.
    Throws exceptions when the input directory is invalid or
    the output file cannot be opened. Ignores invalid input files.
    :param input_dir_name: directory where the files are read
    :param output_file_name: path of file where result is written
    :return: list of opened input files, opened output file
    """
    input_dir_name = os.path.join(os.getcwd(), input_dir_name)
    output_file_name = os.path.join(os.getcwd(), output_file_name)

    # check input directory
    try:
        input_file_names = os.listdir(input_dir_name)
    except Exception as exc:
        logger.error('Invalid directory %s', input_dir_name)
        logger.error(exc)
        raise Exception(exc) from None
    input_files = list()
    # place opened files in list
    for input_file_name in input_file_names:
        try:
            if input_file_name.endswith('.txt') or input_file_name.endswith('.csv'):
                input_files.append(open(os.path.join(input_dir_name, input_file_name), 'r'))
        except IOError as exc:
            logger.error('Unable to open file %s', input_file_name)
            logger.error(exc)
            # ignore file and continue on

    # overwrites existing files, else creates a new file
    output_file = None
    try:
        output_file = open(output_file_name, 'w')
    except IOError as e:
        if output_file is not None:
            output_file.close()
        logger.error('Unable to open output file %s', output_file_name)
        logger.error(e)
        raise IOError(e) from None

    logger.info('Successfully opened files')
    return input_files, output_file
