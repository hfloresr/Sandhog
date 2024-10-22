
import numpy as np
import os
import sys

from argparse import ArgumentParser
from datetime import datetime
from os import path
from threading import Thread, active_count
from time import sleep

from malmopy.agent import RandomAgent
from SandhogAgent import SandhogAgent
try:
    from malmopy.visualization.tensorboard import TensorboardVisualizer
    from malmopy.visualization.tensorboard.cntk import CntkConverter
except ImportError:
    print('Cannot import tensorboard, using ConsoleVisualizer.')
    from malmopy.visualization import ConsoleVisualizer

from common import parse_clients_args, visualize_training, ENV_AGENT_NAMES, ENV_TARGET_NAMES
from agent import PigChaseChallengeAgent, FocusedAgent
from environment import PigChaseEnvironment, PigChaseSymbolicStateBuilder

# Enforce path
sys.path.insert(0, os.getcwd())
sys.path.insert(1, os.path.join(os.path.pardir, os.getcwd()))

BASELINES_FOLDER = 'results/sandhog_baselines/pig_chase/%s/%s'
EPOCH_SIZE = 100


def agent_factory(name, role, baseline_agent, clients, max_epochs,
                  logdir, visualizer):

    assert len(clients) >= 2, 'Not enough clients (need at least 2)'
    clients = parse_clients_args(clients)

    builder = PigChaseSymbolicStateBuilder()
    env = PigChaseEnvironment(clients, builder, role=role,
                              randomize_positions=True)

    if role == 0:
        agent = PigChaseChallengeAgent(name)

        if type(agent.current_agent) == RandomAgent:
            agent_type = PigChaseEnvironment.AGENT_TYPE_1
        else:
            agent_type = PigChaseEnvironment.AGENT_TYPE_2
        obs = env.reset(agent_type)

        reward = 0
        agent_done = False

        while True:

            # select an action
            action = agent.act(obs, reward, agent_done, is_training=True)

            # reset if needed
            if env.done:
                if type(agent.current_agent) == RandomAgent:
                    agent_type = PigChaseEnvironment.AGENT_TYPE_1
                else:
                    agent_type = PigChaseEnvironment.AGENT_TYPE_2
                obs = env.reset(agent_type)

            # take a step
            obs, reward, agent_done = env.do(action)


    else:

        if baseline_agent == 'astar':
            agent = FocusedAgent(name, ENV_TARGET_NAMES[0])
        elif baseline_agent == 'sandhog':
            agent = SandhogAgent(name, ENV_AGENT_NAMES[ENV_AGENT_NAMES.index(name) - 1], ENV_TARGET_NAMES[0], visualizer)
        else:
            agent = RandomAgent(name, env.available_actions)

        obs = env.reset()
        reward = 0
        agent_done = False
        viz_rewards = []

        max_training_steps = EPOCH_SIZE * max_epochs
        for step in range(1, max_training_steps+1):

            # check if env needs reset
            if env.done:

                visualize_training(visualizer, step, viz_rewards)
                viz_rewards = []
                obs = env.reset()

            # select an action
            action = agent.act(obs, reward, agent_done, is_training=True)
            # take a step
            obs, reward, agent_done = env.do(action)
            viz_rewards.append(reward)

            agent.inject_summaries(step)


def run_experiment(agents_def):
    assert len(agents_def) == 2, 'Not enough agents (required: 2, got: %d)'\
                % len(agents_def)

    processes = []
    for agent in agents_def:
        p = Thread(target=agent_factory, kwargs=agent)
        p.daemon = True
        p.start()

        # Give the server time to start
        if agent['role'] == 0:
            sleep(1)

        processes.append(p)

    try:
        # wait until only the challenge agent is left
        while active_count() > 2:
            sleep(0.1)
    except KeyboardInterrupt:
        print('Caught control-c - shutting down.')


if __name__ == '__main__':
    arg_parser = ArgumentParser('Pig Chase baseline experiment')
    arg_parser.add_argument('-t', '--type', type=str, default='astar',
                            choices=['astar', 'random', 'sandhog'],
                            help='The type of baseline to run.')
    arg_parser.add_argument('-e', '--epochs', type=int, default=5,
                            help='Number of epochs to run.')
    arg_parser.add_argument('clients', nargs='*',
                            default=['127.0.0.1:10000', '127.0.0.1:10001'],
                            help='Minecraft clients endpoints (ip(:port)?)+')
    args = arg_parser.parse_args()

    logdir = BASELINES_FOLDER % (args.type, datetime.utcnow().isoformat())
    if 'malmopy.visualization.tensorboard' in sys.modules:
        visualizer = TensorboardVisualizer()
        visualizer.initialize(logdir, None)
    else:
        visualizer = ConsoleVisualizer()

    agents = [{'name': agent, 'role': role, 'baseline_agent': args.type,
               'clients': args.clients, 'max_epochs': args.epochs,
               'logdir': logdir, 'visualizer': visualizer}
              for role, agent in enumerate(ENV_AGENT_NAMES)]

    run_experiment(agents)

