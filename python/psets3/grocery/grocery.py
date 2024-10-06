def main():
    grocery_list = grocery()
    print()
    for item in sorted(grocery_list):
        print(grocery_list[item], item.upper())

def grocery():
    final_dict = {}
    while True:
        try:
            get_input = input().strip()
            if get_input in final_dict:
                final_dict[get_input] += 1
            else:
                final_dict[get_input] = 1
        except EOFError:
            return final_dict

main()
