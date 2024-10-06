import emoji
import sys

def main():
    try:
        get_input = input("Input: ")
        print(f"Output: {emoji.emojize(get_input, language='alias')}")
    except(EOFError, KeyboardInterrupt):
        print()
        sys.exit()

main()
