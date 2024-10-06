import inflect
p = inflect.engine()

def main():
    name_list = get_names()
    print(f"\nAdieu, adieu, to {p.join(name_list)}")


def get_names():
    names = []
    while True:
        try:
            get_input = input("Name: ")
            names.append(get_input)
            pass
        except EOFError:
            return names

main()
