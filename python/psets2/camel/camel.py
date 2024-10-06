camel = input("camelCase: ").strip()
snake = ''
for ch in camel:
    if ch.islower():
        snake += ch
    else:
        snake += ("_" + ch.lower())
print(f"snake_case: {snake}")
