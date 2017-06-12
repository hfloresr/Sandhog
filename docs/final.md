---
layout: default
title: Final Report
---
## Video

## Project Summary
The focus of our project is to design and implement a learning algorithm that trains an agent to collaborate with another (human or non-human) agent to catch a pig in Minecraft according to the rules of [The Malmo Collaborative AI Challenge](https://www.microsoft.com/en-us/research/academic-program/collaborative-ai-challenge/# "Challenge Homepage").

We have defined our baseline agent to be one that uses A* to determine the shortest distance to aid in capturing the pig. We aim to improve our baseline by using well known techniques in reinforcment learning, machine learning, and classical artificial intelligence.

## Approaches
<img src="results/state_space.PNG" alt="alt text" width="35%" height="35%"> <img src="results/labels.png" alt="alt text" width="20%" height="20%">
<center>Figure 1: Symbolic view of a possible state.</center>

<br>
We consider the task in which our agent interacts with the Minecraft environment by making sequence of actions, observations, and receiving rewards. At each time step, the agent selects an action $$a_t$$ from the action space, $$\mathcal{A} = \{turn left, turn right, step forward\}$$. Our agent observes the positions and orientations of the pig and second agent relative to its own position, 

$$x_{agent1_{t}}$$, $$x_{agent2_{t}}$$, $$x_{pig_{t}} \in \mathcal{X}^{2}$$
$$\mathcal{X} = \{0, 1, 2, 3, 4, 5, 6\}$$

$$o_{agent1_{t}}$$, $$o_{agent2_{t}}$$, $$o_{pig_{t}} \in \mathcal{O}$$
$$\mathcal{O} = \{North, East, South, West\}$$

as the coordinates for agent and opponent, respectively. Although the game score depends on the previous sequence of actions and observations, immediate rewards are described as:
  * +5 for exiting through a gate
  * +25 for catching the pig
  * -1 for each action

A symbolic representation of the state space is shown in figure 1.

## Evaluation

## References
