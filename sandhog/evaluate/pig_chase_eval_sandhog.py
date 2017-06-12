
from common import ENV_AGENT_NAMES, ENV_TARGET_NAMES
from evaluation import PigChaseEvaluator
from environment import PigChaseSymbolicStateBuilder
from SandhogAgent import SandhogAgent


if __name__ == '__main__':
    clients = [('127.0.0.1', 10000), ('127.0.0.1', 10001)]

    agent = SandhogAgent(ENV_AGENT_NAMES[1], ENV_AGENT_NAMES[
                         0], ENV_TARGET_NAMES[0])
    agent2 = SandhogAgent(ENV_AGENT_NAMES[1], ENV_AGENT_NAMES[
                          0], ENV_TARGET_NAMES[0])

    builder = PigChaseSymbolicStateBuilder()
    eval = PigChaseEvaluator(clients, agent, agent2, builder)
    eval.run()
    eval.save('Sandhog_vs_Sandhog', 'pig_chase_results_sandhog.json')
