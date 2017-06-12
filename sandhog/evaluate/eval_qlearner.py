#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import ENV_AGENT_NAMES
from evaluation import PigChaseEvaluator
from malmopy.agent import TemporalMemory, LinearEpsilonGreedyExplorer
from malmopy.environment.malmo import MalmoALEStateBuilder
from agent import PigChaseChallengeAgent, PigChaseQLearnerAgent
from malmopy.visualization import ConsoleVisualizer
from malmopy.model.chainer import QNeuralNetwork, ReducedDQNChain



if __name__ == '__main__':
    device = -1
    nb_actions = 3
    visualizer = ConsoleVisualizer()

    clients = [('127.0.0.1', 10000), ('127.0.0.1', 10001)]
    memory = TemporalMemory(100000, (18, 18))
    chain = ReducedDQNChain((memory.history_length, 18, 18), nb_actions)
    target_chain = ReducedDQNChain((memory.history_length, 18, 18), nb_actions)
    model = QNeuralNetwork(chain, target_chain, device)
    explorer = LinearEpsilonGreedyExplorer(0.6, 0.1, 1000000)
    agent = PigChaseQLearnerAgent(ENV_AGENT_NAMES[1], nb_actions,
                                  model, memory, 0.99, 32, 50000,
                                  explorer=explorer, visualizer=visualizer)

    #builder = MalmoALEStateBuilder()
    builder = PigChaseTopDownStateBuilder(True)
    eval = PigChaseEvaluator(clients, agent, agent, builder)
    eval.run()
    eval.save('qlearner_exp', 'qlearner_results.json')
