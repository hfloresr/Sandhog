#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Qlearner for AI project
"""

import numpy as np


def random_pair(s, e):
    """TODO: Docstring for random_pair.
    :returns: TODO

    """
    return np.random.randint(s, e), np.random.randint(s, e)


def find_pos(state, obj):
    for i in range(0, 4):
        for j in range(0, 4):
            if (state[i, j] == obj).all():
                return i, j


def init_grid():
    """TODO: Docstring for init_grid.

    :arg1: TODO
    :returns: TODO

    """
    state = np.zeros((4, 4, 5))

    state[rand_pair(0, 4)] = np.array([1, 0, 0, 0, 0])  # AI agent
    state[rand_pair(0, 4)] = np.array([0, 1, 0, 0, 0])  # Human agent
    state[rand_pair(0, 4)] = np.array([0, 0, 1, 0, 0])  # Pig

    # Initialize fences
    state[3, 3] = np.array([0, 0, 0, 1, 0])
    state[5, 3] = np.array([0, 0, 0, 1, 0])
    state[5, 3] = np.array([0, 0, 0, 1, 0])
    state[5, 3] = np.array([0, 0, 0, 1, 0])

    # Initialize exits
    state[4, 1] = np.array([0, 0, 0, 0, 1])
    state[4, 7] = np.array([0, 0, 0, 0, 1])

    # Find positions
    a = find_pos(state, np.array([1, 0, 0, 0, 0]))
    h = find_pos(state, np.array([0, 1, 0, 0, 0]))
    p = find_pos(state, np.array([0, 0, 1, 0, 0]))
    f = find_pos(state, np.array([0, 0, 0, 1, 0]))
    e = find_pos(state, np.array([0, 0, 0, 0, 1]))

    return state
