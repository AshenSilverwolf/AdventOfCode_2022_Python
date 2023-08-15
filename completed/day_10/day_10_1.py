def parse_input(filepath):

    f = open(filepath, 'r')

    commands_list = []

    while True:
        line = f.readline()
        if line == '':
            break
        line = line.split('\n')[0]
        line_split = line.split(' ')
        if line_split[0] == 'noop':
            commands_list.append((line_split[0], 0))
        elif line_split[0] == 'addx':
            commands_list.append((line_split[0], int(line_split[1])))

    f.close()

    return commands_list


def run_commands(commands):

    key_cycles = [20, 60, 100, 140, 180, 220]
    sum_signals = 0
    
    x_register = 1
    cycle = 1
    command_counter = 0
    adding = False
    num_commands = len(commands)
    
    while command_counter < num_commands:
        command, value = commands[command_counter]

        if cycle in key_cycles:
            signal_strength = cycle * x_register
            print(cycle, x_register, signal_strength)
            sum_signals += signal_strength
        
        if adding:
            x_register += value
            command_counter += 1
            cycle += 1
            adding = False
            continue
        
        if command == 'noop':
            # noop
            command_counter += 1
        elif command == 'addx':
            # addx
            adding = True

        cycle += 1

    return sum_signals


def main():

    commands = parse_input('d10_input.txt')
    # print(commands)

    sum_signals = run_commands(commands)
    print(sum_signals)


main()