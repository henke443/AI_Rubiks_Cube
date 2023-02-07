import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F


class RubiksModel(nn.Module):

    def __init__(self, observation_size, device):

        super(RubiksModel, self).__init__()

        self.device = device
        # self.size = board_size
        self.observation_size = observation_size

        # self.fc0 = nn.Flatten(start_dim=observation_size)
        self.fc1 = nn.Linear(in_features=observation_size, out_features=256)
        self.fc2 = nn.Linear(in_features=256, out_features=256)

        self.value_head = nn.Linear(in_features=256, out_features=1)

        self.to(device)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))

        value_logit = self.value_head(x)

        return torch.tanh(value_logit)

    def predict(self, observation):
        observation = torch.FloatTensor(
            observation.astype(np.float32)).to(self.device)
        observation = observation.view(1, self.observation_size)
        self.eval()
        with torch.no_grad():
            v = self.forward(observation)

        return v.data.cpu().numpy()[0]
