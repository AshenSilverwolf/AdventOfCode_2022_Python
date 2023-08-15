INFINITY = 1000000
ROW_INCR = 77


class Graph:

    def __init__(self):
        self.Vertices = []
        self.Edges = {}


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

    sources = []

    per_row = len(height_map[0])
    graph = Graph()
    a = 0
    for i, _ in enumerate(height_map):
        for j, _ in enumerate(height_map[i]):
            a += 1
            if height_map[i][j] == 'S':
                height_map[i][j] = 'a'

            if height_map[i][j] == 'E':
                height_map[i][j] = 'z'
                target = a

            height_map[i][j] = ord(height_map[i][j]) - 97

            if height_map[i][j] == 0:
                sources.append(a)

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

    return graph, sources, target


def reconstruct_path(prev, current):

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
            tentative_gScore = gScore[current] + graph.Edges[(current,
                                                              neighbor)]
            if tentative_gScore < gScore[neighbor]:
                prev[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = tentative_gScore + heuristic(
                    neighbor, target)
                if neighbor not in openSet.q:
                    openSet.insert_with_priority(neighbor, fScore[neighbor])

    return None


def flood_fill(graph, source):

    # touch every node possible
    # return list of nodes
    Q = [source]
    excluded = set()
    excluded.add(source)

    while len(Q) > 0:
        curr = Q.pop(0)
        neighbors = []
        for e in graph.Edges.keys():
            if e[0] == curr:
                neighbors.append(e[1])
        for neighbor in neighbors:
            if neighbor not in excluded:
                Q.append(neighbor)
                excluded.add(neighbor)

    return excluded


def remove_isolated_groups(graph, sources, target):

    

    '''
    - It takes way too long to A* from every possible source node.
    - We can use flood-fill to see if we can even get from source to target.
    - If we can't, then every node we hit is part of an isolated subgraph
      that we can remove.
    - If we can get to the target, we just leave it alone.
    
    - The unfortunate part of this method is that if our source node finds
      the target, we can't remove anything. 
    - Some edges are only one-way, where things can get in but not out, so
      we can't guarantee that everything a valid source touches is safe.
    - However, we CAN guarantee that everything an invalid source touches
      can be removed, so we do.
    '''

    while len(sources) > 0:
        b_len = len(graph.Vertices)
        curr = sources.pop(0)
        flood = flood_fill(graph, curr)
        if target in flood:
            continue
        graph.Vertices = [x for x in graph.Vertices if x not in flood]
        graph.Edges = dict([(k, v) for k, v in graph.Edges.items() if k[0] not in flood and k[1] not in flood])
        sources = [x for x in sources if x not in flood]
        a_len = len(graph.Vertices)
        nodes_removed = b_len - a_len
        print(str(nodes_removed) + ' Nodes Removed.')
    
    return graph
        


def main():

    # https://stackoverflow.com/questions/1348783/finding-all-disconnected-subgraphs-in-a-graph
    # https://en.wikipedia.org/wiki/Flood_fill

    graph, sources, target = parse_input('d12_input.txt')
    heuristic = lambda c, g: abs(g // ROW_INCR - c // ROW_INCR) + abs(g % ROW_INCR - c % ROW_INCR)
    print('Removing Isolated Groups...')
    graph = remove_isolated_groups(graph, sources, target)
    sources = [x for x in sources if x in graph.Vertices]
    print('Finding Shortest Path...')
    paths = []
    for source in sources:
        curr_path = A_Star(graph, source, target, heuristic)
        paths.append(curr_path)
        print(str(len(curr_path) - 1) + ' steps from ' + str(source))
    paths = [(len(x)-1) for x in paths if x is not None]
    print(min(paths))


main()
