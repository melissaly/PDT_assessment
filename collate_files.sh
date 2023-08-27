#!/bin/sh

DIR="$(dirname "$(realpath "$0")")"
START_DIR="$(pwd)"
cd "$DIR"
ACTION=${1}
case "${ACTION}" in
  "run") echo "Attempting to collate files. Please see app.log for details."
    python3 ./src/main.py ${2} ${3}
  ;;
  "unit_tests") echo "Running unit tests"
    python3 -m unittest discover -s test -p TestCollateFiles.py
  ;;
  "integration_tests") echo "Running integration tests"
    python3 -m unittest discover -s test -p IntegrationTest.py
    ;;
  "perf_tests") echo "Running performance tests. Please see perf.log for details."
    python3 ./test/PerformanceTest.py ${2}
    ;;
  "all_tests") echo "Running all tests"
    python3 -m unittest discover -s test -p TestCollateFiles.py
    python3 -m unittest discover -s test -p IntegrationTest.py
    python3 ./test/PerformanceTest.py ${2}
    ;;
  "clean") echo "Cleaning logs and results"
    rm -f test/perf.log
    rm -f test/perf_results.csv
    rm -f app.log
    rm -f test/app.log
    rm -rf test/test_files/out/*
    ;;
  *) echo "Unknown command! Available commands are:
    run
    unit_tests
    integration_tests
    perf_tests
    all_tests
    clean"
    ;;
esac

cd "$START_DIR"