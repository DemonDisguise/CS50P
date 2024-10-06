import re
import sys


def main():
    print(validate(input("IPv4 Address: ")))


def validate(ip):
    ipaddr = "([0-1]?([0-9]?){2}|2[0-4]?[0-9]?|25[0-5]?)"
    matcher = re.search(rf"^{ipaddr}\.{ipaddr}\.{ipaddr}\.{ipaddr}$", ip)
    if matcher:
        return True
    else:
        return False

if __name__ == "__main__":
    main()
