import torch
import random
import numpy as np
from simulation.cube2 import Cube
from collections import deque

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
NUM_ACTIONS = 18

class Agent:
    
    def __init__(self):
        self.n_attempts = 0
        self.epsilon = 0 #randomness
        self.gamma = 0 #discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = None #TODO
        self.trainer = None #TODO
        #model, trainer

    def get_state(self, simulation):
        simulation.get_state() 

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def action_to_onehot(self, action):
        onehot = np.zeros(NUM_ACTIONS)
        onehot[action] = 1
        return onehot

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        
        actions_onehot = [self.action_to_onehot(action) for action in actions]

        self.trainer.train_step(states, actions_onehot, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        action_onehot = self.action_to_onehot(action)
        self.trainer.train_step(state, action_onehot, reward, next_state, done)

    def get_action(self, state):
        #Exploration vs exploitation
        self.epsilon = 100 - self.n_games
        if random.randint(0, 200) < self.epsilon:
            #Random action (exploration)
            final_move = random.randint(0, 17)
        else:
            #Model prediction (exploitation)
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)  #Output: [18] probabilities
            final_move = torch.argmax(prediction).item()  #Get action with highest probability
        
        return final_move

def train():
    #score is defined as num matching stickers + 4x num matching faces

    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0

    agent = Agent()
    simulation = Cube()

    while True:
        state_old = agent.get_state(simulation)

        final_move = agent.get_action(state_old)

        reward, done, score = simulation.step()

        state_new = agent.get_state(simulation)

        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            simulation.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                #agent.model.save()

                print('Simulation', agent.n_games, 'Score', score, 'Record:', record)
                # plot






if __name__ == '__main__':
    train()
