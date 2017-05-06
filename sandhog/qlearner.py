#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Qlearner for AI project
"""

import numpy as np


def random_pair(start, end):
    """TODO: Docstring for random_pair.

    :start: (int) start for random number
    :end:   (int) end for random number
    :returns: pair for random numbers

    """
    return np.random.randint(start, end), np.random.randint(start, end)


def find_pos(state, obj):
    """TODO: Docstring for random_pair.

    :state
    :obj
    :returns: (x, y) position

    """
    for i in range(0, 4):
        for j in range(0, 4):
            if (state[i, j] == obj).all():
                return i, j


def init_grid():
    """TODO: Docstring for init_grid.

    :returns: state

    """
    state = np.zeros((9, 9, 5))

    state[rand_pair(2, 7)] = np.array([1, 0, 0, 0, 0])  # AI agent
    state[rand_pair(2, 7)] = np.array([0, 1, 0, 0, 0])  # Human agent
    state[rand_pair(2, 7)] = np.array([0, 0, 1, 0, 0])  # Pig

    # Initialize fences
    for i in [1, 7]:
        for j in range(1, 8):
            state[i, j] = np.array([0, 0, 0, 1, 0])
            if j != 4:
                state[j, i] = np.array([0, 0, 0, 1, 0])
    state[3, 3] = np.array([0, 0, 0, 1, 0])
    state[5, 3] = np.array([0, 0, 0, 1, 0])
    state[3, 5] = np.array([0, 0, 0, 1, 0])
    state[5, 5] = np.array([0, 0, 0, 1, 0])

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
