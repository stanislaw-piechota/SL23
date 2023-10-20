from collections import Counter

MIN, MAX = 0, 1000
next_hsn = lambda c: 3 * c + 1 if c % 2 else c // 2


def hsn(c):
    sequence = [c]
    yield c
    while c > 1:
        c = next_hsn(c)
        yield c
        sequence.append(c)
    return sequence


if __name__ == "__main__":
    hsn_sequences = [hsn(start_number) for start_number in range(MIN, MAX + 1)]

    """EXERCISE 1"""
    hsn_lengths = [len(hsn_sequence) for hsn_sequence in hsn_sequences]
    max_length = max(hsn_lengths)
    print(f"Problem 1 (for range {MIN}-{MAX}):")
    print(f"- longest sequence contains {max_length} elements")
    print(f"- starts from seed: {MIN+hsn_lengths.index(max_length)}\n")

    """EXERCISE 2"""
    max_value = -1
    number_of_occurences = 0
    seeds_of_sequences = []
    for hsn_seqence in hsn_sequences:
        if (sequence_max := max(hsn_seqence)) > max_value:
            max_value = sequence_max
            number_of_occurences = 1
            seeds_of_sequences = [str(hsn_seqence[0])]
        elif sequence_max == max_value:
            number_of_occurences += 1
            seeds_of_sequences.append(str(hsn_seqence[0]))

    print(f"Problem 2 (for range {MIN}-{MAX}):")
    print(f"- highest element value is {max_value}")
    print(f"- found {number_of_occurences} times")
    print(f"- in sequences starting from seeds:", ", ".join(seeds_of_sequences), "\n")

    """EXERCISE 3"""
    # dict_of_lengths = {hsn_length:hsn_lengths.count(hsn_length) for hsn_length in set(hsn_lengths)}
    dict_of_lengths = Counter(hsn_lengths)
    common_length, number_of_occurences = dict_of_lengths.most_common()[0]
    seeds_of_sequences = []
    current_index = 0

    for _ in range(number_of_occurences):
        next_index = hsn_lengths.index(common_length, current_index)
        seeds_of_sequences.append(str(hsn_sequences[next_index][0]))
        current_index = next_index + 1

    print(f"Problem 3 (for range {MIN}-{MAX}): ")
    print(f"- most common sequence length is {common_length}")
    print(f"- found times {number_of_occurences}")
    print(f"- in sequences starting from seeds: ", ", ".join(seeds_of_sequences), "\n")
