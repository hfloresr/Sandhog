---
layout: default
title: Status
---

<iframe src="https://player.vimeo.com/video/219234708" width="640" height="500" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
<p><a href="https://vimeo.com/219234708">Deep Q Pig Chase</a> from <a href="https://vimeo.com/user67099619">Hector Flores</a> on <a href="https://vimeo.com">Vimeo</a>.</p>

## Project Summary

The focus of our project is to design and implement a learning algorithm that trains an agent to collaborate with another (human or non-human) agent to catch a pig in Minecraft according to the rules of [The Malmo Collaborative AI Challenge](https://www.microsoft.com/en-us/research/academic-program/collaborative-ai-challenge/# "Challenge Homepage").

We have defined our baseline agent to be one that uses $$A^{*}$$ to determine the shortest distance to aid in capturing the pig. We aim to improve our baseline by using reinfocement learning and train an agent to maximize aggregate future rewards.

Given the complexity of the collaborative challenge, we will employ off-the-shelf deep learning and reinforcement learning libraries to provide the necessary flexibility to explore various reinforcement design paradigms along with parameter tuning.

## Approach

We consider the task in which our agent interacts with the Minecraft environment by making sequence of actions, observations, and receiving rewards. At each time step, the agent selects an action $$a_t$$ from the action space, $$\mathcal{A} = \{turn left, turn right, step forward\}$$. The agent observes an image $$x_t \in \mathbb{R}^{d}$$ from the emulator, which is a vector of pixel values representing the current screen frame. The agent also receives a reward $$r_t$$ representing the change in game score. Although the game score depends on the previous sequence of actions and observations, immediate rewards are described as:
  * +5 for exiting through a gate
  * +25 for catching the pig
  * -1 for each action

A symbolic representation of the state space is shown in figure 1.

Since the agent only observes the current screen, it is impossible for the agent to fully perceive the current situation fom the the current screen $$x_t$$. Therefore, we consider the sequences of actions and observations, $$s_t = x_{1},a_{1},x_{2}, ... , a_{t-1}, x_{t}$$, where $$x_t$$ is is the vector of pixel values that represent the visual input from the agent. The sequences are large but finite, therefore formalizing our finite Markov Decision Process (MDP) where the sequence $$s_t$$ is a distinct state at each time $$t$$.

The goal of our agent is to select actions in order to maximize future rewards. With the discount factor of $$\gamma \; (=0.99)$$, our future reward at time $$t$$ is defined as:

$$R_{t} = \sum_{t'=t}^{T} \gamma^{t'-t}r_{t'} \text{,}$$

where $$T$$ is the number of time steps in an episode of the pig chase game. We use the standard definition of the optimal action-value function in which the maximum expected reward acheivable by following any policy $$\pi$$, after seeing some sequence $$s$$ and taking some action $$a$$ is,

$$Q^{*}(s,a) = \max_{\pi} \mathbb{E} [ R_{t} \, \lvert \, s_{t}=s, a_{t}=a, \pi ]$$


Symbolic State Space:

![Alt text](results/state_space.PNG?raw=true "State Space")
![Alt text](results/labels.png?raw=true "Labels")

### Algorithm:
Our state is an $$84 \times 84$$ grayscale image which represents the screen pixels of the pig chase game.
To avoid an extremely large Q-table, we used a function approximator to approximate the Q function:

$$Q(s, a; \theta) \approx Q^{*}(s, a)$$


The function approximator used in this project is non-linear deep neural network. The architecture for
our neural network is as follows:

<br>
<p align="center">
$$\begin{array}{|c|c|c|c|c|c|c|}
\hline
\textbf{Layer} & \textbf{Input} & \textbf{Filter size} & \textbf{Stride} & \textbf{Number of filters} & \textbf{Activation} & \textbf{Output} \\
\hline
\text{Convolution 1} & 84\times84\times84 & 8\times8 & 4 & 32 & \text{ReLU} & 20\times20\times32 \\
\hline
\text{Convolution 2} & 20\times20\times32 & 4\times4 & 2 & 64 & \text{ReLU} & 9\times9\times64 \\
\hline
\text{Convolution 3} & 9\times9\times64 & 3\times3 & 1 & 64 & \text{ReLU} & 7\times7\times64 \\
\hline
\text{Dense} & 512 & & & & & \\
\hline
\end{array}$$
</p>

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
that randomly samples the data to remove correlations in the observation sequence. Our temporal memory
stores $$N$$ previouse samples of the agent's experiences $$(t, t-1, t-2, .. , t-N)$$. During training,
we use a linear $$\epsilon-greedy$$ approach to offset the exploration/exploitation dilemma. The linear
$$\epsilon-greedy$$ approach linearly interpolates between $$\epsilon_{max}$$ to $$\epsilon_{min}$$ to
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
![](results/agent2_episode_mean_q.PNG){:height="50%" width="50%"}

![](results/agent2_episode_mean_stddev_q.PNG){:height="50%" width="50%"}

![](results/training_actions_per_episode.PNG){:height="50%" width="50%"}

![](results/training_max_reward.PNG){:height="50%" width="50%"}

![](results/training_min_reward.PNG){:height="50%" width="50%"}

![](results/training_reward_per_episode.PNG){:height="50%" width="50%"}



## Remaining Goals and Challenges

Over the next few weeks, our goals are to:

1. Make the agent more collaborative by embedding the other agent's actions into the states of our MDP.

The challenges posed by these are:

1. The increased complexity of a more collaborative approach.




