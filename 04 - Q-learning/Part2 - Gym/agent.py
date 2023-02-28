import random
import numpy as np

class RandomAgent:
    def __init__(self, n_actions):
        self.n_actions = n_actions
    
    def act(self, state):
        # Take a random action
        return random.randint(0, self.n_actions - 1)
    
class QLearningAgent:
    def __init__(self, n_states, n_actions, learning_rate):
        self.n_states = n_states
        self.n_actions = n_actions
        self.learning_rate = learning_rate
        
        self.q_table = np.zeros((n_states, n_actions))
    
    def act(self, state, epsilon):
        # Generate a random number on the [0, 1) interval
        random_int = random.random()
        
        # We exploit with (1-epsilon) probability
        if random_int > epsilon:
            action = np.argmax(self.q_table[state])
        # We explore with epsilon probability
        else:
            action = random.randint(0, self.n_actions - 1)
        
        return action
    
    def learn(self, state, action, reward, new_state, gamma):
        old_value = self.q_table[state][action]
        new_estimate = reward + gamma * max(self.q_table[new_state]) 
        
        self.q_table[state][action] = old_value + self.learning_rate * (new_estimate- old_value)   
    
if __name__ == "__main__":
    agent = RandomAgent(n_actions=3)
    
    for i in range(10):
        print("Action chosen:", agent.act(state=[]))
