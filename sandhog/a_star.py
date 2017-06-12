from collections import deque
from heapq import heapify, heappush, heappop
import operator
import numpy as np

state = np.array(
    [[
        u'grass', u'grass', u'grass', u'grass', u'grass', u'grass', u'grass',
        u'grass', u'grass'
    ], [
        u'grass', u'sand', u'sand', u'sand', u'sand', u'sand', u'sand',
        u'sand', u'grass'
    ], [
        u'grass', u'sand', u'grass', u'grass', u'grass', u'grass', u'grass',
        u'sand', u'grass'
    ], [
        u'sand', u'sand', u'grass', u'sand', u'grass', u'sand',
        u'grass/Agent_2', u'sand', u'sand'
    ], [
        u'sand', u'lapis_block', u'grass', u'grass', u'grass',
        u'grass/Agent_1', u'grass/Pig', u'lapis_block', u'sand'
    ], [
        u'sand', u'sand', u'grass', u'sand', u'grass', u'sand', u'grass',
        u'sand', u'sand'
    ], [
        u'grass', u'sand', u'grass', u'grass', u'grass', u'grass', u'grass',
        u'sand', u'grass'
    ], [
        u'grass', u'sand', u'sand', u'sand', u'sand', u'sand', u'sand',
        u'sand', u'grass'
    ], [
        u'grass', u'grass', u'grass', u'grass', u'grass', u'grass', u'grass',
        u'grass', u'grass'
    ]],
    dtype=object)


def a_star(start, goal, output_states=False):
    parent, cost = {}, {}
    frontier = []

    heapify(frontier)
    heappush(frontier, (0, start))
    parent[start] = None
    cost[start] = 0
    current = None

    while len(frontier) > 0:
        _, current = heappop(frontier)
        if current[1] == goal:
            break
        for nb in neighbors(current, state):
            ccost = 1
            new_cost = cost[current] + ccost
            if nb not in cost or new_cost < cost[nb]:
                cost[nb] = new_cost
                priority = new_cost + heuristic(goal, nb[1])
                heappush(frontier, (priority, nb))
                parent[nb] = current

    path = deque()
    c = cost[current]
    while current is not start:
        if output_states:
            path.appendleft(current)
        else:
            path.appendleft(current[2])
        current = parent[current]

    return path, c


def neighbors(pos, state):
    # up, right, down, left
    dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    result = []
    result.append(((pos[0] + 1) % 4, pos[1], "turn 1"))
    result.append(((pos[0] - 1) % 4, pos[1], "turn -1"))
    result.append((pos[0], tuple(map(operator.add, pos[1], dir[pos[0]])),
                   "move 1"))

    final_results = []
    for n in result:
        if (n[1][0] >= 0 and n[1][0] < state.shape[0] and n[1][1] >= 0 and
                n[1][1] < state.shape[1] and
                state[n[1][0], n[1][1]] != 'sand'):
            final_results.append(n)

    return final_results


def heuristic(a, b):
    (x1, y1) = (a[0], a[1])
    (x2, y2) = (b[0], b[1])
    return abs(x1 - x2) + abs(y1 - y2)
