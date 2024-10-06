def main():
    greeting = input("Greeting: ").strip().capitalize()
    value(greeting)


def value(message):
    message = message.strip().capitalize()
    if message.startswith("Hello"):
        return 100
    elif message.startswith("H"):
        return 20
    else:
        return 0

if __name__ == "__main__":
    main()
