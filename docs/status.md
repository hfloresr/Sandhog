---
layout: default
title: Status
---

<iframe src="https://player.vimeo.com/video/219234708" width="640" height="500" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
<p><a href="https://vimeo.com/219234708">Deep Q Pig Chase</a> from <a href="https://vimeo.com/user67099619">Hector Flores</a> on <a href="https://vimeo.com">Vimeo</a>.</p>

## Project Summary

The ultimate goal of our project remains the same: to design and implement a learning algorithm that trains an agent to collaborate with another (human or non-human) agent to catch a pig in Minecraft according to the rules of [The Malmo Collaborative AI Challenge](https://www.microsoft.com/en-us/research/academic-program/collaborative-ai-challenge/# "Challenge Homepage").

We have since defined, however, an initial subgoal: to design and implement a prototype of this algorithm using off-the-shelf Q-learning methods.

## Approach

The game uses a 9x9 grid board. We model the problem as a Markov Decision Process (MDP) where

1. The actions are
    * Turn right
    * Turn left
    * Move forward one step
    * Move backward one step
2. The rewards are
    * +5 for exiting through a gate
    * +25 for catching the pig
    * -1 for each action, and
3. The states are agent's position on the board (x, y).

State Space:

![Alt text](results/state_space.PNG?raw=true "State Space")
![Alt text](results/labels.png?raw=true "Labels")

### Algorithm:
Our state is an $$84 \times 84$$ grayscale image which represents the screen pixels of the pig chase game.
To avoid an extremely large Q-table, we used a function approximator to approximate the Q function:

$$Q(s, a; \theta) \approx Q^{*}(s, a)$$


The functionn approximator used in this project is non-linear deep neural network. The architecture for
our neural network is as follows:

| Layer | Input    | Filter size | Stride | Number of filters | Activation | Output   |
|:-----:|:--------:|:-----------:|:------:|:-----------------:|:----------:|:--------:|
| Conv1 | 84x84x4  | 8x8         | 4      | 32                | ReLU       | 20x20x32 |
| Conv2 | 20x20x32 | 4x4         | 2      | 64                | ReLU       | 9x9x64   |
| Conv3 | 9x9x64   | 3x3         | 1      | 64                | ReLU       | 7x7x64   |
| Dense | 512      |             |        |                   |            |          |



Linear $$\epsilon-greedy$$ approach:
Linear interpolation between $$\epsilon_{max}$$ to $$\epsilon_{min}$$ to linearly anneal $$\epsilon$$ as a
function of the current episode.

Temporal Memory to store N previous samples $$(t, t-1, t-2, ... , t-N)$$



We use reinforcement learning, specifically, a deep reinforcement learning algorithm where the algorithm uses Q-learning to update expectations of rewards, but a neural netowrk to approximate the value function.

## Evaluation
![Alt text](results/agent2_episode_mean_q.PNG?raw=true "mean q")

![Alt text](results/agent2_episode_mean_stddev_q.PNG?raw=true "stddev q")

![Alt text](results/training_actions_per_episode.PNG?raw=true "training/actions per episode")

![Alt text](results/training_max_reward.PNG?raw=true "training/max reward")

![Alt text](results/training_min_reward.PNG?raw=true "training/min reward")

![Alt text](results/training_reward_per_episode.PNG?raw=true "training/reward per episode")


## Remaining Goals and Challenges

Over the next few weeks, our goals are to:

1. Make the agent more collaborative by embedding the other agent's actions into the states of our MDP.

The challenges posed by these are:

1. The increased complexity of a more collaborative approach.




