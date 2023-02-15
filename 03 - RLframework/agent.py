import random

class RandomAgent:
    def __init__(self, n_actions):
        self.n_actions = n_actions
    
    def act(self, state):
        # Take a random action
        return random.randint(0, self.n_actions - 1)
    
if __name__ == "__main__":
    agent = RandomAgent(n_actions=3)
    
    for i in range(10):
        print("Action chosen:", agent.act(state=[]))
