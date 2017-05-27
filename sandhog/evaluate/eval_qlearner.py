#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import ENV_AGENT_NAMES
from evaluation import PigChaseEvaluator
from malmopy.agent import TemporalMemory, LinearEpsilonGreedyExplorer
from malmopy.environment.malmo import MalmoALEStateBuilder
from agent import PigChaseChallengeAgent, PigChaseQLearnerAgent
from malmopy.model.cntk import QNeuralNetwork
from malmopy.visualization import ConsoleVisualizer



if __name__ == '__main__':
    device = -1
    nb_actions = 3
    visualizer = ConsoleVisualizer()

    clients = [('127.0.0.1', 10000), ('127.0.0.1', 10001)]
    memory = TemporalMemory(100000, (84, 84))

    model = QNeuralNetwork((memory.history_length, 84, 84), nb_actions, device)
    explorer = LinearEpsilonGreedyExplorer(1, 0.1, 1000000)
    agent = PigChaseQLearnerAgent(ENV_AGENT_NAMES[1], nb_actions,
                                  model, memory, 0.99, 32, 50000,
                                  explorer=explorer, visualizer=visualizer)

    builder = MalmoALEStateBuilder()
    eval = PigChaseEvaluator(clients, agent, agent, builder)
    eval.run()

    eval.save('qlearner', 'qlearner_results.json')
