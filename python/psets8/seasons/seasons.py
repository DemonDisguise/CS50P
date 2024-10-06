from datetime import date
import inflect
import sys
import operator

p = inflect.engine()


class Convert:
    def __init__(self, time):
        self.minutes = time * 24 * 60

    def __str__(self):
        return f"{(p.number_to_words(self.minutes, andword='')).capitalize()} minutes"


def main():
    try:
        dob = input("Date of Birth: ")
        dob_format = operator.sub(date.today(), date.fromisoformat(dob))
        final = Convert(dob_format.days)
        print(final)
    except ValueError:
        sys.exit("Invalid date")


if __name__ == "__main__":
    main()
