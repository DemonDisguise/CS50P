import re
import sys


def main():
    print(convert(input("Hours: ")))


def convert(s):
    hour = "(0?[1-9]|1[0-2]):?([0-5][0-9])? (AM|PM)"
    if link := re.search(rf"^{hour} to {hour}$", s):
        get_time = standard_time(link.group(1), link.group(2), link.group(3))
        time = standard_time(link.group(4), link.group(5), link.group(6))
        return f"{get_time} to {time}"
    else:
        raise ValueError


def standard_time(h, min, mer):
    if h == "12":
        if mer == "AM":
            hour = "00"
        else:
            hour = "12"
    else:
        if mer == "AM":
            hour = f"{int(h):02}"
        else:
            hour = f"{int(h)+12}"
    if min == None:
        minute = "00"
    else:
        minute = f"{int(min):02}"
    return f"{hour}:{minute}"

if __name__ == "__main__":
    main()
