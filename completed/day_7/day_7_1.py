def parse_input(filepath):

    f = open(filepath, 'r')

    root = {}
    cwd = root
    path = []
    mode = 'command'

    while True:

        last_pos = f.tell()
        line = f.readline()
    
        if line == '':
            break
        line = line.split('\n')[0]

        if mode == 'command':
            command = line[2:4]
            if command == 'cd':
                target_dir = line[5:]
                if target_dir == '/':
                    cwd = root
                elif target_dir == '..':
                    cwd = root
                    for step in path[:-1]:
                        cwd = cwd[step]
                    path = path[:-1]
                else:
                    path.append(target_dir)
                    cwd = cwd[target_dir]
            elif command == 'ls':
                mode = 'directory'
        elif mode == 'directory':
            if line[0] == '$':
                mode = 'command'
                f.seek(last_pos)
                continue
            dir_element = line.split(' ')
            if dir_element[0] == 'dir':
                cwd[dir_element[1]] = {}
            else:
                cwd[dir_element[1]] = dir_element[0]
    
    f.close()

    return root


def print_filesystem(file_system, depth):

    for key, value in file_system.items():
        if isinstance(value, dict):
            print('\t' * depth + '- ' + key + ' (dir)')
            print_filesystem(value, depth + 1)
        else:
            print('\t' * depth + '- ' + key + ' (file, size=' + value + ')')


def size_of_directory(directory):

    sum_size = 0
    
    for key, value in directory.items():
        if isinstance(value, dict):
            sum_size += size_of_directory(value)
        else:
            sum_size += int(value)

    return sum_size


def sum_size_of_qualifying_directories(file_system):

    sum = 0
    size = size_of_directory(file_system)
    sum += size if size < 100000 else 0

    for val in file_system.values():
        if isinstance(val, dict):
            sum += sum_size_of_qualifying_directories(val)

    return sum        


def main():

    file_system = parse_input('d7_input.txt')
    print_filesystem(file_system, 0)

    print(sum_size_of_qualifying_directories(file_system))


main()