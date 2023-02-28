# # The original code was based on can be found at https://colab.research.google.com/github/huggingface/deep-rl-class/blob/main/unit2/unit2.ipynb
from tqdm import tqdm
import numpy as np
import random
import matplotlib.pyplot as plt
#from env import BanditEnvironment
from agent import RandomAgent, QLearningAgent
import gym

N_EPISODES = 10_000
N_MAX_STEPS_PER_EPISODE = 100
LEARNING_RATE = 0.1

SEED = 0

random.seed(SEED)
np.random.seed(SEED)

#env = BanditEnvironment(n_bandits=N_BANDITS)
env = gym.make("FrozenLake-v1", map_name="4x4", is_slippery=False)

#agent = RandomAgent(n_actions=N_BANDITS)
agent = QLearningAgent(n_states=env.observation_space.n, n_actions=env.action_space.n, learning_rate=LEARNING_RATE)

max_epsilon = 1.0
min_epsilon = 0.05
decay_rate = 0.001
gamma = 0.95

rewards = []
epsilon_history = []

for episode in tqdm(range(N_EPISODES)):
    # Reset the environment
    state, info = env.reset()
    done = False
    
    epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay_rate * episode)
    
    # We will store the cumulated reward in this variable
    total_reward = 0
    
    for step in range(N_MAX_STEPS_PER_EPISODE):
        # Ask the agent for the next action
        action = agent.act(state=state, epsilon=epsilon)

        # Execute the action selected by the agent
        # We get:
        # - the new state s_{t+1}
        # - the reward r_{t+1}
        # - a flag that indicates whether if the episode has ended or not
        new_state, reward, done, truncated, info = env.step(action)
        
        agent.learn(state, action, reward, new_state, gamma)
        
        # We store the obtained reward
        total_reward += reward

        # If the episode has finished, we exit the for loop
        if done:
            break
            
        # We update the current state:
        # s_{t} = s_{t+1}
        state = new_state
        
    #print(f"Total reward for episode {episode}: {total_reward}")
    
    rewards.append(total_reward)
    epsilon_history.append(epsilon)

print("Learnt Q-table:")
print(agent.q_table)

plt.plot(range(N_EPISODES), epsilon_history)
plt.title("The value of epsilon in each episode")
plt.xlabel("Episode")
plt.ylabel("Epsilon")
plt.show()

plt.plot(range(N_EPISODES), rewards)
plt.xlabel("Episode")
plt.ylabel("Reward")
plt.show()

def smoothen(data):
    return np.cumsum(data) / np.arange(len(rewards) + 1)[1:]

rewards_smooth_window_5 = smoothen(rewards)

plt.plot(range(N_EPISODES), rewards)
plt.plot(range(N_EPISODES), rewards_smooth_window_5, color="orange")
plt.title("The obtained reward in each episode")
plt.xlabel("Episode")
plt.ylabel("Reward")
plt.legend(["rewards", "averaged rewards"])
plt.show()
