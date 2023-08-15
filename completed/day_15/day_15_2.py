"""Advent of Code 2022: Day 15 Pt 2
"""

from shapely import intersection, Point, LineString
# from itertools import product

class Sensor:

    """Sensor class represents a sensor's positions with pos: Point and it's range with range: int.
    """

    def __init__(self, p1, sensor_range):
        self.pos = Point(p1.x, p1.y)
        self.range = sensor_range

    def __repr__(self):
        return f'Sensor: {self.pos!r}, Range: {self.range}'

    def __str__(self):
        return f'Sensor {self.pos} has range {self.range}'

ROW_NUM = 2000000
BOUNDARY_P1 = Point(0,0)
BOUNDARY_P2 = Point(4000000,4000000)

def parse_input(filepath):

    """
    Returns a list of Sensor objects, and a set of Point objects representing the beacons. 
    These objects contain the coordinates of both the Sensor and the Beacon associated with it.
    """

    with open(filepath, 'r', encoding='utf-8') as f:

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
            sensor = Sensor(Point(sx, sy), manhattan_distance(Point(sx, sy), Point(bx, by)))
            sensors.append(sensor)
            beacons.add(Point(bx, by))

    return sensors

def manhattan_distance(p1, p2):

    """Returns the Manhattan Distance between two points.

    Returns:
        int: distance between the points
    """

    return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def run_logic(sensors):

    """Runs the logic for finding the missing beacon.

    Returns:
        Point: The Point representing the location of the missing beacon in the grid.
    """

    lines = set()
    intersections = set()

    for sensor in sensors:
        east = Point(sensor.pos.x + sensor.range + 1, sensor.pos.y)
        south = Point(sensor.pos.x, sensor.pos.y - sensor.range - 1)
        west = Point(sensor.pos.x - sensor.range - 1, sensor.pos.y)
        north = Point(sensor.pos.x, sensor.pos.y + sensor.range + 1)

        lines.add(LineString([west, north]))
        lines.add(LineString([west, south]))
        lines.add(LineString([east, north]))
        lines.add(LineString([east, south]))

    # Non-functional, replaces the lower nested for-loops
    # kinda want to get it working

    # intersections = {
    #     cross for cross in {
    #         intersection(l1, l2, grid_size=2)
    #         for l1, l2 in product(lines, lines.copy())
    #         if not l1.equals_exact(l2, 1e-6)
    #     }
    #     if isinstance(cross, Point)
    #     and (0 <= cross.x <= 4000000 and 0 <= cross.y <= 4000000)
    # }

    for l1 in lines:
        for l2 in lines:
            if l1.equals_exact(l2,1e-6):
                continue
            intersection_point = intersection(l1, l2, grid_size=1)
            if not isinstance(intersection_point, Point):
                continue
            within_bounds = (
                0 <= intersection_point.x <= 4000000
                and 0 <= intersection_point.y <= 4000000
            )
            if within_bounds:
                intersections.add(intersection_point)

    for point in intersections:
        covered = False
        for sensor in sensors:
            if manhattan_distance(point, sensor.pos) <= sensor.range:
                covered = True
                break
        if not covered:
            return point

    return None

def main():

    """Driver function.
    """

    sensors = parse_input('d15_input.txt')
    missing_point = run_logic(sensors)
    print(missing_point)
    print(missing_point.x * 4000000 + missing_point.y)

main()
