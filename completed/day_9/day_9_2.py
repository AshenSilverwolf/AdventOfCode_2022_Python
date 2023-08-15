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


def move(head_pos, direction):

    head_x, head_y = head_pos[0], head_pos[1]

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

    return (head_x, head_y)


def follow(leader, follower):

    lead_x = leader[0]
    lead_y = leader[1]
    follow_x = follower[0]
    follow_y = follower[1]
    
    dif_x = lead_x - follow_x
    dif_y = lead_y - follow_y

    if abs(dif_x) <= 1 and abs(dif_y) <= 1:
        return (follow_x, follow_y)

    if dif_x > 0 and dif_y == 0:
        follow_x += 1
    if dif_x < 0 and dif_y == 0:
        follow_x -= 1
    if dif_x == 0 and dif_y > 0:
        follow_y += 1
    if dif_x == 0 and dif_y < 0:
        follow_y -= 1
    if dif_x > 0 and dif_y > 0:
        follow_x += 1
        follow_y += 1
    if dif_x < 0 and dif_y > 0:
        follow_x -= 1
        follow_y += 1
    if dif_x < 0 and dif_y < 0:
        follow_x -= 1
        follow_y -= 1
    if dif_x > 0 and dif_y < 0:
        follow_x += 1
        follow_y -= 1

    return (follow_x, follow_y)


def process_commands(commands_list):

    knots = [(0, 0) for i in range(10)]

    tail_visited = {(0, 0)}

    for command in commands_list:
        direction, distance = command[0], command[1]
        for i in range(distance):
            knots[0] = move(knots[0], direction)
            for i in range(1, 10):
                knots[i] = follow(knots[i-1], knots[i])
            tail_visited.add(knots[9])

    return len(tail_visited)


def main():

    commands_list = parse_input('d9_input.txt')

    tail_visited = process_commands(commands_list)
    print(tail_visited)


main()