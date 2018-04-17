__author__ = "John Muchovej"
__license__ = "GPLv3.0"

import numpy as np

import gym
from gym import wrappers


def run_episode(env, policy=None, render=False):

    obs = env.reset()
    
    total_reward = 0

    ## note: `step_idx` for the discounting factor is initialized here
    for step_idx in range(max_time):
        
        if render:
            env.render()

        a,b = obs_to_state(env, obs)
        action = env.action_space.sample() if policy is None else policy[a][b]
        
        obs, reward, done, _ = env.step(action)
        total_reward += (gamma ** step_idx) * reward
        
        if done:
            return total_reward


def obs_to_state(env, obs):
    """ Maps an observation to state """
    env_lo = env.observation_space.low
    env_hi = env.observation_space.high

    env_dx = (env_hi - env_lo) / n_states

    a = int((obs[0] - env_lo[0]) / env_dx[0])
    b = int((obs[1] - env_lo[1]) / env_dx[1])

    return a, b

################################################################################
## states and the actions that can be taken
n_states = 40
n_action = 3

## episodic and temporal limits
max_iter = 10000
max_time = 10000

## learning rates
lr_ini = 1.0
lr_min = 0.003

## discounting factor
gamma = 1.0

## probability of not exploring
epsilon = 0.02

## general initiatlization
env_name = 'MountainCar-v0'
env = gym.make(env_name)
env.seed(0)
np.random.seed(0)

## initialize the Q table
q_table = np.zeros((n_states, n_states, n_actions))
################################################################################

## Q-Learning
for episode in range(max_iter):

    obs = env.reset()
    total_reward = 0

    ## learning rate is decreased at each step
    lr = max(lr_min, lr_ini * (0.85 ** (episode // 100)))

    for _ in range(max_time):
    	## make an attempt, and retribe an observation
        a, b = obs_to_state(env, obs)

        logits     = q_table[a][b]
        logits_exp = np.exp(logits)

        weighted_probs = logits_exp / np.sum(logits_exp)

        exploit = np.random.uniform(0, 1) < epsilon
        distrib = weighted_probs if exploit else None
    	action  = np.random.choice(env.action_space.n, p=distrib)

        obs, reward, done, _ = env.step(action)
        total_reward += reward
        
        ## we move into the "next timestep", so what is "prev_action" is 
        ## the Q value of the action taken above
        a_, b_ = obs_to_state(env, obs)

        ## prior action we took
        prev_action = q_table[a][b][action]
        ## action we might take before of prior action
        next_action = q_table[a_][b_]

        ## Q(s, a) = (1 - \alpha) * Q(s, a) 
        ##           + \alpha * [r(s, a) + \gamma * max{Q(s', a')}]
        ## some voodoo later...
        ## Q(s, a) = Q(s, a) + \alpha * [r(s, a) + \gamma * max{Q(s', q')} - Q(s, a)]
        q_table[a][b][action] = prev_action + lr * (reward + gamma * np.max(next_action) - prev_action)

        if done:
            break

    if episode % 100 == 0:
        print('iter: {0:5d} | reward: {1:5.5f}.'.format(i + 1, total_reward))

################################################################################
## Select the best solution
solution_policy = np.argmax(q_table, axis=2)

## Score the solutions
solution_policy_scores = [run_episode(env, policy=solution_policy) for _ in range(100)]

print("mean(reward): {5.5f}".format(np.mean(solution_policy_scores)))

## Visualize actions based on the best solution
run_episode(env, policy=solution_policy, render=True)