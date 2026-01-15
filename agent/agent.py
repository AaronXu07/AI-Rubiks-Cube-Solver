import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import torch
import random
import numpy as np
from simulation.cube2 import Cube
from collections import deque
from model.model import Linear_QNet, QTrainer
from plot import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
NUM_ACTIONS = 9
SCRAMBLE_LENGTH = 3

class Agent:
    
    def __init__(self):
        self.n_attempts = 0
        self.epsilon = 0 #randomness
        self.gamma = 0.9 #discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(24, 256, 9)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        #model, trainer

    def load_model(self, file_name='model.pth'):
        model_folder_path = './model'
        file_path = os.path.join(model_folder_path, file_name)
        if os.path.exists(file_path):
            self.model.load_state_dict(torch.load(file_path))
            print(f'Model loaded from {file_path}')
            return True
        else:
            print(f'No saved model found at {file_path}, starting fresh')
            return False

    def get_state(self, simulation):
        return simulation.get_state() 

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
        self.epsilon = max(5, 100 - self.n_attempts/2)
        if random.randint(0, 100) < self.epsilon:

            final_move = random.randint(0, 8)
        else:
            #Model prediction (exploitation)
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)               #Output: [9] probabilities
            final_move = torch.argmax(prediction).item()  #Get action with highest probability
        
        return final_move

def train(visualizer=None, visualize_every=1, visualization_speed=3):

    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    best_mean_score = 0  
    window_size = 100  

    agent = Agent()
    
    # Try to load previous best model to continue training
    agent.load_model()
    
    # If visualizer provided, use its cube, otherwise create new one
    if visualizer:
        simulation = visualizer.cube
        from vpython import rate
    else:
        simulation = Cube()

    while True:
        state_old = agent.get_state(simulation)

        final_move = agent.get_action(state_old)

        state_new, reward, done, info = simulation.step(final_move)
        
        #Calculate score as percentage of correct corners
        score = (info['correct_corners'] / 8) * 100
        
        # Update visualization if provided and it's a visualized episode
        if visualizer:
            if agent.n_attempts % visualize_every == 0:
                visualizer.update_colors()
                rate(visualization_speed) # Control speed during visualized episodes



        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            simulation.reset(scramble_moves = SCRAMBLE_LENGTH)
            agent.n_attempts += 1
            agent.train_long_memory()

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_attempts
            plot_mean_scores.append(mean_score)
            

            if len(plot_scores) >= window_size:
                recent_mean = sum(plot_scores[-window_size:]) / window_size
            else:
                recent_mean = mean_score
            
            if recent_mean > best_mean_score:
                best_mean_score = recent_mean
                agent.model.save()
                print(f'New best avg ({recent_mean:.1f}%)! Model saved.')
            
            if score > record:
                record = score

            print(f'Simulation {agent.n_attempts} | Score: {score:.1f}% | Record: {record:.1f}% | Avg(last {min(window_size, len(plot_scores))}): {recent_mean:.1f}%')
            
            plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    
    """
    #Option 1: Train with visualization
    from simulation.cube_visualizer import CubeVisualizer
    simulation = Cube()
    visualizer = CubeVisualizer(simulation)
    train(visualizer=visualizer, visualize_every=1, visualization_speed=2)
    """

    #Option 2: Train WITHOUT visualization (faster)
    train()
