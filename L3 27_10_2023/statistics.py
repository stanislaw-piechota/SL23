with open('dorian.txt') as file:
    text = file.read().lower()


"""PART 1"""
char_numbers = {char:text.count(char) for char in 'abcdefghijklmnopqrstuvwxyz1234567890,.? "-\'!;:' if text.count(char)}
stats = {}
for key, val in char_numbers.items():
    if stats.get(val):
        stats[val].append(key)
    else: stats[val] = [key]
stats = sorted(stats.items(), reverse=True)

print("Letter statistics:")
print("- 5 most common letters/chars:")
for i in range(5):
    print(f"letter/char \'"+"\', \'".join((pair:=stats[i])[1])+ f"\' found {pair[0]} times")

print("- 5 least common letters/chars:")
for i in range(-1, -6, -1):
    print(f"letter/char \'"+"\', \'".join((pair:=stats[i])[1])+ f"\' found {pair[0]} times")
print()


"""PART 2"""
words = []
words_number = {}
for word in text.split():
    words.append(word.strip())

for word in words:
    if words_number.get(word):
        words_number[word] += 1
    else:
        words_number[word] = 1

stats = {}
for key, val in words_number.items():
    if stats.get(val):
        stats[val].append(key)
    else:
        stats[val] = [key]
stats = sorted(stats.items(), reverse=True)

lengths = {}
for word in words:
    if lengths.get((length:=len(word))):
        if word in lengths.get(length):
            continue
        lengths[length].append(word)
    else:
        lengths[length] = [word]
lengths = sorted(lengths.items(), reverse=True)

print("Words statistics:")
print(f"- number of unique words: {len(set(words))}")
print('- 5 most common words:')
for i in range(5):
    print(f"word \'"+"\', \'".join((pair:=stats[i])[1])+ f"\' found {pair[0]} times")

print('- 5 longest words:')
for i in range(5):
    print(f"words of length {(pair:=lengths[i])[0]} are: \'"+"\', \'".join(pair[1])+'\'')
