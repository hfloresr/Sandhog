---
layout: default
title: Status
---

## Project Summary

The ultimate goal of our project remains the same: to design and implement a learning algorithm that trains an agent to collaborate with another (human or non-human) AI to catch a pig in Minecraft according to the rules of The Malmo Collaborative AI Challenge. 

We did define, however, an initial subgoal: to design and implement a prototype of this algorithm using off-the-shelf Q-learning methods.

## Approach

The game uses a 9x9 grid board. We model the problem as a Markov Decision Process (MDP) where

(a) The actions are
    (i) Turn right
    (ii) Turn left
    (iii) Move forward one step
    (iv) Move backward one step
(b) The rewards are
    (i) +5 for exiting through a gate
    (ii) +25 for catching the pig
    (iii) -1 for each action in (a), and
(c) The states are agent's position on the board (x, y). 
   
We use reinforcement learning, specifically, a deep reinforcement learning algorithm where the algorithm uses Q-learning to update expectations of rewards, but a neural netowrk to approximate the value function. 

## Evaluation



## Remaining Goals and Challenges

Over the next few weeks, our goals are to: 




