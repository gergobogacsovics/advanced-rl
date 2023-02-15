from tqdm.notebook import tqdm
import numpy as np
import random
import matplotlib.pyplot as plt
from env import BanditEnvironment
from agent import RandomAgent

N_BANDITS = 3
N_EPISODES = 100
N_MAX_STEPS_PER_EPISODE = 1_000

SEED = 0

random.seed(SEED)
np.random.seed(SEED)

env = BanditEnvironment(n_bandits=N_BANDITS)

agent = RandomAgent(n_actions=N_BANDITS)

rewards = []

for episode in tqdm(range(N_EPISODES)):
    # Reset the environment
    state = env.reset()
    done = False
    
    # We will store the cumulated reward in this variable
    total_reward = 0
    
    for step in range(N_MAX_STEPS_PER_EPISODE):
        # Ask the agent for the next action
        action = agent.act(state=state)

        # Execute the action selected by the agent
        # We get:
        # - the new state s_{t+1}
        # - the reward r_{t+1}
        # - a flag that indicates whether if the episode has ended or not
        new_state, reward, done = env.step(action)
        
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
