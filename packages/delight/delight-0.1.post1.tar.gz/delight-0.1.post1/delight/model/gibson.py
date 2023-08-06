import torch
import torch.nn as nn


import torch
import torch.nn as nn
from typing import *

# from omlet.learn import Swish, Conv2dWS
from omlet.learn import mlp
import enlight.utils as U
from enlight.rl import distributions

# FIXME
from kitten.model.encoder import *


class Encoder(nn.Module):
    def __init__(
        self,
        feature_dim: int,
        output_dim: int,
        image_mean: List[int],  # 3 dim
        image_std: List[int],  # 3 dim
    ):
        super().__init__()
        self.encoder = create_encoder("resnet9w32gn_ws", num_classes=feature_dim)
        self.feature_dim = feature_dim
        self.output_dim = output_dim
        self.image_mean = image_mean
        self.image_std = image_std

        self.head = nn.Sequential(
            nn.Conv1d(feature_dim, feature_dim, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv1d(feature_dim, output_dim, kernel_size=3, padding=1),
            nn.AdaptiveAvgPool1d((1,))
        )

        # self.head = mlp(
        #     input_dim=feature_dim,
        #     output_dim=output_dim,
        #     hidden_dim=hidden_dim,
        #     hidden_depth=hidden_depth,
        # )

    def forward(self, obs, detach=False):
        # obs is stacked, [N, 9, H, W]
        # resize to [3N, 3, H, W], apply encoder normally,
        # then use conv1d to combine temporal info
        obs = obs / 255.0

        N, C, H, W = obs.size()
        assert C % 3 == 0 and C > 3, f"num channel {C} must divide 3 and > 3"
        T = C // 3
        obs = obs.view(N * T, 3, H, W)
        obs = U.torch_normalize(obs, self.image_mean, self.image_std)

        h = self.encoder(obs)  # [N*T, feature_dim]
        if detach:
            h = h.detach()

        h = h.view(N, T, self.feature_dim).transpose(2, 1)  # [N, feature_dim, T]
        out = self.head(h)  # [N, output_dim, 1]
        return out.squeeze(dim=2)  # [N, output_dim]


class Actor(nn.Module):
    def __init__(self, encoder, action_shape, hidden_dim, hidden_depth, log_std_bounds):
        super().__init__()
        self.encoder = encoder
        self.log_std_bounds = log_std_bounds
        self.trunk = mlp(
            self.encoder.output_dim, hidden_dim, 2 * action_shape[0], hidden_depth
        )
        self.apply(U.weight_init)

    def forward(self, obs, detach_encoder=False):
        obs = self.encoder(obs, detach=detach_encoder)

        mu, log_std = self.trunk(obs).chunk(2, dim=-1)

        # constrain log_std inside [log_std_min, log_std_max]
        log_std = torch.tanh(log_std)
        log_std_min, log_std_max = self.log_std_bounds
        log_std = log_std_min + 0.5 * (log_std_max - log_std_min) * (log_std + 1)
        std = log_std.exp()

        return distributions.SquashedNormal(mu, std)


class Critic(nn.Module):
    def __init__(self, encoder, action_shape, hidden_dim, hidden_depth):
        super().__init__()

        self.encoder = encoder

        self.Q1 = mlp(
            self.encoder.output_dim + action_shape[0], hidden_dim, 1, hidden_depth
        )
        self.Q2 = mlp(
            self.encoder.output_dim + action_shape[0], hidden_dim, 1, hidden_depth
        )

        self.apply(U.weight_init)

    def forward(self, obs, action, detach_encoder=False):
        assert obs.size(0) == action.size(0)
        obs = self.encoder(obs, detach=detach_encoder)

        obs_action = torch.cat([obs, action], dim=-1)
        q1 = self.Q1(obs_action)
        q2 = self.Q2(obs_action)

        return q1, q2
