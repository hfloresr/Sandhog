---
layout: default
title: Final Report
---
## Video
<iframe src="https://player.vimeo.com/video/221383197" width="640" height="360" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>

## Project Summary
The focus of our project is to design and implement a learning algorithm that trains an agent to collaborate with another (human or non-human) agent to catch a pig in Minecraft according to the rules of [The Malmo Collaborative AI Challenge](https://www.microsoft.com/en-us/research/academic-program/collaborative-ai-challenge/# "Challenge Homepage").

We have defined our baseline agent to be one that uses A* to determine the shortest distance to aid in capturing the pig. We aim to improve our baseline by using well known techniques in reinforcment learning, machine learning, and classical artificial intelligence.

## Approaches
<img src="results/state_space.PNG" alt="alt text" width="35%" height="35%"> <img src="results/labels.png" alt="alt text" width="20%" height="20%">
<center>Figure 1: Symbolic view of a possible state.</center>

<br>
We consider the task in which our agent interacts with the Minecraft environment by making sequence of actions, observations, and receiving rewards. At each time step, the agent selects an action $$a_t$$ from the action space, $$\mathcal{A} = \{turn left, turn right, step forward\}$$. Our agent observes the positions and orientations of the pig and second agent relative to its own position, 

$$x_{agent1_{t}}, \, x_{agent2_{t}}, \, x_{pig_{t}} \in \mathcal{X}^{2}, \; \text{where} \; \mathcal{X} = \{0, 1, 2, 3, 4, 5, 6\}$$


$$o_{agent1_{t}}, \, o_{agent2_{t}}, \, o_{pig_{t}} \in \mathcal{O}, \; \text{where} \; \mathcal{O} = \{North, East, South, West\}$$

The agent also receives a reward $$r_t$$ representing the change in game score. Although the game score depends on the previous sequence of actions and observations, immediate rewards are described as:
  * +5 for exiting through a gate
  * +25 for catching the pig
  * -1 for each action

A symbolic representation of the state space is shown in figure 1.


We further extend our state space to include the second agent's previous move to make inference on its intentions to collaborate. We therefore formalize our finite Markov Decision Process (MDP) where the sequence $$s_t$$ is a distinct state at each time $$t$$ and defined as the following:

$$s_t = \{x_{agent1_{t}}, \, x_{agent2_{t}}, \, x_{pig_{t}}, \, o_{agent1_{t}}, \, o_{agent2_{t}}, \, o_{pig_{t}}, a_{agent2_{t-1}}\}$$


The malmo challange introduces an uncertainity about the actions of *agent2* and the pig, which required developing a probabilistic model to infer the objective of *agent2*. We exclude any inference about the actions the pig might make since all of the pig's actions are random and our primary objective is to collaborate with *agent2* to acheive the highest reward possible.

To create a collaborative effort between our agent (*agent1*) and *agent2*, we based our agent's decisions on the probability of *agent2*'s intentention to help catch the pig.  To describe the intentions of *agent2*, we define the random variable $$Z = \{Random, Exit, Pig\}$$. We then represent our probability vector, $$\mathbf{p}$$, as our distribution over the random variable $$Z$$,

$$\mathbf{p}_{t} =
\begin{bmatrix} 
\mathbb{P}[Z = Random] \\
\mathbb{P}[Z = Exit] \\
\mathbb{P}[Z = Pig]
\end{bmatrix}$$

We assume that *agent2* is an optimal agent, such that it trys to find the shortest path to their goal. At each time step $$t$$, we compute the shortest path to the pig and the two exits via A* search algorithm. We can then estimate *agent2*'s optimal policy for each of the possible intentions, which is represented as

$$\pi(s_{t}) = \{\pi_{exit_{t}}, \, \pi_{pig_{t}}\}$$

We store that last two steps so we can infer *agent2*'s intent by as the conditional probability of $$\pi$$ given the previous states. We included a discount factor to give more weight to more recent decisions, the probability is as follows,

$$\mathbb{P}[Z \, \lvert \, p]
= \prod_{i=0}^{n-1} \gamma^i \mathbb{P}[p \, \lvert \, s_{t-(n-i)}], \; \forall p \in \pi$$

Furthermore, we assume that the *agent2* is a random agent if all of the probabilities are equal. Since we are assuming that *agent2* acheives its goals via shortest path, then we can extract *agent2*'s intent by maximizing over the conditional probabilities:

$$Z' = arg\,max_{x \in \pi} \mathbb{P}[Z \, \lvert \, x]$$

Once we have determined *agent2*'s intent, we can update our probabilities by adding a constant weight, $$\eta$$, to the respecitve intent and normalizing by $$\alpha$$, as such

$$\mathbf{p}_{t+1} =
\begin{cases}

\alpha \cdot
\begin{bmatrix} 
\mathbb{P}[Z = Random] + \eta\\
\mathbb{P}[Z = Exit] \\
\mathbb{P}[Z = Pig]
\end{bmatrix}, & \text{if $Z' = Random$}\\

\alpha \cdot
\begin{bmatrix} 
\mathbb{P}[Z = Random]\\
\mathbb{P}[Z = Exit] + \eta\\
\mathbb{P}[Z = Pig]
\end{bmatrix}, & \text{if $Z' = Exit$}\\

\alpha \cdot
\begin{bmatrix} 
\mathbb{P}[Z = Random] \\
\mathbb{P}[Z = Exit] \\
\mathbb{P}[Z = Pig] + \eta
\end{bmatrix}, & \text{if $Z' = Pig$}\\
\end{cases}$$

To determine a strategy for our agent, we used an $$\epsilon - greedy$$ approach by determining the intentions of *agent2*. At a given time step, $$t$$, we have a probability vector, $$\mathbf{p}_{t}$$ (as defined earlier), that helps estimate the cooperation level of *agent2*. With probability $$1 - \epsilon$$ we determine that *agent2's* intensions is $$Z' = arg\,max_{x \in \pi} \mathbb{P}[Z \, \lvert \, x]$$. Otherwise, we choose the second highest probabilty in $$\mathbf{p}_{t}$$. After deciding the intentions of *agent2*, our agent follows a simple strategy that can be described as the following:

    * If agent determines that agent2 is a cooperative agent:
        * If the pig has more than two adjacent positions:
            * Go to nearest exit if our agent is closer to it than agent2 to any of the other exits
            * Otherwise, chase the pig
        * Else:
            * Chase the pig
    * Else:
        * Go to nearest exit if our agent is closer to it than agent2 to any of the other exits
        * Otherwise, chase the pig

Since we compute the shortest path for all goals and for both agents at each time step, our agent can effeciently make the necessary action based on this approach.

## Evaluation



<img src="pics/final_figs/reward_per_episode.png" align="middle" width="75%" height="75%">

<center>Figure 2: Rewards per episode.</center>


<br>


<img src="pics/final_figs/actions_per_episode.png"  width="75%" height="75%">

<center>Figure 3: Number of actions agent makes per episode.</center>


<br>


<img src="pics/final_figs/train_max_reward.png" width="75%" height="75%">

<center>Figure 4: Max rewards.</center>

<br>


## References

Sutton, Richard S. and Andrew G. Barto. 1998. *Reinforcement Learning: An Introduction.* The MIT Press, Cambridge, MA.
