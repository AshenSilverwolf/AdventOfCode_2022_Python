def parse_input(filepath):

    pairs_list = []
    curr_pair = []
    
    f = open(filepath, 'r')
    
    while True:

        line = f.readline()
        if line == '':
            break
        line = line.split('\n')

        # separate the elves
        pair = line[0].split(',')
        
        # separate the ranges into start/end
        for section in pair:
            range_split = section.split('-')
            curr_pair.append([int(range_split[0]), int(range_split[1])])
        start = min(curr_pair[0][0], curr_pair[1][0])
        end = max(curr_pair[0][1], curr_pair[1][1])
        
        # generate generic lists of #/_ based on sections covered
        for i in range(2):
            for j in range(2):
                curr_pair[i][j] = int(curr_pair[i][j]) - start
        end -= start
        start = 0

        overlap = []
        in_range = lambda x, i, j: x >= i and x <= j
        for i in range(end-start+1):
            if in_range(i, curr_pair[0][0], curr_pair[0][1]) and in_range(i, curr_pair[1][0], curr_pair[1][1]):
                overlap.append('+')
            elif in_range(i, curr_pair[0][0], curr_pair[0][1]):
                overlap.append('-')
            elif in_range(i, curr_pair[1][0], curr_pair[1][1]):
                overlap.append('|')
            else:
                overlap.append(' ')
        
        pairs_list.append(''.join(overlap))

        curr_pair.clear()
        
    f.close()

    return pairs_list


def is_super(assignment):

    count = [0 for i in range(3)]
    
    for c in assignment:
        match c:
            case ' ':
                continue
            case '-':
                count[1] += 1
            case '|':
                count[2] += 1
            case '+':
                count[0] += 1
            case _:
                print('huh')

    if not count[0] > 0:
        return False
    elif count[1] > 0 and count[2] > 0:
        return False
    
    return True


def main():

    count = 0
    pairs_list = parse_input('input.txt')
    
    for pair in pairs_list:
        if is_super(pair):
            count += 1

    print(count)


main()