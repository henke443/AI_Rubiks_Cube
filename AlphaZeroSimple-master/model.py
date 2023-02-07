import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F


class RubiksModel(nn.Module):

    def __init__(self, observation_size, action_size, device):

        super(RubiksModel, self).__init__()

        self.device = device
        # self.size = board_size
        self.observation_size = observation_size
        self.action_size = action_size

        # self.fc0 = nn.Flatten(start_dim=observation_size)
        self.fc1 = nn.Linear(in_features=observation_size, out_features=512)
        self.fc2 = nn.Linear(in_features=512, out_features=512)

        # Two heads on our network
        self.action_head = nn.Linear(
            in_features=512, out_features=self.action_size)

        self.value_head = nn.Linear(in_features=512, out_features=1)

        self.to(device)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))

        action_logits = self.action_head(x)
        value_logit = self.value_head(x)

        return F.softmax(action_logits, dim=1), torch.tanh(value_logit)

    def predict(self, observation):
        observation = torch.FloatTensor(
            observation.astype(np.float32)).to(self.device)
        observation = observation.view(1, self.observation_size)
        self.eval()
        with torch.no_grad():
            pi, v = self.forward(observation)

        return pi.data.cpu().numpy()[0], v.data.cpu().numpy()[0]
