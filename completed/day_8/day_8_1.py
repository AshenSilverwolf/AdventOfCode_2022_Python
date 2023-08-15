def parse_input(filepath):

    f = open(filepath, 'r')

    grid = []

    while True:
        line = f.readline()
        if line == '':
            break
        line = line.strip('\n')
        
        row = []
        for tree in line:
            row.append(int(tree))
        grid.append(row)

    f.close()

    return grid


def determine_visibility(r, c, row, col):

    target = row[c]
    s_row = len(row)
    s_col = len(col)

    # if tree is on outside
    if r == 0 or r == s_row - 1:
        return True
    if c == 0 or c == s_col - 1:
        return True

    # Visible from East
    east = row[c+1:]
    e_vis = True
    for tree in east:
        if tree >= target:
            e_vis = False
            break

    # Visible from South
    south = col[r+1:]
    s_vis = True
    for tree in south:
        if tree >= target:
            s_vis = False
            break

    # Visible from West
    west = row[:c]
    w_vis = True
    for tree in west:
        if tree >= target:
            w_vis = False
            break

    # Visible from North
    north = col[:r]
    n_vis = True
    for tree in north:
        if tree >= target:
            n_vis = False
            break

    # Return Visibility (True if any)
    return e_vis or s_vis or w_vis or n_vis


def main():

    grid = parse_input('d8_input.txt')

    counter = 0
    
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            is_visible = determine_visibility(i, j, grid[i], [row[j] for row in grid])
            if is_visible:
                counter += 1

    print(counter)

main()