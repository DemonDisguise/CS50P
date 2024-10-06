import random, sys


def main():
    level = get_level()
    equations = 10
    score = 0
    chances = 3
    while equations != 0:
        if chances == 3:
            X, Y = generate_integer(level)

        try:
            get_answer = int(input(f"{X} + {Y} = "))
            actual_answer = X + Y
            if get_answer == actual_answer:
                equations -= 1
                score += 1
                chances = 3
                continue
            else:
                raise ValueError

        except (ValueError, NameError):
            print("EEE")
            chances -= 1
            pass

        except:
            print()
            sys.exit()

        if chances == 0:
            print(f"{X} + {Y} = {actual_answer}")
            chances = 3
            equations -= 1
            continue

    print(f"Score: {score}")


def get_level():
    while True:
        try:
            check_level = int(input("Level: "))
            if check_level in [1, 2, 3]:
                return check_level
        except ValueError:
            pass
        except:
            print()
            sys.exit()


def generate_integer(level):
    if level == 1:
        X = random.randint(0, 9)
        Y = random.randint(0, 9)
    elif level == 2:
        X = random.randint(10, 99)
        Y = random.randint(10, 99)
    else:
        X = random.randint(100, 999)
        Y = random.randint(100, 999)
    return X, Y


if __name__ == "__main__":
    main()

