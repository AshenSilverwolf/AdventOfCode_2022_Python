priorities = {
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
    'e': 5,
    'f': 6,
    'g': 7,
    'h': 8,
    'i': 9,
    'j': 10,
    'k': 11,
    'l': 12,
    'm': 13,
    'n': 14,
    'o': 15,
    'p': 16,
    'q': 17,
    'r': 18,
    's': 19,
    't': 20,
    'u': 21,
    'v': 22,
    'w': 23,
    'x': 24,
    'y': 25,
    'z': 26,
    'A': 27,
    'B': 28,
    'C': 29,
    'D': 30,
    'E': 31,
    'F': 32,
    'G': 33,
    'H': 34,
    'I': 35,
    'J': 36,
    'K': 37,
    'L': 38,
    'M': 39,
    'N': 40,
    'O': 41,
    'P': 42,
    'Q': 43,
    'R': 44,
    'S': 45,
    'T': 46,
    'U': 47,
    'V': 48,
    'W': 49,
    'X': 50,
    'Y': 51,
    'Z': 52 
}

def parse_input(filepath):

    out = []

    f = open(filepath, 'r')
    
    while True:
        line = f.readline()
        if line == '': # EOF
            break
        if line[-1] == '\n': # line has newline
            line = line[:-1]
        out.append(line)
    
    f.close()

    return out


def tally_items_in_compartment(compartment):

    items = [0 for i in range(52)]
    
    for item in compartment:
        items[priorities[item] - 1] += 1

    return items


def compare_compartments(rucksack):

    half = len(rucksack) // 2
    
    comp1 = rucksack[:half]
    comp2 = rucksack[half:]

    print(comp1)
    print(comp2)

    comp1_contents = tally_items_in_compartment(comp1)
    comp2_contents = tally_items_in_compartment(comp2)

    priority = 0
    
    for i in range(52):
        if comp1_contents[i] > 0 and comp2_contents[i] > 0:
            priority = i + 1

    return priority


def sum_of_priorities(sack_list):

    sum = 0
    
    for sack in sack_list:
        sum += compare_compartments(sack)

    return sum


def main():

    sack_list = parse_input('input.txt')
    print(sum_of_priorities(sack_list))


main()