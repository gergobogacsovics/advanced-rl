import random
import numpy as np

SIGNAL_WIN = 0
SIGNAL_LOST = 1

class BanditEnvironment:
    def __init__(self, n_bandits):    
        self.n_bandits = n_bandits
        
        # Modify this line so that each bandit hits the jackpot 0-20% of the time, randomly  
        self.bandits = [random.randint(0, 20) / 100 for b in range(self.n_bandits)]
        
        # Modifiy this percentage to a higher value (e.g. 60%) for a randomly selected bandit
        self.bandits[random.randint(0, n_bandits-1)] = 0.6
        
        print("Generated probabilities:", [b for b in self.bandits])
    
    def reset(self):
        return 0
    
    def step(self, action):
        # Take the bandit that the agent has selected
        p_win = self.bandits[action]
        
        # Pull the lever (generate a random result based on the probibilites of the selected bandit)
        pull_result = np.random.choice([SIGNAL_WIN, SIGNAL_LOST], 1, p=[p_win, 1 - p_win])[0]

        # Set the reward variable to 1 if the player hit the jackpot, 0 otherwise
        if pull_result == SIGNAL_WIN:
            reward = 1
        else:
            reward = 0
        
        new_state = 0
        done = False
        
        return new_state, reward, done
    
if __name__ == "__main__":
    env = BanditEnvironment(n_bandits=3)
    
    for episode in range(10):
        # Reset the environment
        state = env.reset()
        done = False
        num_tries = 0
        
        while not done and num_tries < 10:
            new_state, reward, done = env.step(0)
            
            if done:
                break
            
            state = new_state
