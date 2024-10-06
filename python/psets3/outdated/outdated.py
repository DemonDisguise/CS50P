import sys

months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def main():
    get_format("Date: ", months)


def get_format(prompt, months):
    while True:
        try:
            get_input = input(prompt).strip().title()
            if "/" in get_input:
                month, day, year = list(map(int, get_input.split("/")))
                if checker(month, day, year) == True:
                    print(f"{year}-{int(month):02d}-{int(day):02d}")
                    break
                else:
                    pass

            elif "," in get_input:
                get_input = get_input.replace(",", "")
                month, day, year = get_input.split()
                if month in months:
                    month = int(months.index(month) + 1)
                    if checker(month, int(day), int(year)) == True:
                        print(f"{year}-{month:02d}-{int(day):02d}")
                        break
                    else:
                        pass
                else:
                    pass
            else:
                pass
        except ValueError:
            pass
        except (EOFError, KeyboardInterrupt):
            print()
            break


def checker(m, d, y):
    if 0000 <= y <= 9999:
        if m in [1, 3, 5, 7, 8, 10, 12]:
            if 1 <= d <= 31:
                return True
            else:
                return False
        elif m in [4, 6, 9, 11]:
            if 1 <= d <= 30:
                return True
            else:
                return False
        elif m == 2:
            if 1 <= d <= 29:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


main()
