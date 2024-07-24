class Node():
    def __init__(self, cost, coords, portal=False, portal_dest=None):
        self.cost = cost
        self.coords = coords
        self.portal = portal
        self.portal_dest = portal_dest


class Pathing:
    def __init__(self, rows, columns, pairs):
        self.end = (0, columns)
        self.map = []
        for i in range(rows + 1):
            row = []
            for j in range(columns + 1):
                coords = (i, j)
                portal = False
                portal_dest = None

                for pair in pairs:
                    if coords == pair[0]:
                        portal = True
                        portal_dest = pair[1]
                        break

                cost = self.calculate_cost(coords, self.end)
                node = Node(cost, coords, portal, portal_dest)

                row.append(node)

            self.map.append(row)

    def calculate_cost(self, current, end):
        return abs(end[0] - current[0]) + abs(end[1] - current[1])

    def find_paths(self):
        end = (0, len(self.map[0]) - 1)
        start = self.map[len(self.map) - 1][0]
        queue = [start]
        path_count = 0
        while len(queue) != 0:
            current = queue.pop(0)
            if current.cost == 0:
                path_count += 1
                continue
            queue.extend(self.find_all_neighbors(current, end))

        return path_count


    def find_all_neighbors(self, current, end):
        pos_nodes = []
        best_cost = float('inf')
        if current.portal:
            newNode = self.map[current.portal_dest[0]][current.portal_dest[1]]
            pos_nodes.append(newNode)
            best_cost = newNode.cost
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for i, j in directions:
            y = current.coords[0]
            x = current.coords[1]
            if (y - i) < 0 or (y - i) >= len(self.map) or (x - j) < 0 or (x - j) >= len(self.map[i]):
                continue
            newNode = self.map[y - i][x - j]
            if newNode.cost < best_cost and newNode.cost < current.cost:
                pos_nodes.clear()
                pos_nodes.append(newNode)
                best_cost = newNode.cost

            elif newNode.cost == best_cost and newNode.cost < current.cost:
                pos_nodes.append(newNode)
        return pos_nodes
