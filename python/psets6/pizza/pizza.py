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
        get_table = []
        with open(file, 'r') as f:
            read_data = csv.DictReader(f)
            for row in read_data:
                get_table.append(row)
        table = tabulate(get_table, headers="keys", tablefmt="grid")
        return table
    except FileNotFoundError:
        sys.exit("File does not exist")


if __name__ == "__main__":
    main()
