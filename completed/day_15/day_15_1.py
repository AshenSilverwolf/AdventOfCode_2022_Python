ROW_NUM = 2000000

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

    def dist(self, other):
        return abs(self.pos.x - other.pos.x) + abs(self.pos.y - other.pos.y)


class Sensor:

    def __init__(self, p1, p2):
        self.pos = Point(p1.x, p1.y)
        self.beacon = Point(p2.x, p2.y)

    def __repr__(self):
        return f'Sensor: {self.pos!r}, Beacon: {self.beacon!r}'

    def __str__(self):
        return f'Sensor {str(self.pos)} sees Beacon {str(self.beacon)}'


def parse_input(filepath):

    """
    Returns a list of Sensor objects, and a set of Point objects representing the beacons. 
    These objects contain the coordinates of both the Sensor and the Beacon associated with it.
    """

    f = open(filepath, 'r')

    sensors = []
    beacons = set()

    while True:
        line = f.readline()
        if line == '':
            break
        line = line.split('\n')[0]
        line = line.split('Sensor at ')[1]
        pair = line.split(': closest beacon is at ')
        sensor_coords = pair[0].split(', ')
        beacon_coords = pair[1].split(', ')
        sx, sy = int(sensor_coords[0][2:]), int(sensor_coords[1][2:])
        bx, by = int(beacon_coords[0][2:]), int(beacon_coords[1][2:])
        sensor = Sensor(Point(sx, sy), Point(bx, by))
        sensors.append(sensor)
        beacons.add(sensor.beacon)

    f.close()

    return sensors, beacons


def manhattan_distance(p1, p2):

    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def find_x_bounds_for_row(sensors):

    leftmost_sensor = sensors[0]
    rightmost_sensor = sensors[0]
    for curr_sensor in sensors:
        if curr_sensor.pos.x < leftmost_sensor.pos.x:
            leftmost_sensor = curr_sensor
        if curr_sensor.pos.x > rightmost_sensor.pos.x:
            rightmost_sensor = curr_sensor

    dist_ly = abs(leftmost_sensor.pos.y - ROW_NUM)
    dist_ry = abs(rightmost_sensor.pos.y - ROW_NUM)

    dist_lb = manhattan_distance(leftmost_sensor.pos, leftmost_sensor.beacon)
    dist_rb = manhattan_distance(rightmost_sensor.pos, rightmost_sensor.beacon)

    dist_lx = dist_lb - dist_ly
    dist_rx = dist_rb - dist_ry

    left_limit = leftmost_sensor.pos.x if dist_lx < 0 else leftmost_sensor.pos.x - dist_lx
    right_limit = rightmost_sensor.pos.x if dist_rx < 0 else rightmost_sensor.pos.x + dist_rx

    return left_limit, right_limit


def run_logic(sensors, beacons):

    """
    Returns the number of points excluded via their proximity to Sensors.

    dist_b = the distance between a Sensor and its associated Beacon.
    dist_y = the distance between a Sensor and the point directly above/below on ROW_NUM.
    dist_x = the remaining play that we have to exclude points with.
    If dist_x is negative, we know that the Sensor's influence doesn't reach to ROW_NUM.
    Otherwise, we exclude points spreading outward from Point(sensor.pos.x, ROW_NUM) for
        dist_x points to the left and the right.
    Do this for all sensors.
    Remove all beacons from the set of excluded points.
    Return the length of the set of excluded points.
    """

    excluded = set()

    left_limit, right_limit = find_x_bounds_for_row(sensors)
    for x in range(left_limit, right_limit+1):
        curr_point = Point(x, ROW_NUM)
        for sensor in sensors:
            if manhattan_distance(curr_point, sensor.pos) <= manhattan_distance(sensor.pos, sensor.beacon):
                excluded.add(curr_point)
                break

    for beacon in beacons:
        try:
            excluded.remove(beacon)
        except KeyError:
            pass

    return len(excluded)


def main():
    
    sensors, beacons = parse_input('d15_input.txt')
    for sensor in sensors:
        print(sensor)
    print()
    for beacon in beacons:
        print(f'Beacon {beacon}')
    print()

    num_excluded = run_logic(sensors, beacons)
    print(f'Number of excluded points = {num_excluded}')


main()
