
from malmopy.agent import BaseAgent
from common import visualize_training, ENV_AGENT_NAMES, ENV_ACTIONS
from a_star import a_star


class SandhogAgent(BaseAgent):
    ACTIONS = ENV_ACTIONS
    EXIT1_POS = (4, 1)
    EXIT2_POS = (4, 7)
    initial_prob = 1

    def __init__(self, name, other_agent, target, visualizer=None,
                 alpha=0.4, threshold=0.5, global_alpha=0.4):
        super(SandhogAgent, self).__init__(
            name, len(SandhogAgent.ACTIONS), visualizer=visualizer)

        self._target = str(target)
        self._other_agent = str(other_agent)
        self._prev_target_pos = None
        self._prev_other_pos = None
        self._prev_pos = None
        self._action_list = []
        self._prob = self.initial_prob
        self._global_prob = self.initial_prob
        self._intent = []
        self._intentions = []
        self._timestep = 0
        self.alpha = alpha
        self.global_alpha = global_alpha
        self.threshold = threshold
        self.too_far = False
        self.step = 0
        self._num_episode = 0

        self._prev_other_cost_EXIT1 = None
        self._prev_other_cost_EXIT2 = None
        self._prev_other_cost_pig = None

    def act(self, state2, reward, done, is_training=False):
        self.step += 1

        if done:
            self._action_list = []
            self._prev_target_pos = None
            self._prev_other_pos = None
            self._prev_pos = None
            self._intent = []
            self._intentions = []

            if reward <= 0:
                if self.too_far:
                    pass
                    #print('{}: pig is too far'.format(self.name))
                else:
                    self._global_prob = max(
                        0.0, self._global_prob - self.global_alpha)
            elif reward <= 5:
                self._global_prob = (self._global_prob + self._prob) / 2
            else:
                self._global_prob = min(
                    self._global_prob + self.global_alpha, 1.0)

            #print('\nglobal_prob: {}'.format(self._global_prob))
            self._prob = self._global_prob
            self._timestep = 0
            self._prev_other_cost_EXIT1 = None
            self._prev_other_cost_EXIT2 = None
            self._prev_other_cost_pig = None

            self.add_entry_to_visualizer(
                'Debug', 'global_prob', self._global_prob, self._num_episode)
            self._num_episode += 1

            # always a different opponent
            self._prob = self.initial_prob
            return 0

        try:
            entities = state2[1]
            state = state2[0]
            # retrieve information from state

            me = [(i, j) for i, v in enumerate(state)
                  for j, k in enumerate(v) if self.name in k][0]
            me_info = [e for e in entities if e['name'] == self.name][0]

            other = [(i, j) for i, v in enumerate(state)
                     for j, k in enumerate(v) if self._other_agent in k][0]
            other_info = [e for e in entities if e[
                'name'] == self._other_agent][0]

            yaw = int(me_info['yaw'])
            # convert Minecraft yaw to 0=north, 1=east etc.
            direction = ((((yaw - 45) % 360) // 90) - 1) % 4

            other_yaw = int(other_info['yaw'])
            other_direction = ((((other_yaw - 45) % 360) // 90) - 1) % 4

            other = (other_direction, other)
            me = (direction, me)

            target = [(i, j) for i, v in enumerate(state)
                      for j, k in enumerate(v) if self._target in k][0]

            if self._prev_target_pos is None:
                self._prev_target_pos = target
            if self._prev_other_pos is None:
                self._prev_other_pos = other
            if self._prev_pos is None:
                self._prev_pos = me

            _, me_cost_EXIT1 = self.distance_exit1(me, state)
            _, me_cost_EXIT2 = self.distance_exit2(me, state)
            _, me_cost_pig = self.distance_pig(
                me, target, state)

            _, other_cost_EXIT1 = self.distance_exit1(
                other, state)
            _, other_cost_EXIT2 = self.distance_exit2(
                other, state)
            other_acc_now_pig, other_cost_pig = self.distance_pig(
                other, self._prev_target_pos, state, True)

            if self._prev_other_cost_EXIT1 is None:
                self._prev_other_cost_EXIT1 = other_cost_EXIT1
            if self._prev_other_cost_EXIT2 is None:
                self._prev_other_cost_EXIT2 = other_cost_EXIT2
            if self._prev_other_cost_pig is None:
                self._prev_other_cost_pig = other_cost_pig

            other_cost_prev_EXIT1 = self._prev_other_cost_EXIT1
            other_cost_prev_EXIT2 = self._prev_other_cost_EXIT2
            other_cost_prev_pig = self._prev_other_cost_pig

            other_delta_pig = other_cost_pig - other_cost_prev_pig
            if other_cost_prev_EXIT1 < other_cost_prev_EXIT2:
                other_delta_exits = other_cost_EXIT1 - other_cost_prev_EXIT1
            elif other_cost_prev_EXIT1 == other_cost_prev_EXIT2:
                other_delta_exits = min(
                    other_cost_EXIT1 - other_cost_prev_EXIT1, other_cost_EXIT2 - other_cost_prev_EXIT2)
            else:
                other_delta_exits = other_cost_EXIT2 - other_cost_prev_EXIT2

            other_stayed = self._prev_other_pos[1] == other[1]
            other_adj_to_pig = other[1] in self.neighbors(target, state)
            self._prob = self.prob_update(
                self._prob, other_delta_pig, other_delta_exits, other_stayed, other_adj_to_pig)
            # print('local prob - %f' % self._prob)
            self._intent = self.strategy(self._prob, min(me_cost_EXIT1, me_cost_EXIT2),
                                         min(other_cost_EXIT1, other_cost_EXIT2), target, state)
            self._intentions = self.adjust(self._prob, self._intent, self._intentions, target,
                                           self.EXIT1_POS if me_cost_EXIT2 > me_cost_EXIT1 else self.EXIT2_POS,
                                           other_acc_now_pig[-2][1] if len(other_acc_now_pig) > 1 else other[1], state)
            self._action_list = self.plan(
                self._prob, self._intentions, me, state)

            self._prev_other_pos = other
            self._prev_pos = me
            self._prev_target_pos = target
            self._timestep += 1

            self._prev_other_cost_EXIT1 = other_cost_EXIT1
            self._prev_other_cost_EXIT2 = other_cost_EXIT2
            self._prev_other_cost_pig = other_cost_pig

            print('Prob[ {} ] = {}\n'.format(self._intent, self._prob))
            self.add_entry_to_visualizer(
                'Debug', 'probs', self._prob, self.step)

            if self._action_list is not None and len(self._action_list) > 0:
                action = self._action_list.popleft()
                return SandhogAgent.ACTIONS.index(action)

            return SandhogAgent.ACTIONS.index("turn 1")

        except Exception as e:
            # print(state2)
            # print('error')
            # print(e)
            return SandhogAgent.ACTIONS.index("turn 1")

    def prob_update(self, prob, other_delta_pig, other_delta_exits, other_stayed, other_adj_to_pig):
        if self._timestep == 0:
            return prob
        def update_coop(b):
            return min(1.0, b + self.alpha)
        def update_exit(b):
            return max(0.0, b - self.alpha)
        if other_stayed and other_adj_to_pig:
            print("\nOther agent is holding position")
            return update_coop(prob)
        if other_delta_pig < 0 and other_delta_pig < other_delta_exits:
            print("\nOther agent moved closer to pig")
            return update_coop(prob)
        elif other_delta_pig == other_delta_exits:
            print("\nUncertain about other agent")
            return prob
        else:
            print("\nOther agent is being uncooperative")
            return update_exit(prob)

    def strategy(self, prob, me_cost_door, other_cost_door, pig_pos, state):
        adj_positions = self.neighbors(pig_pos, state)
        self.too_far = len(adj_positions) > 2
        if self.too_far:
            # impossible to catch!
            if me_cost_door < other_cost_door:
                # I'm closer
                if abs(me_cost_door - other_cost_door) <= 1:
                    return "exit"
                else:
                    return "hold"
            else:
                return "cooperate"

        if len(adj_positions) == 1:
            return "cooperate"

        if prob > self.threshold:
            # he is going to cooperate
            return "cooperate"
        else:
            if me_cost_door > other_cost_door:
                return "cooperate"
            else:
                return "exit"

    def adjust(self, prob, intent, intentions, pig_pos, best_door_pos, other_state, state):

        if intent == "cooperate":
            adj_positions = self.neighbors(pig_pos, state)
            if len(adj_positions) == 2:
                # possible to catch
                if other_state == adj_positions[0]:
                    return adj_positions[1]
                else:
                    return adj_positions[0]

            return pig_pos
        elif intent == "hold":
            return ENV_ACTIONS.index("turn 1")
        else:
            return best_door_pos

    def plan(self, prob, intentions, curr_pos, state):
        actions, _ = a_star(curr_pos, intentions, state)
        if intentions == "cooperate":
            return actions[:-1]
        else:
            return actions

    def distance_exit1(self, curr_pos, state):
        if curr_pos is None:
            return [], 0
        acc, EXIT1_cost = a_star(curr_pos, self.EXIT1_POS, state)
        return acc, EXIT1_cost

    def distance_exit2(self, curr_pos, state):
        if curr_pos is None:
            return [], 0
        acc, EXIT2_cost = a_star(curr_pos, self.EXIT2_POS, state)
        return acc, EXIT2_cost

    def distance_pig(self, curr_pos, pig_pos, state, output_states=False):
        if curr_pos is None or pig_pos is None:
            return [], 0
        acc, pig_cost = a_star(curr_pos, pig_pos, state, output_states)
        return acc, pig_cost

    def neighbors(self, pos, state):
        # up, right, down, left
        dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        result = []
        for d in dirs:
            result.append((pos[0] + d[0], pos[1] + d[1]))

        result = [n for n in result if
                  n[0] >= 0 and n[0] < state.shape[0] and n[1] >= 0 and n[1] < state.shape[1] and state[
                      n[0], n[1]] != 'sand']

        return result

    def add_entry_to_visualizer(self, tag, name, value, step):
        if self.can_visualize:
            self._visualizer.add_entry(step, '%s/%s' % (tag, name), value)
