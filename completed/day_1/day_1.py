from copy import deepcopy


def max_cals(elf_cals_list):
    
    elf_total_list = []
    
    for elf in elf_cals_list:
        elf_total_list.append(sum(elf))

    return max(elf_total_list)


def top_three_cals(elf_cals_list):

    elf_total_cals = []

    for elf in elf_cals_list:
        elf_total_cals.append(sum(elf))

    elf_total_cals.sort()

    return sum(elf_total_cals[-3:])


def parse_input():

    out = []
    running_list = []

    f = open('input.txt', 'r')
    
    while True:
        line = f.readline()
        if line == '': # EOF
            if len(running_list) > 0:
                out.append(deepcopy(running_list))
                running_list.clear()
            break
        if line == '\n': # move on to the next elf
            out.append(deepcopy(running_list))
            running_list.clear()
            continue
        if line[-1] == '\n': # line has newline
            line = line[:-1]
        running_list.append(int(line))
    
    f.close()

    return out
    

print(top_three_cals(parse_input()))