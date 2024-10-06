import re
import sys


def main():
    print(parse(input("HTML: ")))


def parse(s):
    format = r"src=\"http(s)?:\/\/(www\.)?youtube\.com\/embed\/([a-zA-Z0-9]+)\""
    if re.search(r"<iframe(.)*><\/iframe>",s):
        if link := re.search(format, s):
            return f"https://youtu.be/{link.group(3)}"
        else:
            return None
    else:
        return None


if __name__ == "__main__":
    main()
