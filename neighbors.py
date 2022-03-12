from node import Node
import operator
from cost import cost_calc


def find_neighbors(x, y, g_cost, goals):
    """Finds neighboring nodes"""
    neighbors = []
    g = g_cost + 1
    positions = [[x, y - 1], [x - 1, y], [x + 1, y], [x, y + 1]]

    for position in positions:
        h_cost, f_cost = cost_calc(goals[1].x, goals[1].y, position[0], position[1], g_cost)
        position = Node(x=position[0], y=position[1], old_x=x, old_y=y, g_cost=g, h_cost=h_cost, f_cost=f_cost)
        neighbors.append(position)

    neighbors.sort(key=operator.attrgetter('h_cost'))
    neighbors.sort(key=operator.attrgetter('f_cost'))

    return neighbors
