import csv
import sys

def main():
    get_input()


def get_input():
    if len(sys.argv) < 3:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")
    else:
        if sys.argv[1][-4:] == '.csv' and sys.argv[2][-4:] == '.csv':
            get_csv(sys.argv[1], sys.argv[2])
        else:
            sys.exit("Not a CSV file")


def get_csv(input, output):
    try:
        with open(input) as fr:
            data = csv.DictReader(fr)
            with open(output, "w") as fw:
                header = ["first", "last", "house"]
                writer = csv.DictWriter(fw, fieldnames = header)
                writer.writeheader()
                for character in data:
                    last, first = character["name"].split(", ")
                    house = character["house"]
                    writer.writerow({"first": first, "last": last, "house": house})
    except FileNotFoundError:
        sys.exit(f"Could not read {input}")


if __name__ == "__main__":
    main()
