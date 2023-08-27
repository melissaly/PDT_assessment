import sys
import logging

import CollateFiles

if __name__ == '__main__':
    logging.basicConfig(filename='app.log', level='info')
    args = sys.argv
    if len(args) != 3:
        print('Expected parameters: input directory and output file')
    else:
        CollateFiles.collate_files(args[1], args[2])
