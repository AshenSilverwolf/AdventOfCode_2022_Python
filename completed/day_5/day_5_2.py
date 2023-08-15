def create_stacks(file):

    f = file

    output_list = []

    line = f.readline()
    i = 0
    while True:
        block = line[i * 4 : i * 4 + 4]
        i += 1
        if block[3] == '\n':
            break

    num_stacks = i
    for i in range(num_stacks):
        output_list.append([])
    
    while True:
        for i in range(num_stacks):
            block = line[i * 4 : i * 4 + 4]
            crate = block[1]
            if (crate != ' ' and crate != '\n'):
                output_list[i].insert(0, crate)

        line = f.readline()
        if not line[1].isalpha():
            f.readline()
            break

    return output_list


def create_commands(file):

    f = file

    output_list = []

    while True:

        line = f.readline()
        if line == '':
            break
        line = line.split('\n')[0]
        line = line[5:] # remove 'move '
        from_split = line.split(' from ')
        to_split = from_split[1].split(' to ')
        params = [int(from_split[0]), int(to_split[0])-1, int(to_split[1])-1]
        output_list.append(params)

    return output_list


def parse_input(filepath):

    f = open(filepath, 'r')

    stacks = create_stacks(f)

    commands = create_commands(f)
    
    f.close()

    return stacks, commands


def move(command, stacks):

    count = command[0]
    from_stack = command[1]
    to_stack = command[2]
    
    stacks[to_stack] += stacks[from_stack][-count:]
    stacks[from_stack] = stacks[from_stack][:-count]

    return stacks


def perform_work(stacks, commands):

    for command in commands:
        stacks = move(command, stacks)

    tops = ''

    for i in range(len(stacks)):
        tops += stacks[i].pop()
    
    return tops


def main():

    stacks, commands = parse_input('d5_input.txt')

    tops = perform_work(stacks, commands)
    print(tops)


main()