import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_QNet(nn.Module):
    """
    Note:
    Q-Network for Rubik's Cube solver using Q-Learning.
    - input_size: 24 (flattened 2x2 cube state: 6 faces × 4 stickers)
    - hidden_size: 256 (hidden layer neurons)
    - output_size: 9 (9 possible moves: U, U', U2, F, F', F2, R, R', R2)
    
    Only uses R, U, F moves (D, L, B are equivalent on 2x2 cube)
    """
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, hidden_size//2)
        self.linear3 = nn.Linear(hidden_size//2, hidden_size//4)
        self.linear4 = nn.Linear(hidden_size//4, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        x = F.relu(self.linear3(x))
        x = self.linear4(x)
        return x
    
    def save(self, file_name='model.pth'):
        model_folder_path = './model'
        if not  os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        
        file_name = os.path.join(model_folder_path, file_name)
        
        # Save only model weights for curriculum training flexibility
        torch.save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, model, lr, gamma, target_model=None):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.target_model = target_model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        # Handle state/next_state if they are already tensors (from one-hot in agent)
        if not isinstance(state, torch.Tensor):
            state = torch.tensor(state, dtype=torch.float)
        else:
            state = state.float() # Ensure float
            
        if not isinstance(next_state, torch.Tensor):
            next_state = torch.tensor(next_state, dtype=torch.float)
        else:
            next_state = next_state.float() # Ensure float

        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        pred = self.model(state)        #predicted Q values with current state

        target = pred.clone()
        
        # Use target model for next state predictions if available
        next_state_model = self.target_model if self.target_model else self.model

        for i in range(len(done)):
            Q_new = reward[i]
            if not done[i]:
                Q_new = reward[i] + self.gamma * torch.max(next_state_model(next_state[i]))

            target[i][action[i].argmax()] = Q_new
        
        self.optimizer.zero_grad()

        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()