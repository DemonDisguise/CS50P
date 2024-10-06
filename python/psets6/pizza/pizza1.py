import sys
import csv
from tabulate import tabulate

def main():
    get_csv = get_input()
    print(tabulize(get_csv))


def get_input():
    if len(sys.argv) < 2:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 2:
        sys.exit("Too many command-line arguments")
    else:
        if sys.argv[1][-4:] == '.csv':
            return sys.argv[1]
        else:
            sys.exit("Not a CSV file")


def tabulize(file):
    try:
        with open(file, 'r') as f:
            read_data = csv.reader(f)
            table = tabulate(read_data, headers="firstrow", tablefmt="grid")
        return table
    except FileNotFoundError:
        sys.exit("File does not exist")


if __name__ == "__main__":
    main()
