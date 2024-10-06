import random, sys

def main():
    final_level = level()
    guess(final_level)


def level():
    while True:
        try:
            get_level = int(input("Level: "))
            if get_level > 0:
                return get_level
            else:
                pass
        except ValueError:
            pass
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit()


def guess(prompt):
    while True:
        try:
            rand_level = random.randint(1, prompt)
            guess = int(input("Guess: "))
            if guess > 0:
                if guess > rand_level:
                    print("Too large!")
                    pass
                elif guess < rand_level:
                    print("Too small!")
                    pass
                else:
                    print("Just right!")
                    sys.exit()
            else:
                pass
        except ValueError:
            pass
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit()


main()
