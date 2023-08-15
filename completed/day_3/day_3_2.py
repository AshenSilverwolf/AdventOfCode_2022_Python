from copy import deepcopy

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
    current_group = []
    
    f = open(filepath, 'r')
    
    while True:
        
        line = f.readline()
        if line == '':
            break
        
        for i in range(2):
            current_group.append(line)
            line = f.readline()
        current_group.append(line)
        
        for i in range(3):
            if current_group[i][-1] == '\n':
                current_group[i] = current_group[i][:-1]
        
        out.append(deepcopy(current_group))
        current_group.clear()
    
    f.close()

    return out


def tally_items_in_compartment(compartment):

    items = [0 for i in range(52)]
    
    for item in compartment:
        items[priorities[item] - 1] += 1

    return items


def check_for_badge(set):

    set_contents = []
    
    for sack in set:
        set_contents.append(tally_items_in_compartment(sack))

    priority = -1
    
    for i in range(len(set_contents[0])):
        if set_contents[0][i] > 0 and set_contents[1][i] > 0 and set_contents[2][i] > 0:
            priority = i + 1

    return priority


def sum_of_priorities(set_list):

    sum = 0
    
    for set in set_list:
        sum += check_for_badge(set)

    return sum


def main():

    set_list = parse_input('input.txt')
    print(sum_of_priorities(set_list))
        

main()