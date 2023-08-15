def parse_input(filepath):

    f = open(filepath, 'r')

    commands_list = []

    while True:
        line = f.readline()
        if line == '':
            break
        line = line.strip('\n')

        command = line.split(' ')
        direction = command[0]
        distance = int(command[1])

        commands_list.append((direction, distance))

    f.close()

    return commands_list


def move(head_pos, tail_pos, direction):

    head_x, head_y = head_pos[0], head_pos[1]
    tail_x, tail_y = tail_pos[0], tail_pos[1]

    if direction == 'R':
        head_x += 1
    elif direction == 'D':
        head_y -= 1
    elif direction == 'L':
        head_x -= 1
    elif direction == 'U':
        head_y += 1
    else:
        print('huh?')

    dif_x = head_x - tail_x
    dif_y = head_y - tail_y

    if abs(dif_x) <= 1 and abs(dif_y) <= 1:
        return (head_x, head_y), (tail_x, tail_y)

    if dif_x > 0 and dif_y == 0:
        tail_x += 1
    if dif_x < 0 and dif_y == 0:
        tail_x -= 1
    if dif_x == 0 and dif_y > 0:
        tail_y += 1
    if dif_x == 0 and dif_y < 0:
        tail_y -= 1
    if dif_x > 0 and dif_y > 0:
        tail_x += 1
        tail_y += 1
    if dif_x < 0 and dif_y > 0:
        tail_x -= 1
        tail_y += 1
    if dif_x < 0 and dif_y < 0:
        tail_x -= 1
        tail_y -= 1
    if dif_x > 0 and dif_y < 0:
        tail_x += 1
        tail_y -= 1

    return (head_x, head_y), (tail_x, tail_y)


def process_commands(commands_list):

    tail_visited = {(0, 0)}

    head_pos = (0, 0)
    tail_pos = (0, 0)

    for command in commands_list:
        direction, distance = command[0], command[1]
        for i in range(distance):
            head_pos, tail_pos = move(head_pos, tail_pos, direction)
            tail_visited.add(tail_pos)

    print(tail_visited)
    return len(tail_visited)


def main():

    commands_list = parse_input('d9_input.txt')
    print(commands_list)

    tail_visited = process_commands(commands_list)
    print(tail_visited)


main()