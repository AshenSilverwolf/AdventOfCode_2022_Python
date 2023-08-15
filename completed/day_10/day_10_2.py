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


def render(display, x_reg, cycle):

    r = 0
    temp = cycle
    while temp > 40:
        r += 1
        temp -= 40

    c = (temp - 1) % 40

    sprite = [x_reg-1, x_reg, x_reg+1]
    pixel = (cycle - 1) % 40
    
    if pixel in sprite:
        display[r][c] = '#'

    return display


def run_commands(commands):

    crt_display = [['.' for i in range(40)] for j in range (6)]
    
    x_register = 1
    cycle = 1
    command_counter = 0
    adding = False
    num_commands = len(commands)
    
    while command_counter < num_commands:
        command, value = commands[command_counter]
        
        crt_display = render(crt_display, x_register, cycle)
        
        if command == 'noop':
            command_counter += 1
        elif command == 'addx':
            if adding:
                x_register += value
                command_counter += 1
                adding = False
            else:
                adding = True
        cycle += 1

    return crt_display


def main():

    commands = parse_input('d10_input.txt')

    display = run_commands(commands)
    
    for i in range(len(display)):
        print(''.join(display[i]))


main()