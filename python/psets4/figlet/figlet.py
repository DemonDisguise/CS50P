from pyfiglet import Figlet
import random, sys

figlet = Figlet()

def main():
    try:
        if len(sys.argv) == 1:
            get_input = input("Input: ")
            get_formatted(get_input)
        elif len(sys.argv) == 3:
             if sys.argv[1] in ['-f', '--font']:
                  get_font = figlet.getFonts()
                  if sys.argv[2] in get_font:
                       get_input = input("Input: ")
                       manual_formatted(sys.argv[2], get_input)
                  else:
                       sys.exit("Invalid usage")
             else:
                  sys.exit("Invalid usage")
        else:
             sys.exit("Invalid usage")

    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit()


def get_formatted(prompt):
        get_fonts = figlet.getFonts()
        get_random = figlet.setFont(font=random.choice(get_fonts))
        print(figlet.renderText(prompt))

def manual_formatted(prompt, text):
     set_font = figlet.setFont(font=prompt)
     print(figlet.renderText(text))

main()
