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


def size_of_all_directories(file_system):

    sizes = [size_of_directory(file_system)]

    for val in file_system.values():
        if isinstance(val, dict):
            sizes += size_of_all_directories(val)

    return sizes


def find_directory_suitable_for_deletion(file_system):

    total_disk_space = 70000000
    required_disk_space = 30000000
    used_disk_space = size_of_directory(file_system)
    unused_disk_space = total_disk_space - used_disk_space
    target = abs(required_disk_space - unused_disk_space)
    
    list_sizes = size_of_all_directories(file_system)
    min = total_disk_space
    
    for dir_size in list_sizes:
        if dir_size < target:
            continue

        min = dir_size if dir_size < min else min

    return min


def main():

    file_system = parse_input('d7_input.txt')
    print_filesystem(file_system, 0)

    # print(size_of_all_directories(file_system))
    print(find_directory_suitable_for_deletion (file_system))


main()