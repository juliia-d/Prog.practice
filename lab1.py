import argparse
import sys
import typer
from typing import List, Optional
from pathlib import Path


def read_numbers_from_file(prog_py_file):
    numbers = []
    with open(prog_py_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                numbers.append(int(line))
    return numbers

def write_output(result, prog_py_output=None):
    if prog_py_output:
        with open(prog_py_output, 'w') as f:
            f.write(str(result))
    else:
        print(result)


def main():
    args = sys.argv[1:]

    numbers = []
    input_file = None
    output_file = None

    i = 0
    while i < len(args):
        if args[i] == '-f':
            input_file = args[i + 1]
            i += 2
        elif args[i] == '-o':
            output_file = args[i + 1]
            i += 2
        else:
            numbers.append(int(args[i]))
            i += 1

    if input_file:
        numbers = read_numbers_from_file(input_file)

    result = sum(numbers)
    write_output(result, output_file)

if __name__ == "__main__":
    main()
