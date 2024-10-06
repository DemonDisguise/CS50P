tweet = input("Input: ").strip()
formatted_tweet = ""
for ch in tweet:
    if ch.lower() not in "aeiou":
        formatted_tweet += ch
print(f"Output: {formatted_tweet}")
