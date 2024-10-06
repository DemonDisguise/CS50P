items = {
            "Baja Taco": 4.25,
            "Burrito": 7.50,
            "Bowl": 8.50,
            "Nachos": 11.00,
            "Quesadilla": 8.50,
            "Super Burrito": 8.50,
            "Super Quesadilla": 9.50,
             "Taco": 3.00,
            "Tortilla Salad": 8.00
        }

def main():
    get_price("Item: ", items)



def get_price(prompt, items):
    item_price = 0
    while True:
        try:
            get_input = input(prompt).title().strip()
            if get_input in items:
                item_price += items[get_input]
                print(f"Total: ${item_price:.2f}")
            else:
                pass
        except EOFError:
            print()
            break

if __name__ == "__main__":
    main()
