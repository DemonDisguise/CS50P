def main():
    word = input().strip()
    print(shorten(word))


def shorten(word):
    format_tweet = ''
    for ch in word:
        if ch.lower() not in "aeiou":
            format_tweet += ch
    return format_tweet


if __name__ == "__main__":
    main()
