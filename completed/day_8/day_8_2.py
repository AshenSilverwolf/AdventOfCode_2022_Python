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


def determine_visibility_score(r, c, row, col):

    target = row[c]

    # Visible from East
    east = row[c+1:]
    e_vis = 0
    for tree in east:
        e_vis += 1
        if tree >= target:
            break

    # Visible from South
    south = col[r+1:]
    s_vis = 0
    for tree in south:
        s_vis += 1
        if tree >= target:
            break

    # Visible from West
    west = row[:c]
    west.reverse()
    w_vis = 0
    for tree in west:
        w_vis += 1
        if tree >= target:
            break

    # Visible from North
    north = col[:r]
    north.reverse()
    n_vis = 0
    for tree in north:
        n_vis += 1
        if tree >= target:
            break

    # Return Visibility (True if any)
    return e_vis * s_vis * w_vis * n_vis


def main():

    grid = parse_input('d8_input.txt')

    max_score = 0
    
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            vis_score = determine_visibility_score(i, j, grid[i], [row[j] for row in grid])
            max_score = max(max_score, vis_score)

    print(max_score)

main()