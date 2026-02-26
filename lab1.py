import argparse


def read_numbers_from_file():
    numbers = []
    with open('file', 'r') as f:   
        for line in f:
            line = line.strip()
            if line:
                numbers.append(int(line))
    return numbers

def write_output(result):
    with open('output', 'w') as f:  
        f.write(str(result))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("numbers", nargs="*", type=int)
    parser.add_argument("-f", "--file", action="store_true")
    parser.add_argument("-o", "--output", action="store_true")
    args = parser.parse_args()

    total = 0

    if args.file:
        total = sum(read_numbers_from_file())
    else:
        total = sum(args.numbers)

    if args.output:
        write_output(total)
    else:
        print(total)


if __name__ == "__main__":
    main()
