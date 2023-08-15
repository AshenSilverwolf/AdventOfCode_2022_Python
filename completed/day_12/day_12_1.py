INFINITY = 1000000
ROW_INCR = 8

class Graph:

    def __init__(self):
        self.Vertices = []
        self.Edges = {}


# https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#cite_note-chen_07-20
class MinPriorityQueue:

    def __init__(self):
        self.q = []
        self.p = {}

    
    def is_empty(self):
        return len(self.q) == 0

    
    def insert_with_priority(self, item, priority):
        self.p[item] = priority
        if self.is_empty():
            self.q.append(item)
            return

        for index, element in enumerate(self.q):
            if priority < self.p[element]:
                self.q.insert(index, item)
                return

        self.q.append(item)

    
    def extract_min(self):
        min_p_item = self.q.pop(0)
        del self.p[min_p_item]
        return min_p_item

    
    def decrease_priority(self, item, new_priority):
        if new_priority >= self.p[item]:
            return
        
        try:
            self.q.remove(item)
        except ValueError:
            # print('attempting to remove ' + str(item))
            pass
        
        self.insert_with_priority(item, new_priority)


def parse_input(filepath):

    f = open(filepath, 'r')

    height_map = []

    while True:
        line = f.readline()
        if line == '':
            break
        line = line.split('\n')[0]

        curr_row = []

        for c in line:
            curr_row.append(c)

        height_map.append(curr_row)

    f.close()

    # Convert height_map[][] to Graph

    per_row = len(height_map[0])
    graph = Graph()
    a = 0
    for i, _ in enumerate(height_map):
        for j, _ in enumerate(height_map[i]):
            a += 1
            if height_map[i][j] == 'S':
                source = a
                height_map[i][j] = 0
            elif height_map[i][j] == 'E':
                target = a
                height_map[i][j] = 25
            else:
                height_map[i][j] = ord(height_map[i][j]) - 97

    a = 0
    for i, _ in enumerate(height_map):
        for j, _ in enumerate(height_map[i]):
            a += 1
            graph.Vertices.append(a)

            try:
                if height_map[i + 1][j] - height_map[i][j] <= 1:
                    graph.Edges[a, a + per_row] = 1
            except IndexError:
                pass

            try:
                if height_map[i][j + 1] - height_map[i][j] <= 1:
                    graph.Edges[a, a + 1] = 1
            except IndexError:
                pass

            try:
                in_bounds = i - 1 >= 0
                height_difference = height_map[i - 1][j] - height_map[i][j]
                if in_bounds and height_difference <= 1:
                    graph.Edges[a, a - per_row] = 1
            except IndexError:
                pass

            try:
                in_bounds = j - 1 >= 0
                height_difference = height_map[i][j - 1] - height_map[i][j]
                if in_bounds and height_difference <= 1:
                    graph.Edges[a, a - 1] = 1
            except IndexError:
                pass

    return graph, source, target


# Dijkstra's
# A*
# RIPA
def reconstruct_path(prev, current):  # using Dijkstra's

    total_path = [current]
    while current in prev.keys():
        current = prev[current]
        total_path.insert(0, current)

    return total_path


def A_Star(graph, source, target, heuristic):

    openSet = MinPriorityQueue()
    prev = {}
    gScore = {}
    fScore = {}
    
    for node in graph.Vertices:
        gScore[node] = INFINITY
        fScore[node] = INFINITY
    gScore[source] = 0
    fScore[source] = heuristic(source, target)
    
    openSet.insert_with_priority(source, fScore[source])

    while not openSet.is_empty():
        current = openSet.extract_min()
        if current == target:
            return reconstruct_path(prev, current)

        neighbors = []
        for e in graph.Edges.keys():
            if e[0] == current:
                neighbors.append(e[1])
        for neighbor in neighbors:
            tentative_gScore = gScore[current] + graph.Edges[(current, neighbor)]
            if tentative_gScore < gScore[neighbor]:
                prev[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = tentative_gScore + heuristic(neighbor, target)
                if neighbor not in openSet.q:
                    openSet.insert_with_priority(neighbor, fScore[neighbor])

    return None


def main():

    graph, source, target = parse_input('d12_input.txt')
    heuristic = lambda c, g: abs(g // ROW_INCR - c // ROW_INCR) + abs(g % ROW_INCR - c % ROW_INCR)
    final_path = A_Star(graph, source, target, heuristic)
    if final_path is None:
        print('Failure')
    else:
        print(len(final_path) - 1)


main()
