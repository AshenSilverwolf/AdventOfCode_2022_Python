FILEPATH = 'd14_input.txt'


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash(str(self.x) + ',' + str(self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return '<object:Point> -> x: ' + str(self.x) + ', y: ' + str(self.y)

    def __str__(self):
        return str(self.x) + ', ' + str(self.y)


def points_between(p1, p2):

    """
    Returns the set of points between the two parameter points (inclusive).
    """

    if p1.x > p2.x:
        points = set([Point(i, p1.y) for i in range(p2.x, p1.x + 1)])
    elif p1.x < p2.x:
        points = set([Point(i, p1.y) for i in range(p1.x, p2.x + 1)])
    elif p1.y > p2.y:
        points = set([Point(p1.x, i) for i in range(p2.y, p1.y + 1)])
    elif p1.y < p2.y:
        points = set([Point(p1.x, i) for i in range(p1.y, p2.y + 1)])

    return points

 
def parse_input():

    """
    Returns the set of points within the cavern that contain rock.
    """

    f = open(FILEPATH, 'r')

    points = set()

    while True:
        line = f.readline()
        if line == '':
            break
        line = line.split('\n')[0]

        str_points = line.split(' -> ')
        str_points = [x.split(',') for x in str_points]
        given_points = [Point(int(x[0]), int(x[1])) for x in str_points]
        # generate all wall points
        for i in range(1, len(given_points)):
            points.update(points_between(given_points[i-1], given_points[i]))

    f.close()

    return points


def determine_boundaries(points):

    """
    Determines the X and Y boundaries of the visualization
    based on the min/max values of X and Y within the set of points.
    """

    xs = [point.x for point in points]
    ys = [point.y for point in points]
    
    min_x = min(xs)
    max_x = max(xs)

    max_y = max(ys)

    return min_x, max_x, 0, max_y


def visualize(rocks, sand):

    """
    Creates an ASCII text visualization of the boundaries defined by the problem.
    """

    chars = {
        'rock': '#',
        'air': '.',
        'source': '+',
        'sand': 'o'
    }
    
    min_x, max_x, min_y, max_y = determine_boundaries(rocks)
    source = Point(500, 0)

    left_x = list(str(min_x))
    right_x = list(str(max_x))
    spawn = list('500')
    spacer_const = len(str(max_y))
    spacer = ' ' * (spacer_const + 1)
    
    to_print = []

    # key X markers
    for i in range(3):
        curr = '' + spacer
        for j in range(min_x, max_x + 1):
            if j == min_x:
                curr += left_x[i]
            elif j == max_x:
                curr += right_x[i]
            elif j == 500:
                curr += spawn[i]
            else:
                curr += ' '

        to_print.append(curr)

    # Y markers & Rows
    for i in range(max_y + 1):
        curr = ' ' * (spacer_const - len(str(i))) + str(i) + ' '
        for j in range(min_x, max_x + 1):
            if Point(j, i) == source:
                curr += chars['source']
            elif Point(j, i) in rocks:
                curr += chars['rock']
            elif Point(j, i) in sand:
                curr += chars['sand']
            else:
                curr += chars['air']

        to_print.append(curr)

    for line in to_print:
        print(line)

    return


def drop_grain_of_sand(points):

    """
    Runs the game logic for dropping a single grain of sand down the cavern.
    Returns the point where the grain of sand rests.
    If the grain falls below the y-limit, returns None.
    """

    prev = Point(500, -1)
    curr = Point(500, 0)
    limit = max([point.y for point in points])
    
    while prev != curr:
        if curr.y > limit:
            return None

        prev.x, prev.y = curr.x, curr.y
        if Point(curr.x, curr.y+1) not in points:
            curr.x, curr.y = curr.x, curr.y+1
        elif Point(curr.x-1, curr.y+1) not in points:
            curr.x, curr.y = curr.x-1, curr.y+1
        elif Point(curr.x+1, curr.y+1) not in points:
            curr.x, curr.y = curr.x+1, curr.y+1

    return curr


def run_simulation(rocks):

    """
    Runs the game logic, dropping a grain of sand for every iteration.
    Stops once a grain of sand exceeds the boundary.
    Returns the number of grains of sand that got locked in before falling.
    """

    min_x, max_x, min_y, max_y = determine_boundaries(rocks)
    sand = set()
    count = 0

    while True:
        grain = drop_grain_of_sand(rocks | sand)
        if grain is None:
            break

        count += 1
        sand.add(grain)

    visualize(rocks, sand)
    
    return count


def main():

    rocks = parse_input()
    print('There are ' + str(len(rocks)) + ' points in this set.')
    min_x, max_x, min_y, max_y = determine_boundaries(rocks)
    print('X Bounds: ' + str(min_x) + ' - ' + str(max_x))
    print('Y Bounds: ' + str(min_y) + ' - ' + str(max_y))
    print()

    num_grains = run_simulation(rocks)
    print()
    print(num_grains)
    
    return


main()
