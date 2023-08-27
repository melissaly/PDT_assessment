# PDT Assessment: Collate Files
Melissa Ly
August 2023

Thank you for your consideration.

## Expected Behavior
Prompt: This program consolidates data from multiple files into a single lexicographically-sorted file. It takes two arguments: an input directory path and an output file path. The input directory should contain newline-delimited text files sorted lexicographically. Blank lines may be interspersed throughout input files. The program creates an output file at the given path that contains the full set of unique text lines across all input files, lexicographically sorted, omitting any blank lines. 

Other implemented behavior: The file names are expected to be relative to where the user is calling from. If the output file already exists, it will be overwritten. The output file has a newline at the end. The program also accepts csv files as input. 

## Approach

The program iterates through all of the input files simultaneously to find the lowest string across the files, then writes the lowest strings to the output file. 

It reads a line from each of the files, stores them in an array, and finds the lowest string in the array. The file reader keeps track of the current location and when a file has the lowest word, the file location is advanced. The next line is read and written into the array so the process of finding the lowest string continues.

When the file reader reaches the end of the file, the file is removed from the array and the program continues with each of the other files until all files are removed from the array.

This program uses Python because it is easy to read and understand. Although space and time complexity are considered, overall latency was not so Python's main drawback, its speed, was not a significant negative. In addition, since no binary files are to be submitted, a Java or C++ program would have to be compiled after submission anyway so there are fewer benefits of using a compiled language as opposed to an interpreter language. 

## Time and Space Complexity
Let *n* be the number of files and *m* be the average number of lines per file.

### Time Complexity
#### Implemented
The outer loop of this iterates through each of the lines once (m x n lines). In each iteration, it needs to iterate through each of the files again to find the lowest word. This brings the time complexity up to O(m x n^2). 

#### Possible optimizations
Alternatively, instead of using the built-in *min* function, the program could implement a min-heap in order to find the lowest string more quickly and reduce the time complexity to O(m x n log(n)). 

Alternatively, the strings could be written into a sorted map or dictionary. This may decrease the actual runtime in theory because finding the lowest string would not need to read through each file's word each time. However, the time complexity for inserting a word into a sorted list remains O(n) so the time complexity would not be improved. In addition, the maintenance of the map or dictionary may surpass the time saved from not iterating through the whole list, as arrays are very quick. 

These alternatives were not implemented for the sake of simplicity. 

In the case where the files are very unbalanced (for example, 10 files have 5 lines each and 1 file has 5,000 lines) the runtime would not scale to the largest (that is, *m* should be the average and not the maximum number of lines) because when a file reaches the end, it is removed from the list and is no longer iterated through. 

If all of the lines in the file were read at once, the program would likely run faster but the time complexity would not change.

### Space Complexity 
This analysis ignores the space of the actual files and only considers the space that is used at runtime.

This program stores only one line from each of the files at a time, so the space it takes does not scale to the number of lines in a file. This program takes O(n) space. 

>Reading all lines at once would greatly increase the space complexity since all of the lines must be stored at once, so the space would be O(n x m). 

## Testing

### Correctness Tests
These tests are contained and do not need input to run. 

#### Unit Tests
In the style of test-driven development, most of the unit and integration tests were written before the implementation of the program. The unit tests take both valid and invalid inputs and checks the output against pre-defined expected outputs. Before the unit tests are run, the directory location of the program is set to the location of the script (see below) so the input files are relative to the test and not where the program is being run. The test also automatically deletes all the test output files.

#### Integration Tests
The integration tests run the program from the OS as would be expected when in use. It also changes the directory location to the location of the script. 

### Performance Tests
In the interest of evaluating the time complexity in regards to both file count and file size, the performance test runs within a provided range for both of those parameters. They are configured in *perf.cfg*. The test also expects the input of "LOAD" or "STRESS" when running the test. These parameters are set separately in *perf.cfg*. The results can be found in *perf_results.csv*. Any errors are output in *perf.log*.

The configurable parameters are
Parameter|Description
-|-
|file_count_start|Starting count for the number of files       
|file_count_end|Final count for the number of files
|file_count_step|Increase of number of files for each iteration
|avg_file_size_start|Starting file size for each file
|avg_file_size_end|Ending file size for each file
|avg_file_size_step|Increase of size of files for each iteration
|num_iterations|Number of times the program is run for each step

The results are in csv format so they can easily be analyzed by numpy and pandas, but in the interest of not adding dependencies, that was not done in this program.

## Running the Program
### Bash Script
This program offers a bash script in order to run the program and tests.
The file is at the root of the project and is named `collate_files.sh`.  It takes at least one parameter: the action you wish to run. The actions are run (the main program), unit_tests, integration_tests, perf_tests, and all_tests, and clean. Clean will delete *app.log*, *perf.log*, *perf_results.csv*, and all files in *test_files/out*.

When running the main program, it also requires the input directory and output file as parameters. The program will start without them, but will immediately exit. When running perf_tests or all_tests, it also requires "LOAD" or "STRESS" as another parameter (but the tests do not take input directories or output file locations; those are contained in the test folder). The perf test also will start and immediately exit if the expected parameter are not provided.

This script can be run from any directory.

### Running Normal Python Commands
The program and tests can be run using the normal python commands, but must be run from the project root directory.
Action|Command
-|-
run| `python3 ./src/main.py $INPUT_DIR $OUTPUT_FILE`
unit test|`python3 -m unittest discover -s test -p TestCollateFiles.py`
integration test|`python3 -m unittest discover -s test -p IntegrationTest.py`
performance test|`python3 ./test/PerformanceTest.py $TEST_TYPE`


## Given Time Constraints
This work was done with the understanding that there were no time constraints. However, that is not realistic in a work environment. If I was more limited on time, I would not have written the bash script or the performance tests. It would not have been much faster if I had reduced the unit tests, given how standardized they were. 
