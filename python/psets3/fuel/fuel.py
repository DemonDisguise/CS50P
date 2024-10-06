def main():
    fuel_input = get_fuel("Fraction: ")
    if fuel_input <= 1:
        print("E")
    elif fuel_input >= 99:
        print("F")
    else:
        print(f"{fuel_input}%")


def get_fuel(prompt):
    while True:
        try:
            get_input = input(prompt)
            x, y = get_input.strip().split("/")
            if x.strip().isdigit() and y.strip().isdigit() and int(x) <= int(y):
                return round(int(x) / int(y) * 100)
            else:
                pass
        except (ValueError, ZeroDivisionError):
            pass


main()
