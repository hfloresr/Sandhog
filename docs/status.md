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

<br>
$$\begin{array}{|c|c|c|c|c|c|c|}
\hline
\text{Layer} & \text{Input} & \text{Filter size} & \text{Stride} & \text{Number of filters} & \text{Activation} & \text{Output} \\
\hline
\end{array}$$
<br>
The Q-learning update uses the Huber loss function, defined as:

$$L(\theta) =
\begin{cases}
\frac{1}{2}{\theta}^2, & \text{if $|\theta| \lt \delta$} \\
\delta |\theta| - \frac{1}{2}\delta^{2}, & \text{if $|\theta| \geq \delta$}
\end{cases}$$

where $$\delta \, (\geq 0)$$ is the outlier threshold parameter. We used stochasitc gradient descent
to optimize the Huber loss function.

<br>
Since reinforcement learning with a neural network is known to be unstable we used experience replay
that randomly samples the data to remove correlations in the obseration sequence. Our temporal memory
stores $$N$$ previouse samples of the agent's experiences $$(t, t-1, t-2, .. , t-N)$$. During training,
we use a linear $$\epsilon-greedy$$ approach to offset the exploration/exploitation dilemma. The linear
$$\epsilon-greedy$$ approach linearly interpolates betwee $$\epsilon_{max}$$ to $$\epsilon_{min}$$ to
linearly anneal $$\epsilon$$ as a function of the current episode.

The learning algorithm can be described as the following:
  * Initialize temporal memory $$D$$ to capacity $$N$$
  * Initialize action-value function $$Q$$ with random weights $$\theta$$
  * Initialize target action-value function $$\hat{Q}$$ with weights $$\theta^{-}$$
  * **For** episode $$= 1, ... , M$$:
      * Initialize sequence $$s_1 = {x_1}$$ and preprocessed sequence $$\phi_1 = \phi(s_1)$$
      * **For** $$t = 1, ..., T$$:
          * Select random action $$a_t$$ with probability $$\epsilon$$
          * Execute action $$a_t$$ and observe reward $$r_t$$ and frame $$x_{t+1}$$
          * Set $$s_{t+1} = s_{t},a_{t},x_{t+1}$$ and preprocess $$\phi_{t+1} = \phi(s_{t+1})$$
          * $$D$$.append($$\phi_{t}, a_{t}, \phi_{t+1}$$)
          * Sample random minibatch from $$D$$
          * Set $$y_{j} =
                \begin{cases}
                r_{j}, & \text{if episode terminates at step $j+1$} \\
                r_{j} + \gamma \max_{a'} \hat{Q}(\phi_{j+1}, a'; \theta^{-}), & \text{otherwise}
                \end{cases}$$
          * Perform stocahstic gradient descent step on $$L(y_j - Q(\phi_{j},a{j};\theta))$$, where
            $$L$$ is the Huber loss function as previously described.
          * Every $$C$$ steps reset $$\hat{Q} = Q$$






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




