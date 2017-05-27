#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import ENV_AGENT_NAMES, ENV_TARGET_NAMES
from evaluation import PigChaseEvaluator
from environment import PigChaseSymoblicStateBuilder
from agent import PigChaseChallengeAgent, FocusedAgent
from malmopy.visualization import ConsoleVisualizer



if __name__ == '__main__':
    clients = [('127.0.0.1', 10000), ('127.0.0.1', 10001)]
    builder = PigChaseSymbolicStateBuilder()
    agent = FocusedAgent(ENV_AGENT_NAMES[1], ENV_TARGET_NAMES[0])
    eval = PigChaseEvaluator(clients, agent, agent, builder)
    eval.run()
    eval.save('astar_exp', 'astar_results.json')
