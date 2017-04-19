---
layout: default
title:  Proposal
---

## Summary of the Project
The aim of our project is to participate in the Collaborative AI Challenge. We will implement and train an agent that can collaborate with any collaborator to try to capture the pig in the "Pig Chase" challenge.

#### Overview of the game:
Two Minecraft agents and a pig are wandering a small meadow. The agents have two choices:
  * Catch the pig (i.e., the agents pinch or corner the pig, and no escape path is available), and receive a high reward (25 points)
  * Give up and leave the pig pen through the exits to the left and right of the pen, marked by blue squares, and receive a small reward (5 points)

#### How to play
  * The game is played over 10 rounds at a time. Goal is to accumulate the highest score over these 10 rounds.
  * In each round a "collaborator" agent is selected to play with you. Different collaborators may have different behaviors.
  * Once the game has started, use the left/right arrow keys to turn, and the forward/backward keys to move. You can see your agent move in the first person view, and shown as a red arrow in the top-down rendering on the left.
  * You and your collaborator move in turns and try to catch the pig (25 points if caught). You can give up on catching the pig in the current round by moving to the blue "exit squares" (5 points). You have a maximum of 25 steps available, and will get -1 point for each step taken.

## AI/ML Algorithms
We plan on using reinforcement learning for our algorithm.

## Evaluation Plan
For evaluating our algorithm we plan on comparing the total reward gained in ten rounds for the Pig Chase challenge. We also plan on using the the total reward our agent recieves with respect to the number of steps it takes for tracking the progress of our learner. The data that will be used are the statistics that are logged on the malmo-challenge script provided. TensorBoard will be used for visualizing and debugging our learner. Furthermore we will be using the A-star agent as our baseline.


## Appointment with the Instructor
01:45pm - Tuesday, April 25, 2017
