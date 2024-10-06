import sys

def main():
    data = get_input()
    print(get_lines(data))


def get_input():
    if len(sys.argv) < 2:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 2:
        sys.exit("Too many command-line arguments")
    else:
        if sys.argv[1].endswith('.py'):
            return sys.argv[1]
        else:
            sys.exit("Not a python file")


def get_lines(data):
    try:
        lines = 0
        with open(data, 'r') as f:
            for line in f:
                if not (line.lstrip().startswith('#') or line.strip() == ""):
                    lines += 1
        return lines
    except FileNotFoundError:
        sys.exit("File does not exist")

if __name__ == "__main__":
    main()
