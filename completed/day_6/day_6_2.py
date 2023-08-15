def parse_input(filepath):

    f = open(filepath, 'r')

    input = f.readline()

    return input


def find_marker(input):

    for i in range(len(input) - 13):
        j = i + 14
        block = input[i:j]
        dict = {}
        for c in block:
            try: 
                if dict[c] > 0:
                    break
            except KeyError:
                dict[c] = 1

        if len(dict) == 14:
            return j


def main():

    input = parse_input('d6_input.txt')
    
    end_of_marker_index = find_marker(input)

    print(end_of_marker_index)


main()