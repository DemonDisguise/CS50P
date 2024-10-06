import re


def main():
    print(count(input("Text: ")))


def count(s):
    regex = "(^|\W)um($|\W)"
    um_check = re.findall(regex, s, re.IGNORECASE)
    if um_check:
        return(len(um_check))


if __name__ == "__main__":
    main()
