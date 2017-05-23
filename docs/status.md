---
layout: default
title: Status
---

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
   
We use reinforcement learning, specifically, a deep reinforcement learning algorithm where the algorithm uses Q-learning to update expectations of rewards, but a neural netowrk to approximate the value function. 

## Evaluation
![Alt text](results/agent2_episode_mean_q.PNG?raw=true "mean q")

![Alt text](results/agent2_episode_mean_stddev_q.PNG?raw=true "stddev q")

![Alt text](results/training_actions_per_episode.PNG?raw=true "stddev q")

![Alt text](results/training_max_reward.PNG?raw=true "stddev q")

![Alt text](results/training_min_reward.PNG?raw=true "stddev q")

![Alt text](results/training_reward_per_episode.PNG?raw=true "stddev q")


## Remaining Goals and Challenges

Over the next few weeks, our goals are to: 




