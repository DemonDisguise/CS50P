from PIL import Image, ImageOps
import sys
import os


def main():
    get_input()


def get_input():
    if len(sys.argv) < 3:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")
    else:
        formats = [".jpg", ".jpeg", ".png"]
        inpex = os.path.splitext(sys.argv[1])[1].lower()
        outex = os.path.splitext(sys.argv[2])[1].lower()
        if all(x in formats for x in (inpex, outex)):
            if inpex == outex:
                get_photoedit(sys.argv[1], sys.argv[2])
            else:
                sys.exit("Input and output have different extensions")
        else:
            sys.exit("Invalid input")


def get_photoedit(inp, out):
    try:
        shirt = Image.open("shirt.png")
        with Image.open(inp) as fp:
            fp_cropped = ImageOps.fit(fp, shirt.size)
            fp_cropped.paste(shirt, mask=shirt)
            fp_cropped.save(out)
    except FileNotFoundError:
        sys.exit(f"{inp} does not exist")


if __name__ == "__main__":
    main()
